# Trig Circle Reference — @phainumat (TikTok)

Visual reference for unit-circle trigonometry animations. Saved 2026-10-08.
Video (local only, creator's content — not redistributed):
`~/workspace/references/trig-unit-circle-phainumat.mp4` (1024×576, 22s, 30fps).

A 22-second animation showing all six trig functions as live segments on the
unit circle, each traced out as its graph. The single best reference for
"unit circle → graph" videos.

## Palette (measured with PIL from frames)

| Element | Hex | Notes |
|---|---|---|
| Background | `#000000` | Pure black |
| Grid | `#040608` | Barely-visible dark blue-gray grid, whole frame |
| Axes | `#FFFFFF` | White, with arrowheads |
| Unit circle | `#5ba5bc` | Teal-blue |
| θ arc | gold/yellow | Small arc at origin |
| sin | `#91ad85` | Sage green |
| cos | `#b86e64` | Salmon red |
| tan | `#bf7f49` | Orange |
| sec | `#917d9f` | Muted lavender gray-purple |
| csc | teal `#5aa8a0`~ | Same family as the circle |
| cot | magenta `#aa4e98`~ | Pink-purple |

Color grammar rule: **every function owns one color, used identically** in the
legend, on the circle segment, in the formula, on the graph curve, and in the
title. Mixed-color formulas: `tan θ = sin θ/cos θ` renders each term in its
own function color.

## Typography

Serif throughout (Computer Modern-like). Math labels white; function names in
their colors. Point label `(x, y)` with `x` in cos-red, `y` in sin-green —
the color grammar extends into the coordinates themselves.

## Layout

- Left ~40%: unit circle, centered, generous black space around it.
- Right ~50%: graph axes (θ axis marked `0, π/2, π, 3π/2, 2π`; y axis `-2..2`).
- Top-right: color-coded legend (function names only).
- Top-center of graph: title + formula per function (`Sine`, `y = sin(θ)`).
- Bottom-right: creator watermark (theirs — don't copy).

## Animation beats

1. Axes draw in (white, arrowheads).
2. Unit circle draws (teal).
3. Radius line + θ arc (gold) + dashed gray projections to both axes.
4. Point labeled `(x, y)` — x in cos-color, y in sin-color.
5. Legend fades in, six functions color-coded.
6. Tangent line (orange, vertical at x=1) and cotangent line (magenta,
   horizontal at y=1) draw; secant/cosecant rays extend from origin.
7. Graph axes fade in on the right; a dashed connector links the moving
   circle point to the drawing graph tip.
8. Per function: title + formula appear, then the curve draws itself in the
   function color as θ sweeps 0 → 2π. Asymptotes as dashed verticals
   (tan, sec, csc, cot).
9. Finale: `All Trig Graphs` — all six curves overlaid, one per color,
   with a small color-word legend.

## Reusable techniques for our framework

- **Segment = value.** Each trig function is drawn as a *line segment on the
  circle* (sin = vertical green segment = y, cos = horizontal red = x,
  tan = orange tangent segment, …), not as a number. The graph is then just
  the segment's length over θ.
- **Dashed projection lines** (gray, thin) connect circle → axes → graph.
  They are the visual glue between the three views.
- **One θ to drive everything**: a single ValueTracker for θ updates the
  radius, all six segments, the arc, the point, and every graph tip.
- **Asymptotes**: dashed vertical lines at π/2, 3π/2, … drawn before the
  discontinuous curves (tan/sec/csc/cot).
- **Finale overlay**: all curves on one axes with the color-word legend is
  the money shot — build toward it.

## Relation to the Blackboard Framework

Same black background, serif type, and "color = meaning" discipline as
FRAMEWORK.md. Differences: this reference adds a **subtle full-frame grid**
(ours is pure black — grid is optional dressing), uses **brighter, more
varied hues** (six functions need six distinguishable colors; our palette is
more restrained), and leans on **dashed construction lines** where we lean on
fades. When doing trig videos, adopt this reference's color grammar and
segment-as-value technique; keep our typography and pacing.
