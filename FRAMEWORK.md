# The Blackboard Framework
### A 3Blue1Brown-style motion-graphics system, reverse-engineered from measurement

Reference: 3Blue1Brown — "Integration and the fundamental theorem of calculus"
(Essence of Calculus, ch. 8). 83 frames sampled across 20:45, palette measured
with PIL, hard cuts counted with ffmpeg scene detection.

This is an original synthesis. It copies no assets, no code, and no footage —
only the observable design decisions, expressed as buildable rules.

---

## 1. Canvas

- **Background is pure black** (`#000000`). Not dark gray, not navy. Measured across
  dozens of frames: `(0, 0, 0)`.
- The black is doing compositional work: bright objects float, whitespace is free,
  and the eye has exactly one place to go.

## 2. Typography: one serif voice

- **All text is serif** — prose, labels, and math share the same Computer Modern
  voice (LaTeX). There is no sans-serif anywhere on screen.
- Math and English are visually continuous: a sentence can contain an equation and
  it looks like one thought, not two media.
- Tick labels, axis labels, annotations: small serif, white or gray.
- Rule: if you are tempted to use a sans font for "readability", you have already
  lost the look.

## 3. Palette (measured, not guessed)

| Role | Hex | Notes |
|---|---|---|
| Background | `#000000` | pure black |
| Primary blue | `#58C4DD` | the "look here" color; variables of interest |
| Yellow | `#FFFF00` | the active slice / measured quantity / emphasis |
| Green | `#83C167` | approximation machinery (rectangles, sums) |
| White | `#FFFFFF` | equations, prose |
| Gray | `#888888` | axes, ticks, passive context |

Measured samples: bright blue `#51b7cc`, yellow `#e5e216`, green `#a8cc66`,
all within video-compression distance of the canonical values above.

## 4. The color grammar (the real secret)

1. **Equations are white by default.** Color is applied *within* the equation,
   only to the term carrying the current idea: blue `s(T)`, yellow `T`,
   green `h`. Everything else stays white.
2. **One concept = one color for the whole video.** If `dt` is yellow in minute
   3, it is yellow in minute 18.
3. **Fills are dark and muted.** Rectangle/area fills sit at low brightness
   (measured fills: `#162a29`, `#122f1d` — dark desaturated teal-green).
   Brightness is a budget: spend it on exactly one thing.
4. **Gradients, not flats.** Large areas use a blue→green gradient fill, darker
   at the edges. Flat bright fills never appear.
5. **Highlight = brighten one + dim the rest.** To focus a single rectangle: it
   goes bright blue/yellow, everything else drops opacity. Never add a glow,
   outline pulse, or zoom when a brightness change will do.

## 5. Geometry & layout

- **Axes are whispers.** Thin strokes, gray (`#888888`), small serif tick labels.
  They orient; they never compete.
- **The equation is the headline.** It sits top-left or top-center, large.
  The visual field lives below/beside it.
- **Thin white arrows** connect symbols to the visual they name. The arrow is
  the argument: "this symbol *is* that thing."
- **Labels sit in whitespace** next to curves, italic serif, in the curve's
  color family but dimmer. They never touch the curve.
- **One idea per frame.** If a screenshot needs two captions to explain, split
  the beat.

## 6. Motion grammar

- **Measured: 0 hard cuts detected in 20:45** (ffmpeg scene detection at
  thresholds 0.2–0.4). Effectively cut-free. Scenes do not cut; they *evolve*.
  Objects persist across the entire video and transform into their next form.
- Every transition should answer "where did this come from?" If it can't,
  it's a cut wearing a costume.
- Camera is essentially static. No pans, no zooms for decoration.
- Standard moves:
  - `Create` — something is being constructed (axes, curve)
  - `Write` — an equation is being stated (always with LaTeX)
  - `Transform` / `TransformMatchingTex` — an idea changing form
  - brightness/opacity shift — change of focus
  - `FadeIn` — context entering quietly; `FadeOut` — context leaving

## 7. Pacing

- Dwell on the **question** before the machinery. The video spends its first
  minutes making "distance from velocity" feel like a real puzzle.
- Symbols arrive **after** the viewer already has a mental object for them
  to name. The integral sign appears late, as a compression of something
  already understood.
- Beats: show → hold (let the eye explore) → highlight → transform → hold.

## 8. Narrative spine (integration-shaped)

```
concrete situation  →  a quantity you want but can't measure directly
visual experiment   →  chop it into measurable pieces
pattern             →  more pieces → closer to truth
invariant           →  the shape stays; the error shrinks
symbol (late!)      →  Σ …  becomes  ∫ …  (one continuous morph)
resolve             →  the exact value, colored as the payoff
```

## 9. What NOT to do (measured anti-patterns)

- No sans-serif. No dark-gray/navy background. No bright flat fills.
- No coloring a whole formula one color — color the *term*.
- No hard cuts between ideas. No decorative camera moves.
- No label touching a curve. No two focal points in one frame.
- No equation before its intuition exists.

## 10. Manim implementation notes

- `config.background_color = "#000000"`
- **All** text via `Tex`/`MathTex`/`TexText` (serif). Never `Text` with a
  sans font.
- Area fills: `set_color_by_gradient(BLUE_DARK, GREEN_DARK)` or low-opacity
  dark fills; brighten single elements with `.animate.set_color(YELLOW)`.
- Axes: `axis_config={"color": GREY, "stroke_width": 2}`, small `Tex` tick labels.
- In-equation coloring: build `MathTex` from substring args, `set_color` per term.
- Arrows: `Arrow(..., color=WHITE, stroke_width=3, buff=...)` from term to visual.
- **Number swaps: use `FadeTransform`, never raw `Transform` on `DecimalNumber`
  or `MathTex` counters** — raw `Transform` leaves ghost glyphs (measured defect
  in v3 audit, 2026-10-07).
- **No dead frames:** never leave black screen with a single axis line while
  the next element "loads" — overlap the outgoing fade with the incoming
  `Create` (measured defect in v3 audit, 2026-10-07).
