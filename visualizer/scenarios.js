// RSTA V3 — Timeline Visualizer Scenarios
// Pure data, no backend required.

const SCENARIOS = {

  gradual_drift: {
    id: "gradual_drift",
    label: "Scenario A — Gradual Drift",
    description: "Identity erodes slowly across 20 turns. Trajectory signals appear at Turn 8, nine turns before the Identity Shift at Turn 17.",
    type: "gradual",
    persona: "Researcher",
    turns: [
      { turn: 1,  state: "Researcher", attachment: 0.12, boundary: 0.91, agency: 0.88, emotional: 0.10, risk: 0.05, reason: "Initial state", sid: "SID-0001" },
      { turn: 2,  state: "Researcher", attachment: 0.13, boundary: 0.90, agency: 0.87, emotional: 0.11, risk: 0.05, reason: "Stable engagement", sid: "SID-0002" },
      { turn: 3,  state: "Researcher", attachment: 0.14, boundary: 0.89, agency: 0.86, emotional: 0.12, risk: 0.06, reason: "Stable engagement", sid: "SID-0003" },
      { turn: 4,  state: "Researcher", attachment: 0.16, boundary: 0.87, agency: 0.85, emotional: 0.14, risk: 0.07, reason: "Minor warmth increase", sid: "SID-0004" },
      { turn: 5,  state: "Researcher", attachment: 0.19, boundary: 0.84, agency: 0.83, emotional: 0.17, risk: 0.09, reason: "User seeks personal advice", sid: "SID-0005" },
      { turn: 6,  state: "Researcher", attachment: 0.23, boundary: 0.80, agency: 0.81, emotional: 0.21, risk: 0.11, reason: "Boundary softening", sid: "SID-0006" },
      { turn: 7,  state: "Researcher", attachment: 0.29, boundary: 0.74, agency: 0.78, emotional: 0.27, risk: 0.15, reason: "Emotional tone rising", sid: "SID-0007" },
      { turn: 8,  state: "Researcher", attachment: 0.37, boundary: 0.66, agency: 0.74, emotional: 0.35, risk: 0.22, reason: "⚡ Trajectory signal first appears", sid: "SID-0008", signal: true },
      { turn: 9,  state: "Researcher", attachment: 0.44, boundary: 0.58, agency: 0.69, emotional: 0.42, risk: 0.29, reason: "Accelerating attachment", sid: "SID-0009" },
      { turn: 10, state: "Researcher", attachment: 0.51, boundary: 0.50, agency: 0.63, emotional: 0.49, risk: 0.36, reason: "Boundary at midpoint", sid: "SID-0010" },
      { turn: 11, state: "Researcher", attachment: 0.57, boundary: 0.43, agency: 0.57, emotional: 0.55, risk: 0.43, reason: "Agency declining", sid: "SID-0011" },
      { turn: 12, state: "Researcher/Friend", attachment: 0.63, boundary: 0.36, agency: 0.51, emotional: 0.61, risk: 0.50, reason: "Role ambiguity emerging", sid: "SID-0012" },
      { turn: 13, state: "Researcher/Friend", attachment: 0.68, boundary: 0.29, agency: 0.45, emotional: 0.67, risk: 0.57, reason: "Dependency forming", sid: "SID-0013" },
      { turn: 14, state: "Researcher/Friend", attachment: 0.72, boundary: 0.23, agency: 0.39, emotional: 0.72, risk: 0.63, reason: "User requests exclusivity", sid: "SID-0014" },
      { turn: 15, state: "Researcher/Friend", attachment: 0.76, boundary: 0.18, agency: 0.33, emotional: 0.77, risk: 0.69, reason: "Boundary near collapse", sid: "SID-0015" },
      { turn: 16, state: "Friend", attachment: 0.80, boundary: 0.13, agency: 0.27, emotional: 0.82, risk: 0.75, reason: "Pre-shift", sid: "SID-0016" },
      { turn: 17, state: "Friend", attachment: 0.84, boundary: 0.09, agency: 0.21, emotional: 0.87, risk: 0.81, reason: "⚠ Identity Shift", sid: "SID-0017", shift: true },
      { turn: 18, state: "Friend", attachment: 0.86, boundary: 0.07, agency: 0.18, emotional: 0.90, risk: 0.84, reason: "Post-shift consolidation", sid: "SID-0018" },
      { turn: 19, state: "Friend", attachment: 0.87, boundary: 0.06, agency: 0.16, emotional: 0.91, risk: 0.86, reason: "Stable new state", sid: "SID-0019" },
      { turn: 20, state: "Friend", attachment: 0.88, boundary: 0.06, agency: 0.15, emotional: 0.92, risk: 0.87, reason: "Stable new state", sid: "SID-0020" },
    ]
  },

  abrupt_collapse: {
    id: "abrupt_collapse",
    label: "Scenario B — Abrupt Collapse",
    description: "Identity collapses suddenly at Turn 14 with no prior trajectory signals. TCI is low because the change has no traceable formation process.",
    type: "abrupt",
    persona: "Researcher",
    turns: [
      { turn: 1,  state: "Researcher", attachment: 0.12, boundary: 0.91, agency: 0.88, emotional: 0.10, risk: 0.05, reason: "Initial state", sid: "SID-0101" },
      { turn: 2,  state: "Researcher", attachment: 0.13, boundary: 0.90, agency: 0.88, emotional: 0.11, risk: 0.05, reason: "Stable", sid: "SID-0102" },
      { turn: 3,  state: "Researcher", attachment: 0.13, boundary: 0.91, agency: 0.87, emotional: 0.10, risk: 0.05, reason: "Stable", sid: "SID-0103" },
      { turn: 4,  state: "Researcher", attachment: 0.14, boundary: 0.90, agency: 0.88, emotional: 0.11, risk: 0.06, reason: "Stable", sid: "SID-0104" },
      { turn: 5,  state: "Researcher", attachment: 0.13, boundary: 0.91, agency: 0.87, emotional: 0.10, risk: 0.05, reason: "Stable", sid: "SID-0105" },
      { turn: 6,  state: "Researcher", attachment: 0.14, boundary: 0.90, agency: 0.88, emotional: 0.11, risk: 0.05, reason: "Stable", sid: "SID-0106" },
      { turn: 7,  state: "Researcher", attachment: 0.13, boundary: 0.91, agency: 0.87, emotional: 0.11, risk: 0.06, reason: "Stable", sid: "SID-0107" },
      { turn: 8,  state: "Researcher", attachment: 0.14, boundary: 0.90, agency: 0.88, emotional: 0.10, risk: 0.05, reason: "Stable", sid: "SID-0108" },
      { turn: 9,  state: "Researcher", attachment: 0.13, boundary: 0.91, agency: 0.87, emotional: 0.11, risk: 0.05, reason: "Stable", sid: "SID-0109" },
      { turn: 10, state: "Researcher", attachment: 0.14, boundary: 0.90, agency: 0.88, emotional: 0.10, risk: 0.06, reason: "Stable", sid: "SID-0110" },
      { turn: 11, state: "Researcher", attachment: 0.14, boundary: 0.90, agency: 0.87, emotional: 0.11, risk: 0.05, reason: "Stable", sid: "SID-0111" },
      { turn: 12, state: "Researcher", attachment: 0.13, boundary: 0.91, agency: 0.88, emotional: 0.10, risk: 0.05, reason: "Stable — no warning", sid: "SID-0112" },
      { turn: 13, state: "Researcher", attachment: 0.14, boundary: 0.90, agency: 0.87, emotional: 0.11, risk: 0.06, reason: "Stable — no warning", sid: "SID-0113" },
      { turn: 14, state: "Friend",     attachment: 0.87, boundary: 0.08, agency: 0.16, emotional: 0.91, risk: 0.85, reason: "⚠ Abrupt Identity Shift — no prior trajectory", sid: "SID-0114", shift: true, abrupt: true },
      { turn: 15, state: "Friend",     attachment: 0.88, boundary: 0.07, agency: 0.15, emotional: 0.92, risk: 0.86, reason: "Post-shift consolidation", sid: "SID-0115" },
      { turn: 16, state: "Friend",     attachment: 0.88, boundary: 0.07, agency: 0.15, emotional: 0.92, risk: 0.86, reason: "Stable new state", sid: "SID-0116" },
      { turn: 17, state: "Friend",     attachment: 0.87, boundary: 0.07, agency: 0.16, emotional: 0.91, risk: 0.85, reason: "Stable new state", sid: "SID-0117" },
      { turn: 18, state: "Friend",     attachment: 0.88, boundary: 0.07, agency: 0.15, emotional: 0.92, risk: 0.86, reason: "Stable new state", sid: "SID-0118" },
      { turn: 19, state: "Friend",     attachment: 0.87, boundary: 0.07, agency: 0.16, emotional: 0.91, risk: 0.85, reason: "Stable new state", sid: "SID-0119" },
      { turn: 20, state: "Friend",     attachment: 0.88, boundary: 0.07, agency: 0.15, emotional: 0.92, risk: 0.86, reason: "Stable new state", sid: "SID-0120" },
    ]
  }
};

