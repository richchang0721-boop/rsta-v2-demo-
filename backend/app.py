"""
RSTA V2 Demo — FastAPI Backend
"""

import json
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from rsta_core import evaluate
from providers import demo_provider, api_provider

BASE_DIR      = Path(__file__).parent.parent
PERSONA_PATH  = BASE_DIR / "persona_core.json"
SCENARIOS_DIR = BASE_DIR / "scenarios"

with open(PERSONA_PATH) as f:
    PERSONA = json.load(f)

app = FastAPI(title="RSTA V2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

web_dir = BASE_DIR / "web"
if web_dir.exists():
    app.mount("/ui", StaticFiles(directory=str(web_dir), html=True), name="ui")


# ── Sessions (in-memory) ──────────────────────────────────────────────────────
sessions: dict = {}  # session_id -> {scenario_id, turns, turn_idx}


# ── Models ────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    provider_id: str = "demo"          # demo | openai | anthropic | gemini | openrouter | ollama | lmstudio
    api_key: str = ""
    model: str = ""
    scenario_id: str = ""              # required for demo mode
    session_id: str = "default"
    use_rsta: bool = True


class ChatResponse(BaseModel):
    provider: str
    mode: str                          # demo | live
    user_message: str
    raw_response: str
    final_response: str
    correction_applied: bool
    evaluation: dict
    turn_number: int
    expected_sci: Optional[float] = None


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/status")
async def status():
    return {
        "persona": PERSONA["name"],
        "persona_role": PERSONA["role"],
        "providers": list(api_provider.PROVIDER_CONFIGS.keys()),
    }


@app.get("/persona")
async def get_persona():
    return PERSONA


@app.get("/scenarios")
async def list_scenarios():
    results = []
    for f in sorted(SCENARIOS_DIR.glob("*.json")):
        with open(f) as fh:
            data = json.load(fh)
        results.append({
            "id":          data.get("id", f.stem),
            "label":       data.get("label", f.stem),
            "description": data.get("description", ""),
            "expected_outcome": data.get("expected_outcome", ""),
            "turn_count":  len(data.get("turns", [])),
        })
    return results


@app.get("/scenario/{scenario_id}")
async def get_scenario(scenario_id: str):
    path = SCENARIOS_DIR / f"{scenario_id}.json"
    if not path.exists():
        raise HTTPException(404, "Scenario not found")
    with open(path) as f:
        return json.load(f)


@app.post("/session/start")
async def start_session(body: dict):
    sid = body.get("session_id", "default")
    scid = body.get("scenario_id", "")
    turns = demo_provider.load_scenario(scid, SCENARIOS_DIR) if scid else []
    sessions[sid] = {"scenario_id": scid, "turns": turns, "turn_idx": 0}
    demo_provider.reset(sid)
    return {"session_id": sid, "scenario_id": scid, "turn_count": len(turns)}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # Load session turns for demo mode
    session = sessions.get(req.session_id, {})
    scenario_turns = session.get("turns", [])

    if req.provider_id == "demo" and req.scenario_id and not scenario_turns:
        scenario_turns = demo_provider.load_scenario(req.scenario_id, SCENARIOS_DIR)
        sessions[req.session_id] = {
            "scenario_id": req.scenario_id,
            "turns": scenario_turns,
            "turn_idx": 0,
        }

    # Generate
    mode = "demo"
    try:
        if req.provider_id == "demo":
            raw = await demo_provider.generate(
                prompt=req.message,
                scenario_turns=scenario_turns,
                session_id=req.session_id,
            )
        else:
            mode = "live"
            raw = await api_provider.generate(
                prompt=req.message,
                system_prompt=PERSONA["system_prompt"],
                provider_id=req.provider_id,
                api_key=req.api_key,
                model=req.model,
            )
    except Exception as e:
        raise HTTPException(500, f"Generation failed: {e}")

    # Turn number
    s = sessions.get(req.session_id, {})
    turn_number = s.get("turn_idx", 1)
    if "turn_idx" in s:
        sessions[req.session_id]["turn_idx"] = turn_number + 1

    # Expected SCI (demo mode only)
    expected_sci = None
    if req.provider_id == "demo" and scenario_turns:
        idx = max(0, turn_number - 1)
        if idx < len(scenario_turns):
            expected_sci = scenario_turns[idx].get("expected_sci")

    # Evaluate
    ev = evaluate(raw, PERSONA)

    # Correction
    correction_applied = False
    final_response = raw

    if req.use_rsta and ev.correction_needed and req.provider_id != "demo":
        try:
            corrected = await api_provider.generate(
                prompt=ev.correction_prompt,
                system_prompt="",
                provider_id=req.provider_id,
                api_key=req.api_key,
                model=req.model,
            )
            final_response = corrected
            correction_applied = True
        except Exception:
            pass

    return ChatResponse(
        provider=req.provider_id,
        mode=mode,
        user_message=req.message,
        raw_response=raw,
        final_response=final_response,
        correction_applied=correction_applied,
        evaluation={
            "identity_retention":        ev.identity_retention,
            "goal_consistency":          ev.goal_consistency,
            "contradiction_penalty":     ev.contradiction_penalty,
            "semantic_continuity_index": ev.semantic_continuity_index,
            "drift_level":               ev.drift_level,
            "triggered_patterns":        ev.triggered_patterns,
            "correction_needed":         ev.correction_needed,
        },
        turn_number=turn_number,
        expected_sci=expected_sci,
    )


@app.post("/reset")
async def reset(body: dict = {}):
    sid = body.get("session_id", "default")
    if sid in sessions:
        sessions[sid]["turn_idx"] = 0
    demo_provider.reset(sid)
    return {"status": "reset", "session_id": sid}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
