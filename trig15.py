from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif, math
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

WIRE = "#D8D8D8"
TEAL = "#5ba5bc"       # unit circle (trig reference)
COS_RED = "#b86e64"    # cos (trig reference)
SIN_GREEN = "#91ad85"  # sin (trig reference)
GOLD = "#d4b84a"

R = 2.0
CX, CY = 2.4, -0.5

def pt(deg):
    t = np.radians(deg)
    return np.array([CX + R * np.cos(t), CY + R * np.sin(t), 0.0])


class Trig15(Scene):
    def construct(self):
        # ---------- Beat 1: title + problem ----------
        title = serif("Nilai Trigonometri Sudut Istimewa", size=52)
        prob = MathTex(r"\cos 210^\circ \cdot \sin 330^\circ - \cos 60^\circ"
                       r" = \dots", font_size=52)
        prob.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.0)
        self.play(Write(prob), run_time=1.0)
        self.wait(0.8)

        # ---------- Beat 2: unit circle + 210 deg, cos ----------
        header = serif("Lingkaran satuan", size=32)
        header.to_corner(UL, buff=0.55)
        x_ax = Line([CX - R - 0.7, CY, 0], [CX + R + 0.7, CY, 0],
                    color=GRAY, stroke_width=2)
        y_ax = Line([CX, CY - R - 0.7, 0], [CX, CY + R + 0.7, 0],
                    color=GRAY, stroke_width=2)
        circ = Circle(radius=R, color=TEAL, stroke_width=4).move_to([CX, CY, 0])
        self.play(
            FadeOut(title, run_time=0.7),
            FadeOut(prob, run_time=0.7),
            FadeIn(header, run_time=0.6),
            Create(x_ax, run_time=0.7),
            Create(y_ax, run_time=0.7),
            Create(circ, run_time=1.1),
        )

        P210 = pt(210)
        rad210 = Line([CX, CY, 0], P210, color=WIRE, stroke_width=3)
        arc210 = Arc(radius=0.55, start_angle=0, angle=np.radians(210),
                     arc_center=[CX, CY, 0], color=GOLD, stroke_width=4)
        lab210 = MathTex(r"210^\circ", font_size=30, color=GOLD)
        lab210.move_to(np.array([CX - 1.0, CY + 0.45, 0.0]))
        seg_cos = Line(P210, np.array([CX, P210[1], 0.0]),
                       color=COS_RED, stroke_width=6)
        val_cos = MathTex(r"\cos 210^\circ = -\frac{\sqrt{3}}{2}", font_size=34)
        val_cos.set_color_by_tex(r"\cos", COS_RED)
        val_cos.set_color_by_tex(r"-\frac{\sqrt{3}}{2}", COS_RED)
        val_cos.move_to(np.array([-3.9, 2.3, 0.0]))
        note210 = serif(r"$210^\circ = 180^\circ + 30^\circ$", size=26, color=GRAY)
        note210.next_to(val_cos, DOWN, aligned_edge=LEFT, buff=0.25)

        self.play(Create(rad210, run_time=0.7), Create(arc210, run_time=0.8),
                  FadeIn(lab210, run_time=0.5))
        self.play(Create(seg_cos, run_time=0.7), Write(val_cos), run_time=1.0)
        self.play(FadeIn(note210), run_time=0.6)
        self.wait(0.5)

        # ---------- Beat 3: 330 deg, sin ----------
        P330 = pt(330)
        rad330 = Line([CX, CY, 0], P330, color=WIRE, stroke_width=3)
        # small reference arc: 330 = 360 - 30
        arc330 = Arc(radius=0.55, start_angle=0, angle=np.radians(-30),
                     arc_center=[CX, CY, 0], color=GOLD, stroke_width=4)
        lab330 = MathTex(r"330^\circ", font_size=30, color=GOLD)
        lab330.move_to(np.array([CX + 2.0, CY - 1.15, 0.0]))
        lab30 = MathTex(r"30^\circ", font_size=26, color=GOLD)
        lab30.move_to(np.array([CX + 0.95, CY - 0.35, 0.0]))
        seg_sin = Line(P330, np.array([P330[0], CY, 0.0]),
                       color=SIN_GREEN, stroke_width=6)
        val_sin = MathTex(r"\sin 330^\circ = -\frac{1}{2}", font_size=34)
        val_sin.set_color_by_tex(r"\sin", SIN_GREEN)
        val_sin.set_color_by_tex(r"-\frac{1}{2}", SIN_GREEN)
        val_sin.next_to(note210, DOWN, aligned_edge=LEFT, buff=0.35)
        note330 = serif(r"$330^\circ = 360^\circ - 30^\circ$", size=26, color=GRAY)
        note330.next_to(val_sin, DOWN, aligned_edge=LEFT, buff=0.25)

        self.play(Create(rad330, run_time=0.7), Create(arc330, run_time=0.6),
                  FadeIn(lab330, run_time=0.5), FadeIn(lab30, run_time=0.5))
        self.play(Create(seg_sin, run_time=0.7), Write(val_sin), run_time=1.0)
        self.play(FadeIn(note330), run_time=0.6)
        self.wait(0.5)

        # ---------- Beat 4: compute (reuse the left column) ----------
        self.play(
            FadeOut(val_cos, run_time=0.6),
            FadeOut(note210, run_time=0.6),
            FadeOut(val_sin, run_time=0.6),
            FadeOut(note330, run_time=0.6),
        )
        e1a = MathTex(r"\cos 210^\circ \cdot \sin 330^\circ - \cos 60^\circ",
                      font_size=40)
        e1a.set_color_by_tex(r"\cos", COS_RED)
        e1a.set_color_by_tex(r"\sin", SIN_GREEN)
        e1a.move_to(np.array([-3.7, 2.3, 0.0]))
        e1b = MathTex(r"= ", r"-\frac{\sqrt{3}}{2}", r"\cdot ",
                      r"-\frac{1}{2}", r" - ", r"\frac{1}{2}", font_size=40)
        e1b[1].set_color(COS_RED)
        e1b[3].set_color(SIN_GREEN)
        e1b[5].set_color(COS_RED)
        e1b.next_to(e1a, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(Write(e1a), run_time=1.0)
        self.play(Write(e1b), run_time=1.2)

        e2 = MathTex(r"= \frac{\sqrt{3}}{4} - \frac{1}{2}", font_size=44)
        e2.next_to(e1b, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(Write(e2), run_time=1.0)

        e3 = MathTex(r"= \frac{\sqrt{3}-2}{4}", font_size=44)
        e3.next_to(e2, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(Write(e3), run_time=0.9)

        e4 = MathTex(r"= -\frac{1}{4}(2-\sqrt{3})", font_size=54)
        e4.set_color(YELLOW)
        e4.next_to(e3, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(e4), run_time=1.0)
        self.wait(0.8)

        # ---------- Beat 5: answer + options on a clean frame ----------
        self.play(
            FadeOut(e1a, run_time=0.7),
            FadeOut(e1b, run_time=0.7),
            FadeOut(e2, run_time=0.7),
            FadeOut(e3, run_time=0.7),
            FadeOut(circ, run_time=0.7),
            FadeOut(x_ax, run_time=0.7),
            FadeOut(y_ax, run_time=0.7),
            FadeOut(rad210, run_time=0.7),
            FadeOut(rad330, run_time=0.7),
            FadeOut(arc210, run_time=0.7),
            FadeOut(arc330, run_time=0.7),
            FadeOut(seg_cos, run_time=0.7),
            FadeOut(seg_sin, run_time=0.7),
            FadeOut(lab210, run_time=0.7),
            FadeOut(lab330, run_time=0.7),
            FadeOut(lab30, run_time=0.7),
            FadeOut(header, run_time=0.7),
            e4.animate.move_to(np.array([-2.2, 1.4, 0.0])),
            run_time=1.0,
        )
        opts = VGroup(
            MathTex(r"(A)\ \frac{3}{4}(2-\sqrt{3})", font_size=32),
            MathTex(r"(B)\ \frac{1}{4}(2-\sqrt{3})", font_size=32),
            MathTex(r"(C)\ 0", font_size=32),
            MathTex(r"(D)\ -\frac{3}{4}(2-\sqrt{3})", font_size=32),
            MathTex(r"(E)\ -\frac{1}{4}(2-\sqrt{3})", font_size=32),
        ).arrange(RIGHT, buff=0.45)
        opts.move_to(np.array([0.0, -1.6, 0.0]))
        self.play(FadeIn(opts, run_time=0.9))
        box = SurroundingRectangle(opts[4], color=YELLOW, buff=0.14,
                                   stroke_width=3)
        self.play(Create(box, run_time=0.7),
                  opts[4].animate.set_color(YELLOW), run_time=0.7)
        self.wait(2.0)
