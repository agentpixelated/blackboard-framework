from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif, math
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

WIRE = "#D8D8D8"
R = 2.5
CX, CY = 1.9, -0.4

def pt(t):
    return np.array([CX + R * np.cos(t), CY + R * np.sin(t), 0.0])


class EulerIdentity(Scene):
    def construct(self):
        # ---------- Beat 1: title + the identity ----------
        title = serif("Euler's Identity", size=60)
        ident = MathTex(r"e^{i\pi} + 1 = 0", font_size=64)
        ident.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.0)
        self.play(Write(ident), run_time=1.0)
        q = serif("Mengapa ini benar?", size=30, color=GRAY)
        q.next_to(ident, DOWN, buff=0.35)
        self.play(FadeIn(q), run_time=0.6)
        self.wait(0.8)

        # ---------- Beat 2: e^(ix) as a point on the unit circle ----------
        header = serif(r"Pandang $e^{ix}$ sebagai titik di bidang kompleks", size=30)
        header.to_corner(UL, buff=0.55)
        re_ax = Line([CX - R - 0.8, CY, 0], [CX + R + 0.8, CY, 0],
                     color=GRAY, stroke_width=2)
        im_ax = Line([CX, CY - R - 0.8, 0], [CX, CY + R + 0.8, 0],
                     color=GRAY, stroke_width=2)
        circ = Circle(radius=R, color=WIRE, stroke_width=4).move_to([CX, CY, 0])
        l1 = MathTex("1", font_size=28).move_to([CX + R + 0.35, CY, 0])
        li = MathTex("i", font_size=28).move_to([CX, CY + R + 0.35, 0])
        lm1 = MathTex("-1", font_size=28).move_to([CX - R - 0.42, CY, 0])
        lmi = MathTex("-i", font_size=28).move_to([CX, CY - R - 0.42, 0])
        lre = serif("Re", size=24, color=GRAY).move_to([CX + R + 0.9, CY - 0.38, 0])
        lim = serif("Im", size=24, color=GRAY).move_to([CX + 0.38, CY + R + 0.9, 0])

        self.play(
            FadeOut(title, run_time=0.7),
            FadeOut(ident, run_time=0.7),
            FadeOut(q, run_time=0.7),
            FadeIn(header, run_time=0.6),
            Create(re_ax, run_time=0.8),
            Create(im_ax, run_time=0.8),
            Create(circ, run_time=1.2),
        )
        self.play(LaggedStart(FadeIn(l1), FadeIn(li), FadeIn(lm1), FadeIn(lmi),
                              FadeIn(lre), FadeIn(lim), lag_ratio=0.08),
                  run_time=1.0)

        x = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(pt(x.get_value()), color=YELLOW, radius=0.13))
        rad = always_redraw(lambda: Line([CX, CY, 0], pt(x.get_value()),
                                         color=GRAY, stroke_width=2, stroke_opacity=0.6))
        trail = TracedPath(dot.get_center, stroke_color=YELLOW, stroke_width=5)
        arc = always_redraw(lambda: Arc(radius=0.6, start_angle=0,
                                        angle=x.get_value(), arc_center=[CX, CY, 0],
                                        color=WHITE, stroke_width=3, stroke_opacity=0.7))

        t0 = serif(r"Mulai di $x=0$: $e^0 = 1$", size=28)
        t0.move_to(np.array([-3.9, 2.45, 0.0]))
        self.play(FadeIn(dot), FadeIn(rad), FadeIn(t0), run_time=0.9)
        self.wait(0.5)

        # ---------- Beat 3: the derivative insight ----------
        eqd = MathTex(r"\frac{d}{dx}e^{ix} = ", r"i", r"e^{ix}", font_size=44)
        eqd[1].set_color(BLUE)
        eqd.next_to(t0, DOWN, aligned_edge=LEFT, buff=0.4)
        tm = MathTex(r"|e^{ix}| = 1", font_size=40)
        tm.next_to(eqd, DOWN, aligned_edge=LEFT, buff=0.35)
        t1a = serif(r"Dikali $i$ = diputar $90^\circ$", size=28)
        t1a.next_to(tm, DOWN, aligned_edge=LEFT, buff=0.4)
        t1b = serif(r"$v \perp$ posisi, $|v|=1$ $\Rightarrow$ melingkar", size=28)
        t1b.next_to(t1a, DOWN, aligned_edge=LEFT, buff=0.25)
        t1 = VGroup(t1a, t1b)

        def vel_arrow():
            t = x.get_value()
            p = pt(t)
            d = np.array([-np.sin(t), np.cos(t), 0.0])
            return Arrow(p, p + 0.95 * d, color=BLUE, stroke_width=6, buff=0.1,
                         max_tip_length_to_length_ratio=0.28)
        vel = always_redraw(vel_arrow)

        self.play(Write(eqd), run_time=1.0)
        self.play(FadeIn(tm), run_time=0.7)
        # always_redraw / TracedPath mobjects can't be FadeIn'd — add directly
        self.add(vel, arc, trail)
        self.play(FadeIn(t1), run_time=1.0)
        self.wait(0.6)

        # ---------- Beat 4: walk a distance of pi ----------
        t2 = serif(r"Berjalan sejauh $\pi$ \dots", size=28)
        t2.next_to(t1, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(FadeIn(t2), run_time=0.7)
        self.play(x.animate.set_value(np.pi), run_time=7, rate_func=linear)
        self.wait(0.5)

        # ---------- Beat 5: land on -1 ----------
        plab = MathTex(r"\pi", font_size=36, color=WHITE)
        plab.move_to(np.array([CX, CY + 1.05, 0.0]))
        self.play(FadeIn(plab), lm1.animate.set_color(YELLOW), run_time=0.8)
        t3 = serif(r"$\frac{1}{2}$ keliling $\Rightarrow$ tiba di $-1$", size=28)
        t3.next_to(t2, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(FadeIn(t3), run_time=0.8)

        eq1 = MathTex(r"e^{i\pi} = -1", font_size=52)
        eq1.next_to(t3, DOWN, aligned_edge=LEFT, buff=0.45)
        self.play(Write(eq1), run_time=1.0)
        self.wait(0.5)

        eq2 = MathTex(r"e^{i\pi} + 1 = 0", font_size=60)
        eq2.move_to(eq1, aligned_edge=LEFT)
        self.play(FadeTransform(eq1, eq2), run_time=1.1)
        box = SurroundingRectangle(eq2, color=YELLOW, buff=0.22, stroke_width=3)
        self.play(Create(box), run_time=0.8)
        self.wait(2.0)
