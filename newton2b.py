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

# ---- right-panel geometry (x in [0.2, 6.9]) ----
T0 = np.array([2.4, 1.3, 0.0])
SD = np.array([0.8, -0.6, 0.0])     # slope direction (unit)
NM = np.array([0.6, 0.8, 0.0])      # outward normal (unit)
B0 = T0 + 4 * SD                    # (5.6, -1.1)
BACK = np.array([2.4, -1.1, 0.0])
PUL = np.array([2.05, 1.45, 0.0])
AC = np.array([4.19, 0.36, 0.0])    # block A centre
BC = np.array([2.05, -0.6, 0.0])    # block B centre

PANEL_CX = 3.55  # right-panel centre x for equations/options


def tline(parts, size=27):
    """One text line from [(text, color_or_None)]."""
    mob = VGroup(*[serif(t, size=size, color=c or WHITE) for t, c in parts])
    mob.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    return mob


def tblock(lines, size=27):
    """One explanation block: list of line part-lists, left aligned."""
    mob = VGroup(*[tline(p, size) for p in lines])
    mob.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    return mob


def arrow(s, e, color, w=6):
    return Arrow(np.array(s, dtype=float), np.array(e, dtype=float),
                 color=color, stroke_width=w, buff=0,
                 max_tip_length_to_length_ratio=0.25)


# ---------------- full explanation text (left panel) ----------------
BLOCKS = [
    # T1
    [[("Balok A (4 kg) di bidang miring 37$^\\circ$,", None)],
     [("dihubung tali via katrol ke balok B (6 kg).", None)]],
    # T2
    [[("Tegangan tali", BLUE), (" sama di kedua ujung.", None)]],
    # T3
    [[("B: berat ", None), ("60 N", W_RED), (" ke bawah,", None)],
     [("tegangan ", None), ("T", BLUE), (" ke atas.", None)]],
    # T4
    [[("A: ", None), ("40 N", W_RED), (" ke bawah,", None)],
     [("N", GREEN), (" tegak lurus, ", None), ("T", BLUE),
      (" ke atas bidang,", None)],
     [("24 N", ORANGE), (" ke bawah bidang.", None)]],
    # T5
    [[("Jumlahkan", YELLOW), (": 60 $-$ 24 = 10a,", None)],
     [("jadi ", None), ("a = 3,6 m/s$^2$.", YELLOW)]],
    # T6
    [[("Jawaban: (D)", YELLOW)]],
]


