"""Blackboard Framework — video format registry.

Five options, each with a keyword. Generate a starter scene with:
    python scaffold.py <keyword> <SceneName>

Keywords:
    formula         Concept from Basic Formulas        (Format 1)
    geometry        Concept Geometrically              (Format 2)
    combined        Concept, Formulas + Geometry       (Format 3)
    equations       Problem, Equation Solving Only     (Format 4)
    keyword-visual  Problem, Keyword-to-Visual         (Format 5)
"""

FORMATS = {
    "formula": {
        "title": "Concept from Basic Formulas",
        "goal": "Teach a concept starting from its defining equations.",
        "layout": "Full-screen equations, one transformation per beat.",
        "beats": [
            "State the concept in one plain sentence.",
            "Write the base formula; color each term by meaning.",
            "Derive consequences step by step (one transformation per beat).",
            "Box the result + one-line intuition.",
        ],
    },
    "geometry": {
        "title": "Concept Geometrically",
        "goal": "Teach a concept through shapes and spatial reasoning.",
        "layout": "Full-screen canvas; geometry drawn slowly, labels follow.",
        "beats": [
            "Draw the geometry slowly (nothing labeled at first).",
            "Name each part as it appears (keyword first, then the element).",
            "Show the relationship visually (lengths, angles, areas).",
            "Read the formula off the picture at the end.",
        ],
    },
    "combined": {
        "title": "Concept, Formulas + Geometry Combined",
        "goal": "Bind the equation to the picture.",
        "layout": "Split screen: formula/text LEFT, geometry RIGHT, divider at x=0.",
        "beats": [
            "Full text or formula on the left; basic figure on the right.",
            "Walk through terms left to right: each term lights up together "
            "with its geometric counterpart (same color, same beat).",
            "Manipulate one side, show the other responding.",
            "Box the takeaway.",
        ],
    },
    "equations": {
        "title": "Problem, Equation Solving Only",
        "goal": "Drill algebraic problem-solving when the setup is understood.",
        "layout": "Diketahui/Ditanya panel, then full-width equation chain.",
        "beats": [
            "Problem statement (brief) + Diketahui / Ditanya panel.",
            "Equation solving: one line of working per beat.",
            "Box the answer; options row if multiple choice.",
        ],
    },
    "keyword-visual": {
        "title": "Problem, Keyword-to-Visual Translation",
        "goal": "Teach how to READ a problem: words -> picture -> equations.",
        "layout": "Split screen: original problem text LEFT, canvas RIGHT.",
        "beats": [
            "Phase A: problem text verbatim on the left; right panel empty.",
            "Phase B: mark keywords in place (words/shapes/numbers, colored "
            "boxes); each keyword BECOMES one visual element on the right, "
            "strictly one per beat.",
            "Phase C: problem text fades, leaving only the Diketahui panel; "
            "diagram stays.",
            "Phase D: equation solving step by step (term colors match the "
            "diagram) until the boxed answer.",
        ],
    },
}


def get(keyword):
    """Return the format dict for a keyword, or None."""
    return FORMATS.get(keyword)


def keywords():
    """List all format keywords."""
    return list(FORMATS)