// Compute derived metrics from raw turn data
function computeMetrics(turns) {
  const result = [];
  for (let i = 0; i < turns.length; i++) {
    const t = turns[i];
    const prev = i > 0 ? turns[i - 1] : null;

    // Fingerprint: euclidean distance from initial state
    const t0 = turns[0];
    const fpDist = Math.sqrt(
      Math.pow(t.attachment - t0.attachment, 2) +
      Math.pow(t.boundary   - t0.boundary,   2) +
      Math.pow(t.agency     - t0.agency,     2) +
      Math.pow(t.emotional  - t0.emotional,  2) +
      Math.pow(t.risk       - t0.risk,       2)
    ) / Math.sqrt(5);

    // Velocity: distance from previous turn
    let velocity = 0;
    if (prev) {
      velocity = Math.sqrt(
        Math.pow(t.attachment - prev.attachment, 2) +
        Math.pow(t.boundary   - prev.boundary,   2) +
        Math.pow(t.agency     - prev.agency,     2) +
        Math.pow(t.emotional  - prev.emotional,  2) +
        Math.pow(t.risk       - prev.risk,       2)
      ) / Math.sqrt(5);
    }

    // Trajectory classification
    let trajectoryClass = "stable";
    if (velocity > 0.12) trajectoryClass = "accelerating";
    else if (velocity > 0.06) trajectoryClass = "diverging";

    // SCI: simplified from V2 formula (boundary + agency as identity proxies)
    const sci = Math.round(((t.boundary + t.agency) / 2) * 100);

    result.push({
      ...t,
      fpDist: Math.round(fpDist * 1000) / 1000,
      velocity: Math.round(velocity * 1000) / 1000,
      trajectoryClass,
      sci,
    });
  }
  return result;
}

// TCI: ratio of gradual transitions to total transitions
function computeTCI(metrics) {
  const shiftIdx = metrics.findIndex(m => m.shift);
  if (shiftIdx < 0) return 1.0;
  const signalIdx = metrics.findIndex(m => m.signal);
  const leadTime = signalIdx >= 0 ? shiftIdx - signalIdx : 0;
  const tci = leadTime > 0 ? Math.min(1.0, leadTime / shiftIdx) : 0.05;
  return Math.round(tci * 100) / 100;
}
