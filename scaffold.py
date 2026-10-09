#!/usr/bin/env python3
"""Scaffold a new Blackboard Framework scene from a format keyword.

Usage:
    python scaffold.py <keyword> <SceneName> [output.py]

Keywords: formula, geometry, combined, equations, keyword-visual
Example:
    python scaffold.py keyword-visual KatrolF5 katrol_f5.py
"""
import sys
from formats import get, keywords

HEADER = '''from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif, math

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

W_RED = "#b86e64"
ORANGE = "#bf7f49"
'''

DIVIDER = '''
        # thin divider at x=0 (split-screen formats)
        div = Line([0, -4, 0], [0, 4, 0], color=GRAY, stroke_width=2,
                   opacity=0.4)
        self.add(div)
'''

TEMPLATES = {
    "formula": """
        # Beat 1: concept in one plain sentence
        # Beat 2: base formula, one color per term
        # Beat 3+: one transformation per beat (FadeTransform)
        # Final: box the result + one-line intuition
""",
    "geometry": """
        # Beat 1: draw the geometry slowly (Create), no labels yet
        # Beat 2: name each part — keyword text first, then the element
        # Beat 3: show the relationship (lengths / angles / areas)
        # Final: read the formula off the picture
""",
    "combined": """
        # LEFT x in [-6.9, -0.2]: full text or formula, keywords colored
        # RIGHT x in [0.2, 6.9]: the figure
        # Walk terms left to right: term + geometric counterpart light up
        # together (same color, same beat). Active text block: opacity 1.0
        # + translucent highlight bar; inactive blocks at 0.45.
""",
    "equations": """
        # Diketahui / Ditanya panel (top-left)
        # Equation chain: one line of working per beat, term colors carry
        # meaning across lines (use FadeTransform between steps)
        # Final: box the answer; options row, correct one boxed YELLOW
""",
    "keyword-visual": """
        # Phase A: problem text VERBATIM on the left (Tex, size ~26,
        # wrapped); right panel empty.
        # Phase B: for each keyword in order — mark it IN PLACE
        # (SurroundingRectangle + recolor via get_part_by_tex), pause,
        # then draw its ONE visual element on the right.
        #   words (concepts) -> concept color, shapes -> shape color,
        #   numbers -> value color (gold).
        # Phase C: fade the problem text; keep only the Diketahui panel.
        # Phase D: equations under Diketahui, synced visuals on the right,
        # one transformation per beat, until the boxed answer.
""",
}


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in keywords():
        print("Usage: python scaffold.py <keyword> <SceneName> [output.py]")
        print("Keywords:", ", ".join(keywords()))
        sys.exit(1)
    kw, name = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else f"{name.lower()}.py"
    fmt = get(kw)
    body = TEMPLATES[kw]
    split = DIVIDER if kw in ("combined", "keyword-visual") else ""
    code = (
        HEADER
        + f'\n\nclass {name}(Scene):\n    def construct(self):\n'
        + f'        # Format: {fmt["title"]}  (keyword: {kw})\n'
        + f'        # Goal: {fmt["goal"]}\n'
        + split
        + body
        + '        self.wait(1.0)\n'
    )
    with open(out, "w") as f:
        f.write(code)
    print(f"Scaffolded {out}  — format '{kw}': {fmt['title']}")


if __name__ == "__main__":
    main()