class NewtonSplit(Scene):
    def construct(self):
        # ============ beat 1: title (brief) ============
        title = serif(r"Hukum Newton: Katrol \& Bidang Miring", size=54)
        self.play(Write(title), run_time=1.5)
        self.wait(1.0)
        self.play(FadeOut(title, run_time=0.8))

        # ============ beat 2: full text left + setup right ============
        divider = Line([0, 3.8, 0], [0, -3.8, 0], color=GRAY,
                       stroke_width=2, stroke_opacity=0.4)
        blocks = [tblock(b) for b in BLOCKS]
        stack = VGroup(*blocks).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        stack.move_to([-6.85 + stack.width / 2, 3.0 - stack.height / 2, 0])
        for b in blocks:
            b.set_opacity(0.45)
        bars = [SurroundingRectangle(b, buff=0.12, color=YELLOW,
                                    fill_opacity=0.12, stroke_opacity=0)
                for b in blocks]

        # --- right-panel setup (no force arrows yet) ---
        slope = Line(T0, B0, color=WIRE, stroke_width=4)
        base = Line(B0, BACK, color=WIRE, stroke_width=4)
        back = Line(BACK, T0, color=GRAY, stroke_width=3)
        arc37 = Arc(radius=0.55, start_angle=np.radians(143),
                    angle=np.radians(37), arc_center=B0,
                    color=GOLD, stroke_width=4)
        lab37 = MathTex(r"37^\circ", font_size=30, color=GOLD)
        lab37.move_to(B0 + 0.9 * np.array(
            [np.cos(np.radians(161.5)), np.sin(np.radians(161.5)), 0.0]))
        rectA = Rectangle(width=0.9, height=0.55, color=WIRE,
                          stroke_width=4)
        rectA.rotate(-37 * DEGREES).move_to(AC)
        labA = VGroup(MathTex("A", font_size=36), serif("4 kg", size=24))
        labA.arrange(DOWN, buff=0.04).move_to(AC)
        pulley = Circle(radius=0.16, color=WIRE, stroke_width=4).move_to(PUL)
        PA = AC - 0.4 * SD
        s1 = Line(PA, PUL, color=GRAY, stroke_width=3)
        s2 = Line(PUL, np.array([BC[0], BC[1] + 0.425, 0.0]),
                  color=GRAY, stroke_width=3)
        rectB = Rectangle(width=0.7, height=0.85, color=WIRE,
                          stroke_width=4).move_to(BC)
        labB = VGroup(MathTex("B", font_size=36), serif("6 kg", size=24))
        labB.arrange(DOWN, buff=0.04).move_to(BC)

        self.play(Create(divider, run_time=0.6),
                  *[FadeIn(b, run_time=0.8) for b in blocks])
        self.wait(0.5)
        self.play(Create(slope, run_time=0.8), Create(base, run_time=0.8),
                  Create(back, run_time=0.8))
        self.play(Create(arc37, run_time=0.8), FadeIn(lab37, run_time=0.6))
        self.play(FadeIn(rectA, run_time=0.8), FadeIn(labA, run_time=0.8))
        self.play(Create(pulley, run_time=0.6))
        self.play(Create(s1, run_time=0.8), Create(s2, run_time=0.8))
        self.play(FadeIn(rectB, run_time=0.8), FadeIn(labB, run_time=0.8))
        self.wait(1.5)

        active = -1

        def activate(i):
            nonlocal active
            anims = []
            if active >= 0:
                anims += [FadeOut(bars[active], run_time=0.4),
                          blocks[active].animate.set_opacity(0.45)]
            anims += [FadeIn(bars[i], run_time=0.4),
                      blocks[i].animate.set_opacity(1.0)]
            self.play(*anims)
            self.bring_to_back(bars[i])
            active = i

        # ============ T1: the system ============
        activate(0)
        self.play(Indicate(rectA, run_time=1.0),
                  Indicate(rectB, run_time=1.0))
        self.wait(1.5)

        # ============ T2: tension keyword -> T labels ============
        activate(1)
        tS1 = MathTex("T", font_size=30, color=BLUE).move_to(
            (PA + PUL) / 2 + np.array([0.28, 0.2, 0.0]))
        tS2 = MathTex("T", font_size=30, color=BLUE).move_to(
            np.array([BC[0] + 0.32, (PUL[1] + BC[1]) / 2, 0.0]))
        self.play(FadeIn(tS1, run_time=0.8), FadeIn(tS2, run_time=0.8))
        self.wait(1.8)

        # ============ T3: block B forces + equation ============
        activate(2)
        wB = arrow([2.05, -1.05, 0], [2.05, -1.8, 0], W_RED)
        wB_lab = MathTex(r"60\ \text{N}", font_size=32, color=W_RED)
        wB_lab.move_to([2.58, -1.42, 0])
        tB = arrow([2.05, -0.1, 0], [2.05, 0.55, 0], BLUE)
        tB_lab = MathTex("T", font_size=34, color=BLUE)
        tB_lab.move_to([2.34, 0.22, 0])
        eqB = math("60", "-", "T", "= 6a", size=40)
        eqB[0].set_color(W_RED)
        eqB[2].set_color(BLUE)
        eqB.move_to([PANEL_CX, -2.3, 0])
        self.play(Create(wB, run_time=1.0), FadeIn(wB_lab, run_time=0.6))
        self.wait(0.8)
        self.play(FadeOut(tS2, run_time=0.5),
                  Create(tB, run_time=1.0), FadeIn(tB_lab, run_time=0.6))
        self.wait(0.8)
        self.play(Write(eqB), run_time=1.2)
        self.wait(1.5)

        # ============ T4: block A forces + equation ============
        activate(3)
        wA = arrow(AC + np.array([0, -0.4, 0]), AC + np.array([0, -1.2, 0]),
                   W_RED)
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
        eqA = math("T", "-", "24", "= 4a", size=40)
        eqA[0].set_color(BLUE)
        eqA[2].set_color(ORANGE)
        eqA.move_to([PANEL_CX, -2.95, 0])
        note24 = serif(r"$m_A g\sin37^\circ = 24$ N", size=26, color=GRAY)
        note24.move_to([PANEL_CX, -3.5, 0])

        self.play(Create(wA, run_time=1.0), FadeIn(wA_lab, run_time=0.6))
        self.wait(0.8)
        self.play(Create(nA, run_time=1.0), FadeIn(nA_lab, run_time=0.6))
        self.wait(0.8)
        self.play(FadeOut(tS1, run_time=0.5),
                  Create(tA, run_time=1.0), FadeIn(tA_lab, run_time=0.6))
        self.wait(0.8)
        self.play(Create(pA, run_time=1.0), FadeIn(pA_lab, run_time=0.6))
        self.wait(0.6)
        self.play(FadeIn(note24, run_time=0.8))
        self.wait(1.0)
        self.play(Write(eqA), run_time=1.2)
        self.wait(1.5)

        # ============ T5: merge -> answer ============
        activate(4)
        e_mid = math("60", "-", "24", "=", "10a", size=40)
        e_mid[0].set_color(W_RED)
        e_mid[2].set_color(ORANGE)
        e_mid.move_to([PANEL_CX, -2.6, 0])
        self.play(FadeOut(note24, run_time=0.5),
                  FadeTransform(VGroup(eqB, eqA), e_mid, run_time=1.2))
        self.wait(1.0)
        e_add = math("36", "=", "10a", size=42)
        e_add.move_to([PANEL_CX, -2.6, 0])
        self.play(FadeTransform(e_mid, e_add, run_time=1.0))
        self.wait(1.0)
        e_ans = math(r"a = 3{,}6\ \text{m/s}^2", size=52, color=YELLOW)
        e_ans.move_to([PANEL_CX, -2.6, 0])
        self.play(FadeTransform(e_add, e_ans, run_time=1.2))
        self.wait(2.0)

        # ============ T6: options, (D) boxed ============
        activate(5)
        opts = VGroup(*[MathTex(f"({L})\\ {v}", font_size=32)
                        for L, v in [("A", "2{,}0"), ("B", "2{,}4"),
                                      ("C", "3{,}0"), ("D", "3{,}6"),
                                      ("E", "4{,}8")]])
        opts.arrange(RIGHT, buff=0.4)
        opts.move_to([PANEL_CX, -2.7, 0])
        self.play(FadeOut(e_ans, run_time=0.6),
                  FadeIn(opts, run_time=1.0))
        self.wait(0.8)
        box = SurroundingRectangle(opts[3], color=YELLOW, buff=0.14,
                                   stroke_width=3)
        self.play(Create(box, run_time=0.8),
                  opts[3].animate.set_color(YELLOW), run_time=0.8)
        self.wait(3.0)
