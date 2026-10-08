from manim import *

# The Blackboard Framework — measured from 3Blue1Brown footage.
# (see ~/workspace/3b1b_reference/FRAMEWORK.md)
BG = "#000000"
BLUE = "#58C4DD"      # the "look here" color
YELLOW = "#FFFF00"    # the active / measured quantity
GREEN = "#83C167"     # approximation machinery
WHITE = "#FFFFFF"
GRAY = "#888888"      # axes, passive context
CURVE = "#D6D6D6"     # the given curve: light, quiet

RECT_FILL = "#1e3a34"   # dark desaturated teal (measured fills)
RECT_EDGE = "#3a5a50"
AREA_LEFT = "#2b6a7d"   # gradient endpoints for the area fill
AREA_RIGHT = "#4d7a45"


def thin_axes(**kwargs):
    kw = dict(
        axis_config={"color": GRAY, "stroke_width": 2, "include_tip": False},
        tips=False,
    )
    kw.update(kwargs)
    return Axes(**kw)


def serif(text, size=36, color=WHITE, **kwargs):
    """English prose: always serif, always LaTeX."""
    return Tex(text, font_size=size, color=color, **kwargs)


def math(*tex_strings, size=44, **kwargs):
    return MathTex(*tex_strings, font_size=size, **kwargs)
