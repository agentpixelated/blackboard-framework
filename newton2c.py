from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif, math
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

W_RED = "#b86e64"     # weight
ORANGE = "#bf7f49"    # downhill component
WIRE = "#D8D8D8"
GOLD = "#d4b84a"

# ---- right-panel geometry (from newton2b) ----
T0 = np.array([2.4, 1.3, 0.0])
SD = np.array([0.8, -0.6, 0.0])     # slope direction (unit)
NM = np.array([0.6, 0.8, 0.0])      # outward normal (unit)
B0 = T0 + 4 * SD                    # (5.6, -1.1)
BACK = np.array([2.4, -1.1, 0.0])
PUL = np.array([2.05, 1.45, 0.0])
AC = np.array([4.19, 0.36, 0.0])    # block A centre
BC = np.array([2.05, -0.6, 0.0])    # block B centre
PA = AC - 0.4 * SD
PANEL_CX = 3.55


def arrow(s, e, color, w=6):
    return Arrow(np.array(s, dtype=float), np.array(e, dtype=float),
                 color=color, stroke_width=w, buff=0,
                 max_tip_length_to_length_ratio=0.25)


def kline(specs, font_size=26):
    """One problem-text line from [(text, kwid_or_None)].
    Returns (VGroup, {kwid: submobject}) — keywords are directly
    addressable, no string matching needed."""
    mob = VGroup()
    kwmap = {}
    for text, kwid in specs:
        t = Tex(text, font_size=font_size)
        mob.add(t)
        if kwid:
            kwmap[kwid] = t
    mob.arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
    return mob, kwmap


