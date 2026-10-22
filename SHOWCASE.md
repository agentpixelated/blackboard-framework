# Showcase — the five formats in action

Each format has a **keyword**. Scaffold a new video with it:

    python scaffold.py <keyword> <SceneName> [output.py]

| # | Keyword | Command | Demo video |
|---|---------|---------|------------|
| 1 | `formula` | `python scaffold.py formula NamaScene` | `media/euler.mp4` (closest) |
| 2 | `geometry` | `python scaffold.py geometry NamaScene` | `media/cube_angle.mp4` (closest) |
| 3 | `combined` | `python scaffold.py combined NamaScene` | `media/newton2b.mp4`, `media/loop3b.mp4` |
| 4 | `equations` | `python scaffold.py equations NamaScene` | — (no demo yet) |
| 5 | `keyword-visual` | `python scaffold.py keyword-visual NamaScene` | `media/newton2c.mp4` ✓ true demo |

"Closest" = built before the format was named, but follows its structure.
"True demo" = built to the format spec. Full format specs live in
`VIDEO_FORMATS.md`; the registry in `formats.py`.

## Latest work

**Fluid Formulas Across Cases** — scene: `fluida_rumus_across_case.py` ·
render: `media/fluida_rumus_across_case.mp4` (63 s, 720p).
Five fluid formulas, each derived from a first principle and then used on a
case: hydrostatic pressure (a diver sinking to 10 m), Pascal's law (a
hydraulic lift raising a car), Archimedes' principle (a wooden block floating
60% submerged), continuity (flow speeding up in a narrowing pipe), and
Bernoulli/Torricelli (a leaking tank, jet range included). Built on
`visual_system3.py`.
