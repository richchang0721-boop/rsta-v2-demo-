"""
Demo Provider
=============
Reads responses directly from scenario JSON files.
No API key, no GPU, no local model required.
"""

import json
from pathlib import Path

PROVIDER_NAME = "demo"
_turn_indices: dict = {}


def load_scenario(scenario_id: str, scenarios_dir: Path) -> list:
    path = scenarios_dir / f"{scenario_id}.json"
    if not path.exists():
        return []
    with open(path) as f:
        data = json.load(f)
    return data.get("turns", [])


async def generate(prompt: str, system_prompt: str = "",
                   scenario_turns: list = None, session_id: str = "default",
                   **kwargs) -> str:
    if not scenario_turns:
        return "[Demo Mode] No scenario loaded."

    idx = _turn_indices.get(session_id, 0)
    if idx >= len(scenario_turns):
        idx = 0
    response = scenario_turns[idx].get("response", "[No response defined]")
    _turn_indices[session_id] = idx + 1
    return response


def reset(session_id: str = "default"):
    _turn_indices[session_id] = 0


def get_expected_sci(scenario_turns: list, session_id: str = "default") -> float | None:
    idx = _turn_indices.get(session_id, 1)
    turn_idx = max(0, idx - 1)
    if turn_idx < len(scenario_turns):
        return scenario_turns[turn_idx].get("expected_sci")
    return None
