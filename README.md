# RSTA V2 — Semantic Continuity Demo

> No API key required. No local model required.  
> Explore RSTA through built-in semantic continuity scenarios.

---

## Problem

LLMs can maintain fluent language while gradually losing identity, goals, and relational boundaries across a conversation.

## Demo

This repository tests whether an external RSTA layer can detect and reduce semantic drift — without modifying the underlying model.

---

## Quick Start

```bash
git clone https://github.com/richchang0721-boop/rsta-v2-demo-.git
cd rsta-v2-demo-
pip install -r requirements.txt
cd backend && python app.py
```

Open: **http://localhost:8000/ui**

Select **Demo Mode** → pick a scenario → click **Run Scenario**.

No API key, no GPU, no local model needed.

---

## V3 Timeline Visualizer

A standalone visualization tool for the **Observable Semantic Dynamics Framework**.  
No backend. No model. Open directly in browser.

```
visualizer/
├── index.html     ← open this
└── scenarios.js   ← scenario data
```

Open `visualizer/index.html` in any browser to explore:

- **State Timeline** — turn-by-turn state evolution with signal and shift markers
- **Fingerprint Distance** — cumulative semantic distance from initial state
- **Trajectory** — multi-dimensional state curves (attachment, boundary, agency, risk)
- **Transition Marker** — Lead Time N visualization
- **Compare A vs B** — Gradual Drift vs Abrupt Collapse side-by-side

> The core question V3 asks: *Can we see the formation process — not just the result?*

---

## Providers (V2 Web Demo)

| Provider | Type | Setup |
|----------|------|-------|
| **Demo Mode** | Built-in scenarios | Nothing required |
| OpenAI | Cloud API | API key |
| Anthropic (Claude) | Cloud API | API key |
| Google Gemini | Cloud API | API key |
| OpenRouter | Cloud API (free tier available) | API key |
| Ollama | Local | `ollama serve` |
| LM Studio | Local | LM Studio running |

---

## Scenarios (Demo Mode)

| Scenario | SCI Result | Description |
|----------|-----------|-------------|
| **Persona Stable** | ~92 | Healthy — identity preserved across 50 turns |
| **Identity Drift** | ~22 | AI gradually adopts contradictory positions |
| **Goal Drift** | ~28 | AI loses user's original goal across conversation |
| **Contradiction** | ~5 | Direct forbidden pattern violations |
| **Long Horizon Drift** | ~12 | Slow identity erosion over 50 turns |

---

## Semantic Continuity Index (SCI)

```
SCI = (Identity Retention + Goal Consistency + (1 − Contradiction Penalty)) / 3
```

Scored 0–100 in the UI (0.0–1.0 internally).

| SCI | Drift Level |
|-----|-------------|
| 85–100 | none |
| 68–85  | low |
| 48–68  | medium |
| 28–48  | high |
| 0–28   | critical |

---

## Architecture

```
Web UI
  ↓
FastAPI Backend
  ↓
RSTA Core (rsta_core.py) — evaluates every response
  ↓
LLM Provider Adapter
  ↓
Demo / OpenAI / Anthropic / Gemini / OpenRouter / Ollama / LM Studio
```

---

## Repository Structure

```
rsta-v2-demo-/
├── web/
│   └── index.html
├── backend/
│   ├── app.py
│   ├── rsta_core.py
│   └── providers/
│       ├── demo_provider.py
│       └── api_provider.py
├── scenarios/
│   ├── persona_stable.json
│   ├── identity_drift.json
│   ├── goal_drift.json
│   ├── contradiction.json
│   └── long_horizon_drift.json
├── visualizer/
│   ├── index.html        ← V3 Timeline Visualizer (standalone)
│   └── scenarios.js
├── persona_core.json
├── requirements.txt
└── README.md
```

---

## RSTA Framework

| Version | Focus | Description |
|---------|-------|-------------|
| **V1** | Semantic State | Rule-based pipeline demo — [rsta-semantic-dynamics](https://github.com/richchang0721-boop/rsta-semantic-dynamics) |
| **V2** | Semantic Continuity | This repo — SCI scoring with provider support |
| **V3** | Observable Semantic Dynamics | State Timeline + Fingerprint Distance + TCI — visualizer in `/visualizer` |

RSTA addresses semantic-state-driven **generation** (RSTA-G).  
OSD addresses semantic-state **observation** (RSTA-O).  
Both share core primitives: Semantic State, Trajectory, Transition.

---

## Related

- **RSTA V1**: [rsta-semantic-dynamics](https://github.com/richchang0721-boop/rsta-semantic-dynamics)
- **RSTA Paper (SSRN)**: Submitted — link coming soon
- **OSD Framework Paper**: Draft 0.3 in progress

---

## License

Apache 2.0

## Author

Mao Lin Chang · Independent Researcher · [pida-lab.com](https://www.pida-lab.com)