class NewtonFormat5(Scene):
    def construct(self):
        divider = Line([0, 3.8, 0], [0, -3.8, 0], color=GRAY,
                       stroke_width=2, stroke_opacity=0.4)
        self.play(Create(divider, run_time=0.6))

        # ============ PHASE A: problem verbatim, right empty ============
        spec_lines = [
            [("Balok A", "bA"), ("(4 kg)", "m4"), ("berada di atas", None)],
            [("bidang miring", "bm"), ("licin bersudut", None),
             (r"$37^\circ$", "t37"), ("dan", None)],
            [("dihubungkan dengan", None), ("tali", "tali"),
             ("melalui", None)],
            [("katrol", "katrol"), ("licin ke", None), ("balok B", "bB"),
             ("(6 kg)", "m6")],
            [("yang tergantung vertikal. Jika", None)],
            [(r"$g = 10$ m/s$^2$ dan", None),
             (r"$\sin 37^\circ = 0{,}6$,", None)],
            [("percepatan sistem", "ps"), (r"balok adalah \dots", None)],
        ]
        built = [kline(s) for s in spec_lines]
        plines = VGroup(*[b[0] for b in built])
        KW = {}
        for b in built:
            KW.update(b[1])
        plines.arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        plines.move_to([-6.8 + plines.width / 2, 1.0, 0])

        vis_cap = serif("Visualisasi", size=24, color=GRAY)
        vis_cap.move_to([PANEL_CX, 3.3, 0])

        self.play(FadeIn(plines, run_time=1.2),
                  FadeIn(vis_cap, run_time=0.8))
        self.wait(2.0)

        def mark(kwid, color):
            """Mark keyword in place: recolor + surrounding box."""
            m = KW[kwid]
            m.set_color(color)
            return SurroundingRectangle(m, color=color, buff=0.05,
                                        stroke_width=2.5)

        # ============ PHASE B: keyword -> visual, one element/beat ====
        # B1: "bidang miring" -> wedge
        b_bm = mark("bm", WHITE)
        self.play(FadeIn(b_bm, run_time=0.6))
        self.wait(0.6)
        slope = Line(T0, B0, color=WIRE, stroke_width=4)
        base = Line(B0, BACK, color=WIRE, stroke_width=4)
        back = Line(BACK, T0, color=GRAY, stroke_width=3)
        self.play(Create(slope, run_time=0.8), Create(base, run_time=0.8),
                  Create(back, run_time=0.8))
        self.wait(1.0)

        # B2: "37°" -> angle arc
        b_t37 = mark("t37", GOLD)
        self.play(FadeIn(b_t37, run_time=0.6))
        self.wait(0.6)
        arc37 = Arc(radius=0.55, start_angle=np.radians(143),
                    angle=np.radians(37), arc_center=B0,
                    color=GOLD, stroke_width=4)
        lab37 = MathTex(r"37^\circ", font_size=30, color=GOLD)
        lab37.move_to(B0 + 0.9 * np.array(
            [np.cos(np.radians(161.5)), np.sin(np.radians(161.5)), 0.0]))
        self.play(Create(arc37, run_time=0.8), FadeIn(lab37, run_time=0.6))
        self.wait(1.0)

        # B3: "Balok A (4 kg)" -> block A
        b_bA = mark("bA", WHITE)
        b_m4 = mark("m4", GOLD)
        self.play(FadeIn(b_bA, run_time=0.5), FadeIn(b_m4, run_time=0.5))
        self.wait(0.6)
        rectA = Rectangle(width=0.9, height=0.55, color=WIRE, stroke_width=4)
        rectA.rotate(-37 * DEGREES).move_to(AC)
        labA = VGroup(MathTex("A", font_size=36), serif("4 kg", size=24))
        labA.arrange(DOWN, buff=0.04).move_to(AC)
        self.play(FadeIn(rectA, run_time=0.8), FadeIn(labA, run_time=0.8))
        self.wait(1.0)

        # B4: "katrol" -> pulley (concept BLUE)
        b_kat = mark("katrol", BLUE)
        self.play(FadeIn(b_kat, run_time=0.6))
        self.wait(0.6)
        pulley = Circle(radius=0.16, color=BLUE, stroke_width=4).move_to(PUL)
        self.play(Create(pulley, run_time=0.8))
        self.wait(1.0)

        # B5: "tali" -> strings (concept BLUE)
        b_tali = mark("tali", BLUE)
        self.play(FadeIn(b_tali, run_time=0.6))
        self.wait(0.6)
        s1 = Line(PA, PUL, color=BLUE, stroke_width=3)
        s2 = Line(PUL, np.array([BC[0], BC[1] + 0.425, 0.0]),
                  color=BLUE, stroke_width=3)
        self.play(Create(s1, run_time=0.8), Create(s2, run_time=0.8))
        self.wait(1.0)

        # B6: "balok B (6 kg)" -> block B
        b_bB = mark("bB", WHITE)
        b_m6 = mark("m6", GOLD)
        self.play(FadeIn(b_bB, run_time=0.5), FadeIn(b_m6, run_time=0.5))
        self.wait(0.6)
        rectB = Rectangle(width=0.7, height=0.85, color=WIRE,
                          stroke_width=4).move_to(BC)
        labB = VGroup(MathTex("B", font_size=36), serif("6 kg", size=24))
        labB.arrange(DOWN, buff=0.04).move_to(BC)
        self.play(FadeIn(rectB, run_time=0.8), FadeIn(labB, run_time=0.8))
        self.wait(1.0)

        # B7: "percepatan sistem" -> a = ?
        b_ps = mark("ps", YELLOW)
        self.play(FadeIn(b_ps, run_time=0.6))
        self.wait(0.6)
        aq = MathTex(r"a = ?", font_size=40, color=YELLOW)
        aq.move_to([PANEL_CX, -2.4, 0])
        self.play(FadeIn(aq, run_time=0.8))
        self.wait(1.5)

        # ============ PHASE C: strip to givens ============
        boxes = [b_bm, b_t37, b_bA, b_m4, b_kat, b_tali, b_bB, b_m6, b_ps]
        self.play(FadeOut(plines, run_time=0.8),
                  *[FadeOut(bx, run_time=0.8) for bx in boxes],
                  FadeOut(aq, run_time=0.8))
        self.wait(0.5)
        dik = VGroup(
            serif("Diketahui:", size=30, color=GRAY),
            MathTex(r"m_A = 4\ \text{kg}", font_size=30),
            MathTex(r"m_B = 6\ \text{kg}", font_size=30),
            MathTex(r"\theta = 37^\circ", font_size=30),
            MathTex(r"\sin 37^\circ = 0{,}6", font_size=30),
            MathTex(r"g = 10\ \text{m/s}^2", font_size=30),
            MathTex(r"\text{Ditanya: } a = ?", font_size=30),
        )
        dik.arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        dik.move_to([-6.8 + dik.width / 2, 2.0, 0])
        self.play(FadeIn(dik, run_time=1.0))
        self.wait(1.2)

        # ============ PHASE D: solve step by step ============
        def lefteq(mob, y):
            mob.move_to([-6.8 + mob.width / 2, y, 0])
            return mob

        # D1: block B equation + force arrows
        d1 = VGroup(serif("Balok B: ", size=30, color=GRAY),
                    math("60", "-", "T", "= 6a", size=38))
        d1[1][0].set_color(W_RED)
        d1[1][2].set_color(BLUE)
        d1.arrange(RIGHT, buff=0.2)
        lefteq(d1, -0.9)
        wB = arrow([2.05, -1.05, 0], [2.05, -1.8, 0], W_RED)
        wB_lab = MathTex(r"60\ \text{N}", font_size=32, color=W_RED)
        wB_lab.move_to([2.58, -1.42, 0])
        tB = arrow([2.05, -0.1, 0], [2.05, 0.55, 0], BLUE)
        tB_lab = MathTex("T", font_size=34, color=BLUE)
        tB_lab.move_to([2.34, 0.22, 0])
        self.play(Write(d1, run_time=1.2))
        self.wait(0.6)
        self.play(Create(wB, run_time=1.0), FadeIn(wB_lab, run_time=0.6))
        self.wait(0.6)
        self.play(Create(tB, run_time=1.0), FadeIn(tB_lab, run_time=0.6))
        self.wait(1.2)

        # D2: block A equation + force arrows
        d2 = VGroup(serif("Balok A: ", size=30, color=GRAY),
                    math("T", "-", "24", "= 4a", size=38))
        d2[1][0].set_color(BLUE)
        d2[1][2].set_color(ORANGE)
        d2.arrange(RIGHT, buff=0.2)
        lefteq(d2, -1.7)
        wA = arrow(AC + np.array([0, -0.4, 0]),
                   AC + np.array([0, -1.2, 0]), W_RED)
        wA_lab = MathTex(r"40\ \text{N}", font_size=32, color=W_RED)
        wA_lab.move_to(AC + np.array([-0.54, -1.11, 0]))
        nA = arrow(AC + 0.45 * NM, AC + 1.15 * NM, GREEN)
        nA_lab = MathTex("N", font_size=34, color=GREEN)
        nA_lab.move_to(AC + 1.35 * NM + np.array([0.12, 0.08, 0]))
        tA = arrow(AC - 0.35 * SD, AC - 1.05 * SD, BLUE)
        tA_lab = MathTex("T", font_size=34, color=BLUE)
        tA_lab.move_to(AC - 1.25 * SD + np.array([-0.12, 0.06, 0]))
        pA = DashedLine(AC + 0.35 * SD, AC + 1.05 * SD, color=ORANGE,
                        stroke_width=5, dash_length=0.12)
        pA_lab = MathTex(r"24\ \text{N}", font_size=32, color=ORANGE)
        pA_lab.move_to(AC + 1.05 * SD + np.array([0.28, -0.08, 0]))
        self.play(Write(d2, run_time=1.2))
        self.wait(0.6)
        self.play(Create(wA, run_time=1.0), FadeIn(wA_lab, run_time=0.6))
        self.wait(0.6)
        self.play(Create(nA, run_time=1.0), FadeIn(nA_lab, run_time=0.6))
        self.wait(0.6)
        self.play(Create(tA, run_time=1.0), FadeIn(tA_lab, run_time=0.6))
        self.wait(0.6)
        self.play(Create(pA, run_time=1.0), FadeIn(pA_lab, run_time=0.6))
        self.wait(1.2)

        # D3: merge -> answer
        d3 = math("36", "=", "10a", size=40)
        lefteq(d3, -2.6)
        self.play(FadeTransform(VGroup(d1[1], d2[1]), d3, run_time=1.2))
        self.wait(1.0)
        dans = math(r"a = 3{,}6\ \text{m/s}^2", size=48, color=YELLOW)
        lefteq(dans, -2.6)
        self.play(FadeTransform(d3, dans, run_time=1.2))
        self.wait(1.5)

        # D4: options, (D) boxed
        opts = VGroup(*[MathTex(f"({L})\\ {v}", font_size=28)
                        for L, v in [("A", "2{,}0"), ("B", "2{,}4"),
                                      ("C", "3{,}0"), ("D", "3{,}6"),
                                      ("E", "4{,}8")]])
        opts.arrange(RIGHT, buff=0.3)
        opts.move_to([PANEL_CX, -2.9, 0])
        self.play(FadeIn(opts, run_time=1.0))
        self.wait(0.8)
        box = SurroundingRectangle(opts[3], color=YELLOW, buff=0.14,
                                   stroke_width=3)
        self.play(Create(box, run_time=0.8),
                  opts[3].animate.set_color(YELLOW), run_time=0.8)
        self.wait(3.0)
