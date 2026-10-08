from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif, math
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

WIRE = "#D8D8D8"
W_RED = "#b86e64"    # weight
ORANGE = "#bf7f49"   # downhill component
GOLD = "#d4b84a"

# ---- geometry ----
T0 = np.array([0.8, 1.3, 0.0])
SD = np.array([0.8, -0.6, 0.0])     # slope direction (unit)
NM = np.array([0.6, 0.8, 0.0])      # outward normal (unit)
B0 = T0 + 4 * SD                    # slope foot (4.0, -1.1)
BACK = np.array([0.8, -1.1, 0.0])
PUL = np.array([0.45, 1.45, 0.0])
AC = np.array([2.59, 0.36, 0.0])    # block A centre
BC = np.array([0.45, -0.6, 0.0])   # block B centre


def leftcol(mob, y):
    """Left-align a mobject in the equation column."""
    mob.to_edge(LEFT, buff=0.7)
    mob.move_to([mob.get_center()[0], y, 0.0])
    return mob


def arrow(s, e, color, w=6):
    return Arrow(np.array(s, dtype=float), np.array(e, dtype=float),
                 color=color, stroke_width=w, buff=0,
                 max_tip_length_to_length_ratio=0.25)


def kwcap(parts, y=3.55, x=0.5):
    """Keyword caption: parts = [(text, color_or_None), ...].
    The keyword (colored) appears first, then its visual follows."""
    mob = VGroup(*[serif(t, size=32, color=c or WHITE) for t, c in parts])
    mob.arrange(RIGHT, buff=0.18)
    mob.move_to([x, y, 0.0])
    return mob


