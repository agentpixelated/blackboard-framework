# Video Format Options

Five reusable formats for Blackboard Framework videos. Pick one per video
based on the learning goal. All formats share the visual system
(`visual_system.py`): pure black background, serif prose, real LaTeX,
in-equation term coloring, and the keyword→visual color grammar
(weight `#b86e64`, tension/normal `BLUE`/`GREEN`, key results `YELLOW`).

---

## Format 1 — Concept from Basic Formulas

**Goal:** teach a concept starting from its defining equations.

**Structure:**
1. State the concept in one plain sentence.
2. Write the base formula; color each term by meaning.
3. Derive consequences step by step (one transformation per beat).
4. End with the boxed result + one-line intuition.

**Use when:** the concept IS an equation (e.g. kinematic formulas,
Coulomb's law).

---

## Format 2 — Concept Geometrically

**Goal:** teach a concept through shapes and spatial reasoning.

**Structure:**
1. Draw the geometry slowly (nothing labeled at first).
2. Name each part as it appears (keyword first, then the element).
3. Show the relationship visually (lengths, angles, areas).
4. Read the formula off the picture at the end.

**Use when:** the concept IS a picture (e.g. trig on the unit circle,
projectile trajectory).

---

## Format 3 — Concept, Formulas + Geometry Combined

**Goal:** bind the equation to the picture.

**Structure:**
1. Formula on the left, geometry on the right (split screen).
2. Each term in the formula lights up together with its geometric
   counterpart (same color, same beat).
3. Manipulate one, show the other responding.

**Use when:** the learner must connect symbols to meaning
(e.g. `v² = gR` ↔ forces at the loop's top).

---

## Format 4 — Problem, Equation Solving Only

**Goal:** drill algebraic problem-solving.

**Structure:**
1. Problem statement (brief) + "Diketahui / Ditanya" panel.
2. Straight to equations: one line of working per beat.
3. Box the answer; options row if multiple choice.

**Use when:** the setup is already understood and only the
computation needs practice.

---

## Format 5 — Problem, Keyword-to-Visual Translation

**Goal:** teach how to READ a problem: turn words into a picture,
then the picture into equations.

**Layout:** split screen — original problem text on the LEFT,
visualization canvas on the RIGHT.

**Phase A — the problem, verbatim.**
Left panel shows the original problem text, complete and unedited.
Right panel starts empty.

**Phase B — keyword marking → gradual visualization.**
Walk through the problem text word by word. Mark each keyword
in place (do not rephrase):
- **words** (concepts: "katrol", "tegangan tali") → concept color,
- **shapes/forms** ("bidang miring", "loop lingkaran") → shape color,
- **numbers** ("4 kg", "37°", "0,5 m") → value color.

Each marked keyword then BECOMES a visual element on the right:
the word "katrol" fades into the drawn pulley, "37°" into the angle
arc, "4 kg" into the labeled block. Strictly one element per beat —
never draw the whole diagram at once. The text stays visible while
its keywords turn into the picture.

**Phase C — strip down to the givens.**
The problem text fades out, leaving only a "Diketahui:" panel
(the marked numbers and facts). The completed diagram stays on
the right.

**Phase D — solve step by step.**
Equation solving, one transformation per beat, with the same
term colors as the diagram, until the boxed answer (and the
multiple-choice options row, correct one boxed).

**Use when:** the learner struggles to start — they can do the
math but cannot translate the problem statement into a setup.
