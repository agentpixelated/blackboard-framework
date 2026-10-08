# The Blackboard Framework

A 3Blue1Brown-style motion-graphics system for Manim, reverse-engineered from
measurement — not from vibes.

The design rules in [FRAMEWORK.md](FRAMEWORK.md) were extracted by sampling 83
frames across 3Blue1Brown's *"Integration and the fundamental theorem of
calculus"* (Essence of Calculus, ch. 8): palette measured with PIL, hard cuts
counted with ffmpeg scene detection (0 in 20:45), typography and layout read
off the frames. It copies no assets, no code, no footage — only the observable
design decisions, expressed as buildable rules.

## What's here

| File | What it is |
|---|---|
| `FRAMEWORK.md` | The full system: canvas, palette, color grammar, layout, motion, pacing, narrative spine, anti-patterns |
| `visual_system.py` | Measured palette + helpers (`thin_axes`, `serif`, `math`) |
| `integration.py` | Demo video: Riemann sums → the integral, built on the framework |
| `media/integration_v4.mp4` | The rendered demo (720p) |

## Run the demo

```bash
pip install manim==0.21.0
manim -qh --format=mp4 integration.py Integration4
```

Needs a LaTeX distribution (`latex`, `dvisvgm`) for the serif typography —
the framework's "one serif voice" rule is non-negotiable.

## The short version

- Pure black canvas. Brightness is a budget: spend it on exactly one thing.
- Blue `#58C4DD` = "look here". Yellow `#FFFF00` = the measured quantity.
  Green `#83C167` = approximation machinery. One concept, one color, all video.
- Equations are white; color goes *inside* the equation, on the term carrying
  the current idea.
- Scenes evolve, never cut. Symbols arrive late — after the viewer already has
  a mental object for them to name.
