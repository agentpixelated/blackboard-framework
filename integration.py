from manim import *
from visual_system import *
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.background_color = BG


def riemann_sum(n):
    dx = 2.0 / n
    xs = np.linspace(dx / 2, 2 - dx / 2, n)
    return float(np.sum(xs ** 2 * dx))


class Integration4(Scene):
    def construct(self):
        # ---------- Beat 1: title, serif on black ----------
        title = serif("Integration", size=84)
        subtitle = serif("the area under a curve", size=34, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=0.9)
        self.play(FadeIn(subtitle), run_time=0.7)
        self.wait(1.0)

        # ---------- Beat 2: the given curve ----------
        # FIX (audit: dead frame): axes start drawing AS the title leaves,
        # never an empty black frame.
        ax = thin_axes(
            x_range=[0, 2.6, 0.5], y_range=[0, 5, 1],
            x_length=7.6, y_length=4.6,
        ).shift(LEFT * 1.4 + DOWN * 0.35)
        self.play(
            FadeOut(title, run_time=0.7),
            FadeOut(subtitle, run_time=0.7),
            Create(ax, run_time=1.4),
        )

        graph = ax.plot(lambda x: x ** 2, x_range=[0, 2, 0.005],
                        color=CURVE, stroke_width=5)
        func_label = math(r"f(x) = x^2", size=38, color=GRAY)
        func_label.next_to(ax.c2p(1.62, 2.62), RIGHT, buff=0.25)
        self.play(Create(graph), run_time=1.2)
        self.play(Write(func_label), run_time=0.6)
        self.wait(0.3)

        # ---------- Beat 3: the question ----------
        # FIX (audit: blue absent): the area under the curve is the thing we
        # want -> it gets BLUE, the "look here" color, from the first sighting.
        area = ax.get_area(graph, x_range=[0, 2], color=BLUE, opacity=0.55)
        area.set_color_by_gradient(BLUE, "#2b6a7d")
        area_label = math(r"\text{area} = ?", size=46)
        area_label[0][-1].set_color(BLUE)  # the "?" is the current idea
        area_label.move_to(ax.c2p(1.0, 0.75))
        self.play(FadeIn(area), run_time=0.8)
        self.play(Write(area_label), run_time=0.6)
        self.wait(1.2)  # dwell on the question

        # ---------- Beat 4: chop into measurable pieces ----------
        def rects(n):
            return ax.get_riemann_rectangles(
                graph, x_range=[0, 2], dx=2.0 / n,
                input_sample_type="center",
                color=RECT_FILL, fill_opacity=0.9,
                stroke_color=RECT_EDGE, stroke_width=1,
            )

        sigma = math(r"\sum_{i=1}^{n}", r"f(x_i)", r"\Delta x", size=44)
        sigma[2].set_color(YELLOW)  # the piece width is the current idea
        n_text = math(r"n = 4", size=40, color=GRAY)
        # FIX (audit: color grammar): the running total IS the measured
        # quantity -> YELLOW for its whole life, per framework rule 4.2.
        total = DecimalNumber(riemann_sum(4), num_decimal_places=3,
                              font_size=40, color=YELLOW)
        approx = math(r"\approx", size=40, color=GRAY)
        approx.next_to(total, LEFT, buff=0.2)
        side = VGroup(sigma, n_text, VGroup(approx, total))
        side.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.to_edge(RIGHT, buff=1.0).shift(UP * 0.6)

        r = rects(4)
        self.play(
            FadeOut(area_label, run_time=0.4),
            FadeOut(area, run_time=0.4),
            FadeOut(func_label, run_time=0.4),
            FadeIn(r, run_time=0.8),
        )
        self.play(Write(sigma), run_time=0.8)
        self.play(FadeIn(n_text), FadeIn(approx), FadeIn(total), run_time=0.6)

        # highlight one piece: brighten one + DIM THE REST (framework 4.5)
        one = r[2]
        rest = VGroup(*[x for x in r if x is not one])
        piece_label = math(r"f(x_i)\,\Delta x", size=36, color=YELLOW)
        piece_label.next_to(ax.c2p(1.5, 0), DOWN, buff=0.55)
        arrow = Arrow(piece_label.get_top(), one.get_bottom(),
                      color=WHITE, stroke_width=3, buff=0.08)
        self.play(
            one.animate.set_color(YELLOW).set_opacity(0.9),
            rest.animate.set_opacity(0.25),
            run_time=0.7,
        )
        self.play(FadeIn(piece_label, shift=UP * 0.1),
                  Create(arrow), run_time=0.7)
        self.wait(0.8)
        self.play(
            FadeOut(piece_label), FadeOut(arrow),
            one.animate.set_color(RECT_FILL).set_opacity(0.9),
            rest.animate.set_opacity(0.9),
            run_time=0.6,
        )

        # ---------- Beat 5: more pieces, closer to truth ----------
        # FIX (audit: ghost glyphs): FadeTransform for number swaps, never
        # raw Transform on DecimalNumber.
        for n in (16, 64, 256):
            r2 = rects(n)
            n2 = math(rf"n = {n}", size=40, color=GRAY)
            n2.move_to(n_text, aligned_edge=LEFT)
            t2 = DecimalNumber(riemann_sum(n), num_decimal_places=3,
                               font_size=40, color=YELLOW)
            t2.next_to(approx, RIGHT, buff=0.2)
            self.play(
                FadeTransform(r, r2, run_time=1.0),
                FadeTransform(n_text, n2, run_time=1.0),
                FadeTransform(total, t2, run_time=1.0),
            )
            r, n_text, total = r2, n2, t2
            self.wait(0.5)

        # ---------- Beat 6: the symbol arrives late, as compression ----------
        integral = math(r"\int_{0}^{2}", r"x^2\,dx", size=72)
        integral[0].set_color(BLUE)
        integral.move_to(ORIGIN).shift(UP * 0.4)

        self.play(
            FadeOut(r, run_time=0.7), FadeOut(n_text, run_time=0.7),
            FadeOut(approx, run_time=0.7), FadeOut(total, run_time=0.7),
            FadeOut(graph, run_time=0.7), FadeOut(ax, run_time=0.7),
        )
        self.play(TransformMatchingTex(sigma, integral), run_time=1.4)
        self.wait(0.4)

        exact = math(r"=", r"\frac{8}{3}", size=72)
        exact[1].set_color(YELLOW)  # the payoff
        exact.next_to(integral, RIGHT, buff=0.35)
        self.play(Write(exact), run_time=1.0)
        self.play(
            VGroup(integral, exact).animate.move_to(ORIGIN).shift(UP * 0.4),
            run_time=0.6,
        )
        self.wait(1.2)

        # ---------- Beat 7: name the idea ----------
        punch = serif("the limit of Riemann sums, as $n \\to \\infty$",
                      size=32, color=GRAY)
        punch.next_to(VGroup(integral, exact), DOWN, buff=0.6)
        self.play(FadeIn(punch, shift=UP * 0.15), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(integral), FadeOut(exact), FadeOut(punch),
                  run_time=0.8)

        # ---------- Beat 8: resolve ----------
        outro = serif("That's integration.", size=54)
        self.play(FadeIn(outro, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)
        self.play(FadeOut(outro), run_time=0.9)