class NewtonPulley(Scene):
    def construct(self):
        # ============ Beat 1: title + problem ============
        title = serif(r"Hukum Newton: Katrol \& Bidang Miring", size=54)
        p1 = serif(r"Balok $A$ ($4$ kg) di atas bidang miring licin $37^\circ$,",
                   size=30, color=GRAY)
        p2 = serif(r"dihubungkan tali melalui katrol ke balok $B$ ($6$ kg)"
                   r" yang tergantung.", size=30, color=GRAY)
        p3 = serif(r"$g = 10$ m/s$^2$, $\sin37^\circ = 0{,}6$."
                   r" Berapa percepatan sistem?", size=30, color=GRAY)
        p1.next_to(title, DOWN, buff=0.4)
        p2.next_to(p1, DOWN, buff=0.2)
        p3.next_to(p2, DOWN, buff=0.2)
        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(p3), run_time=1.4)
        self.wait(3.0)

        # ============ Beat 2: draw the setup, slowly ============
        slope = Line(T0, B0, color=WIRE, stroke_width=4)
        base = Line(B0, BACK, color=WIRE, stroke_width=4)
        back = Line(BACK, T0, color=GRAY, stroke_width=3)
        arc37 = Arc(radius=0.55, start_angle=np.radians(143),
                    angle=np.radians(37), arc_center=B0,
                    color=GOLD, stroke_width=4)
        lab37 = MathTex(r"37^\circ", font_size=30, color=GOLD)
        lab37.move_to(B0 + 0.9 * np.array(
            [np.cos(np.radians(161.5)), np.sin(np.radians(161.5)), 0.0]))

        rectA = Rectangle(width=0.9, height=0.55, color=WIRE, stroke_width=4)
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

        self.play(FadeOut(title, run_time=1.0), FadeOut(p1, run_time=1.0),
                  FadeOut(p2, run_time=1.0), FadeOut(p3, run_time=1.0))
        self.play(Create(slope, run_time=1.0), Create(base, run_time=1.0),
                  Create(back, run_time=1.0))
        self.play(Create(arc37, run_time=1.0), FadeIn(lab37, run_time=0.8))
        self.wait(0.8)
        self.play(FadeIn(rectA, run_time=1.0), FadeIn(labA, run_time=1.0))
        self.wait(0.8)
        self.play(Create(pulley, run_time=0.8))
        self.wait(0.5)
        self.play(Create(s1, run_time=1.0), Create(s2, run_time=1.0))
        self.wait(0.5)
        self.play(FadeIn(rectB, run_time=1.0), FadeIn(labB, run_time=1.0))
        self.wait(2.5)

        # ============ Beat 3: keyword -> visual (tension) ============
        kwT = kwcap([("Tegangan tali", BLUE), (" sama di kedua ujung.", None)])
        self.play(FadeIn(kwT, run_time=1.0))
        self.wait(0.8)
        tS1 = MathTex("T", font_size=30, color=BLUE).move_to(
            (PA + PUL) / 2 + np.array([0.28, 0.2, 0.0]))
        tS2 = MathTex("T", font_size=30, color=BLUE).move_to(
            np.array([BC[0] + 0.32, (PUL[1] + BC[1]) / 2, 0.0]))
        self.play(FadeIn(tS1, run_time=0.8), FadeIn(tS2, run_time=0.8))
        self.wait(1.8)

        # ============ Beat 4: free-body diagram of B ============
        wB = arrow([0.45, -1.05, 0], [0.45, -1.8, 0], W_RED)
        wB_lab = MathTex(r"60\ \text{N}", font_size=32, color=W_RED)
        wB_lab.move_to([0.98, -1.42, 0])
        tB = arrow([0.45, -0.1, 0], [0.45, 0.55, 0], BLUE)
        tB_lab = MathTex("T", font_size=34, color=BLUE)
        tB_lab.move_to([0.74, 0.22, 0])

        rowB = VGroup(serif("B:", size=34, color=GRAY),
                      MathTex(r"60", r" - ", r"T", r" = 6a", font_size=42))
        rowB[1][0].set_color(W_RED)
        rowB[1][2].set_color(BLUE)
        rowB.arrange(RIGHT, buff=0.25)
        leftcol(rowB, 2.3)

        kwB1 = kwcap([("Berat ", None), ("60 N", W_RED), (" ke bawah", None)])
        self.play(FadeOut(kwT, run_time=0.6), FadeOut(tS1, run_time=0.6),
                  FadeOut(tS2, run_time=0.6), FadeIn(kwB1, run_time=0.8))
        self.wait(0.6)
        self.play(Create(wB, run_time=1.2), FadeIn(wB_lab, run_time=0.8))
        self.wait(1.0)
        kwB2 = kwcap([("Tegangan ", None), ("T", BLUE), (" ke atas", None)])
        self.play(FadeOut(kwB1, run_time=0.6), FadeIn(kwB2, run_time=0.8))
        self.wait(0.6)
        self.play(Create(tB, run_time=1.2), FadeIn(tB_lab, run_time=0.8))
        self.wait(1.0)
        self.play(FadeOut(kwB2, run_time=0.6), Write(rowB, run_time=1.6))
        self.wait(2.0)

        # ============ Beat 5: free-body diagram of A ============
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

        note24 = serif(r"$m_A g\sin37^\circ = 4\cdot10\cdot0{,}6 = 24$ N",
                       size=27, color=GRAY)
        leftcol(note24, 0.55)

        rowA = VGroup(serif("A:", size=34, color=GRAY),
                      MathTex(r"T", r" - ", r"24", r" = 4a", font_size=42))
        rowA[1][0].set_color(BLUE)
        rowA[1][2].set_color(ORANGE)
        rowA.arrange(RIGHT, buff=0.25)
        leftcol(rowA, 1.4)

        kwA1 = kwcap([("Berat ", None), ("40 N", W_RED), (" ke bawah", None)])
        self.play(FadeIn(kwA1, run_time=0.8))
        self.wait(0.6)
        self.play(Create(wA, run_time=1.2), FadeIn(wA_lab, run_time=0.8))
        self.wait(1.0)
        kwA2 = kwcap([("Normal ", None), ("N", GREEN), (" tegak lurus bidang", None)])
        self.play(FadeOut(kwA1, run_time=0.6), FadeIn(kwA2, run_time=0.8))
        self.wait(0.6)
        self.play(Create(nA, run_time=1.2), FadeIn(nA_lab, run_time=0.8))
        self.wait(1.0)
        kwA3 = kwcap([("Tegangan ", None), ("T", BLUE), (" ke atas bidang", None)])
        self.play(FadeOut(kwA2, run_time=0.6), FadeIn(kwA3, run_time=0.8))
        self.wait(0.6)
        self.play(Create(tA, run_time=1.2), FadeIn(tA_lab, run_time=0.8))
        self.wait(1.0)
        kwA4 = kwcap([("Komponen berat ", None), ("24 N", ORANGE),
                      (" ke bawah bidang", None)])
        self.play(FadeOut(kwA3, run_time=0.6), FadeIn(kwA4, run_time=0.8))
        self.wait(0.6)
        self.play(Create(pA, run_time=1.4), FadeIn(pA_lab, run_time=0.8))
        self.wait(0.8)
        self.play(FadeIn(note24, run_time=1.0))
        self.wait(1.5)
        self.play(FadeOut(kwA4, run_time=0.6), Write(rowA, run_time=1.6))
        self.wait(2.0)

        # ============ Beat 6: add the equations ============
        e_mid = MathTex(r"60 - 24 = 6a + 4a", font_size=42)
        e_mid.set_color_by_tex("60", W_RED)
        e_mid.set_color_by_tex("24", ORANGE)
        leftcol(e_mid, 0.55)
        e_add = MathTex(r"36 = 10a", font_size=44)
        leftcol(e_add, -0.35)
        e_ans = MathTex(r"a = 3{,}6\ \text{m/s}^2", font_size=54, color=YELLOW)
        leftcol(e_ans, -1.45)
        intu = serif(r"selisih gaya $\div$ massa total", size=28, color=GRAY)
        leftcol(intu, -2.35)

        kwAdd = kwcap([("Jumlahkan", YELLOW), (" — T saling menghapus.", None)])
        self.play(FadeIn(kwAdd, run_time=0.8))
        self.wait(0.8)
        self.play(FadeOut(note24, run_time=0.8), FadeOut(kwAdd, run_time=0.8),
                  Write(e_mid, run_time=1.4))
        self.wait(1.2)
        self.play(Write(e_add, run_time=1.4))
        self.wait(1.2)
        self.play(Write(e_ans, run_time=1.6))
        self.wait(2.0)
        self.play(FadeIn(intu, run_time=1.2))
        self.wait(3.0)

        # ============ Beat 7: motion demo ============
        aB = arrow([1.15, -0.35, 0], [1.15, -1.05, 0], YELLOW, w=5)
        aB_lab = MathTex("a", font_size=32, color=YELLOW)
        aB_lab.move_to([1.44, -0.7, 0])
        aA_s = AC + np.array([0.76, -0.46, 0])
        aA = arrow(aA_s, aA_s - 0.7 * SD, YELLOW, w=5)
        aA_lab = MathTex("a", font_size=32, color=YELLOW)
        aA_lab.move_to(aA_s + np.array([0.25, 0.05, 0]))
        cap = serif(r"$A$ ke atas, $B$ ke bawah --- satu sistem, satu $a$.",
                    size=30)
        cap.move_to([0.0, -3.3, 0.0])

        self.play(
            *[FadeOut(m, run_time=1.2) for m in
              [wB, wB_lab, tB, tB_lab, wA, wA_lab, nA, nA_lab,
               tA, tA_lab, pA, pA_lab]],
            FadeIn(aB, run_time=1.2), FadeIn(aB_lab, run_time=1.2),
            FadeIn(aA, run_time=1.2), FadeIn(aA_lab, run_time=1.2),
            FadeIn(cap, run_time=1.2),
        )
        self.wait(3.5)

        # ============ Beat 8: options, answer (D) ============
        self.play(FadeOut(aB, run_time=0.8), FadeOut(aB_lab, run_time=0.8),
                  FadeOut(aA, run_time=0.8), FadeOut(aA_lab, run_time=0.8),
                  FadeOut(cap, run_time=0.8))
        opts = VGroup(*[MathTex(f"({L})\\ {v}", font_size=34)
                        for L, v in [("A", "2{,}0"), ("B", "2{,}4"),
                                      ("C", "3{,}0"), ("D", "3{,}6"),
                                      ("E", "4{,}8")]])
        opts.arrange(RIGHT, buff=0.45)
        unit = MathTex(r"\text{m/s}^2", font_size=30, color=GRAY)
        orow = VGroup(opts, unit).arrange(RIGHT, buff=0.3)
        orow.move_to([-0.5, -3.3, 0.0])
        self.play(FadeIn(orow, run_time=1.4))
        self.wait(0.8)
        box = SurroundingRectangle(opts[3], color=YELLOW, buff=0.14,
                                   stroke_width=3)
        self.play(Create(box, run_time=1.0),
                  opts[3].animate.set_color(YELLOW), run_time=1.0)
        self.wait(4.0)
