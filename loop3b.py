"""Loop-the-loop, split-screen remake (v2).

LEFT  (x in [-6.9,-0.2]): full explanation text, 6 blocks, all visible
      from beat 2. Active block = opacity 1 + yellow highlight bar.
RIGHT (x in [ 0.2, 6.9]): track/loop/ball visualization + equations.
Sync rule: text block highlighted FIRST, then its visual appears.
"""
from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif, math
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

WIRE = "#D8D8D8"
TEAL = "#5ba5bc"
REDW = "#b86e64"   # weight


def TL(s, size=27):
    """One left-aligned text line (single Tex; colors via \\textcolor)."""
    return Tex(s, font_size=size, color=WHITE, tex_template=TEX_TPL)


TEX_TPL = TexTemplate()
TEX_TPL.add_to_preamble(r"\usepackage{xcolor}")


def tblock(lines):
    blk = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    return blk


class LoopSplit(Scene):
    def construct(self):
        # ================= right-panel geometry =================
        Cx, Cy = 3.7, -1.0
        R = 1.5
        P0 = np.array([0.9, 2.0])          # release point (top of incline)
        C = np.array([Cx, Cy])

        # exact tangent point: incline meets loop with no kink, ball enters
        # moving counter-clockwise
        d_vec = P0 - C
        d = np.linalg.norm(d_vec)
        alpha = np.arctan2(d_vec[1], d_vec[0])
        beta = np.arccos(R / d)
        theta_T = None
        for sgn in (+1, -1):
            th = alpha + sgn * beta
            T = C + R * np.array([np.cos(th), np.sin(th)])
            v_in = (T - P0) / np.linalg.norm(T - P0)
            t_ccw = np.array([-np.sin(th), np.cos(th)])
            if np.dot(v_in, t_ccw) > 0:
                theta_T, T_pt = th, T
                break
        assert theta_T is not None
        T3 = np.array([T_pt[0], T_pt[1], 0.0])
        P0_3 = np.array([P0[0], P0[1], 0.0])
        C3 = np.array([Cx, Cy, 0.0])

        L1 = float(np.linalg.norm(T_pt - P0))
        theta_top = 5 * np.pi / 2
        s_top = (L1 + R * (theta_top - theta_T)) / (L1 + 2 * np.pi * R)

        # invisible, uniformly sampled motion path: incline + full loop
        pts = []
        n1 = 60
        for i in range(n1):
            t = i / (n1 - 1)
            p = P0 + (T_pt - P0) * t
            pts.append([p[0], p[1], 0.0])
        n2 = 160
        for i in range(1, n2 + 1):
            th = theta_T + (i / n2) * 2 * np.pi
            pts.append([Cx + R * np.cos(th), Cy + R * np.sin(th), 0.0])
        path = VMobject()
        path.set_points_as_corners(pts)
        path.set_stroke(opacity=0)

        # ================= left-panel text blocks =================
        B1 = tblock([
            TL(r"Bola meluncur dari ketinggian "
               r"\textcolor[HTML]{FFFF00}{$h$},"),
            TL(r"melewati loop \textcolor[HTML]{5BA5BC}{$R = 0{,}5$} m."),
            TL(r"Berapa \textcolor[HTML]{FFFF00}{$h$} minimum agar tak jatuh"),
            TL(r"di puncak?"),
        ])
        B2 = tblock([
            TL(r"Syarat di puncak:"),
            TL(r"\textcolor[HTML]{58C4DD}{$N$} $+$ "
               r"\textcolor[HTML]{B86E64}{$mg$} $= mv^2/R$."),
        ])
        B3 = tblock([
            TL(r"Tepat tak jatuh $\to$ "
               r"\textcolor[HTML]{58C4DD}{$N = 0$},"),
            TL(r"jadi \textcolor[HTML]{FFFF00}{$v^2 = gR$}."),
        ])
        B4 = tblock([
            TL(r"\textcolor[HTML]{FFFF00}{Kekekalan energi}:"),
            TL(r"$mgh = mg(2R) + \frac{1}{2}mv^2$."),
        ])
        B5 = tblock([
            TL(r"Substitusi \textcolor[HTML]{FFFF00}{$v^2 = gR$}:"),
            TL(r"\textcolor[HTML]{FFFF00}{$h = 2{,}5R = 1{,}25$} m."),
        ])
        B6 = tblock([
            TL(r"Jawaban: \textcolor[HTML]{FFFF00}{(D)}"),
        ])
        blocks = [B1, B2, B3, B4, B5, B6]
        all_text = VGroup(*blocks).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        all_text.to_edge(LEFT, buff=0.5)
        all_text.move_to([all_text.get_center()[0],
                          3.2 - all_text.height / 2, 0.0])
        for b in blocks:
            b.set_opacity(0.45)

        def bar_for(b):
            return SurroundingRectangle(b, color=YELLOW, fill_opacity=0.12,
                                        stroke_width=0, buff=0.14)

        # ================= beat 1: title =================
        title = serif(r"Energi \& Loop-the-Loop", size=54)
        sub = serif(r"$h$ minimum agar tak jatuh di puncak loop",
                    size=30, color=GRAY)
        sub.next_to(title, DOWN, buff=0.35)
        self.play(Write(title, run_time=1.4))
        self.play(FadeIn(sub, run_time=0.8))
        self.wait(1.6)
        self.play(FadeOut(title, run_time=0.8), FadeOut(sub, run_time=0.8))

        # ================= beat 2: split screen + full text + track ====
        divider = Line([0, -3.9, 0], [0, 3.9, 0], color=GRAY,
                       stroke_width=2, stroke_opacity=0.4)
        incline = Line(P0_3, T3, color=WHITE, stroke_width=5)
        loop = Circle(radius=R, color=TEAL, stroke_width=5).move_to(C3)
        rad_line = Line(C3, C3 + np.array([R, 0, 0]), color=GRAY,
                        stroke_width=2)
        r_lab = MathTex(r"R = 0{,}5\ \text{m}", font_size=26, color=GRAY)
        r_lab.next_to(rad_line, DOWN, buff=0.12)

        y_top, y_bot = P0[1], Cy - R
        h_arrow = DoubleArrow([0.55, y_bot, 0], [0.55, y_top, 0],
                              color=YELLOW, stroke_width=4, buff=0.05)
        h_lab = MathTex(r"h = ?", font_size=32, color=YELLOW)
        h_lab.move_to([1.18, (y_top + y_bot) / 2, 0.0])
        dash_top = DashedLine([P0[0], y_top, 0], [1.7, y_top, 0],
                              color=GRAY, stroke_width=2, dash_length=0.1)
        dash_bot = DashedLine([2.0, y_bot, 0], [2.9, y_bot, 0],
                              color=GRAY, stroke_width=2, dash_length=0.1)

        self.play(Create(divider, run_time=0.8))
        for b in blocks:
            self.play(FadeIn(b, run_time=0.4))
        self.play(Create(incline, run_time=1.2), Create(loop, run_time=1.6))
        self.play(Create(rad_line, run_time=0.5), FadeIn(r_lab, run_time=0.5))
        self.play(Create(h_arrow, run_time=0.7), FadeIn(h_lab, run_time=0.5),
                  Create(dash_top, run_time=0.5),
                  Create(dash_bot, run_time=0.5))
        self.wait(1.0)

        # ball (updater-driven; added, never faded)
        s = ValueTracker(0.0)
        ball = Dot(point=path.point_from_proportion(0.0), radius=0.13,
                   color=YELLOW)
        ball.add_updater(
            lambda m: m.move_to(path.point_from_proportion(s.get_value())))

        # ================= T1: release =================
        bar = bar_for(B1)
        self.play(FadeIn(bar, run_time=0.6), B1.animate.set_opacity(1.0),
                  run_time=0.6)
        self.wait(0.5)
        self.add(ball)
        self.wait(0.5)
        self.play(Indicate(h_arrow, run_time=1.0))
        self.wait(1.2)

        # ================= T2: slide to top + FBD =================
        bar2 = bar_for(B2)
        self.play(FadeOut(bar, run_time=0.5),
                  FadeIn(bar2, run_time=0.5),
                  B1.animate.set_opacity(0.45),
                  B2.animate.set_opacity(1.0), run_time=0.5)
        self.wait(0.5)
        self.play(s.animate.set_value(s_top), run_time=7, rate_func=linear)
        self.wait(0.8)

        top_pt = np.array([Cx, Cy + R, 0.0])
        mg_arr = Arrow(top_pt + np.array([-0.16, -0.16, 0]),
                       top_pt + np.array([-0.16, -0.95, 0]),
                       color=REDW, stroke_width=6, buff=0,
                       max_tip_length_to_length_ratio=0.25)
        n_arr = Arrow(top_pt + np.array([0.16, -0.16, 0]),
                      top_pt + np.array([0.16, -0.55, 0]),
                      color=BLUE, stroke_width=6, buff=0,
                      max_tip_length_to_length_ratio=0.3)
        mg_lab = MathTex("mg", font_size=30, color=REDW)
        mg_lab.next_to(mg_arr, LEFT, buff=0.12)
        n_lab = MathTex("N", font_size=30, color=BLUE)
        n_lab.next_to(n_arr, RIGHT, buff=0.12)
        self.play(Create(mg_arr, run_time=0.8), FadeIn(mg_lab, run_time=0.6))
        self.wait(0.6)
        self.play(Create(n_arr, run_time=0.8), FadeIn(n_lab, run_time=0.6))
        self.wait(0.6)

        eq1 = MathTex(r"N", r"+", r"mg", r"=\frac{mv^2}{R}", font_size=40)
        eq1[0].set_color(BLUE)
        eq1[2].set_color(REDW)
        eq1.move_to([3.55, -3.3, 0.0])
        self.play(Write(eq1, run_time=1.2))
        self.wait(1.2)

        # ================= T3: N = 0 -> v^2 = gR =================
        bar3 = bar_for(B3)
        self.play(FadeOut(bar2, run_time=0.5),
                  FadeIn(bar3, run_time=0.5),
                  B2.animate.set_opacity(0.45),
                  B3.animate.set_opacity(1.0), run_time=0.5)
        self.wait(0.5)
        eq2 = MathTex(r"v^2 = gR", font_size=46, color=YELLOW)
        eq2.move_to([3.55, -3.3, 0.0])
        box2 = SurroundingRectangle(eq2, color=YELLOW, buff=0.12,
                                    stroke_width=2)
        self.play(FadeTransform(eq1, eq2), run_time=1.2)
        self.play(Create(box2, run_time=0.6))
        self.wait(1.5)

        # ================= T4: energy =================
        bar4 = bar_for(B4)
        self.play(FadeOut(bar3, run_time=0.5),
                  FadeIn(bar4, run_time=0.5),
                  B3.animate.set_opacity(0.45),
                  B4.animate.set_opacity(1.0), run_time=0.5)
        self.wait(0.5)
        eq3 = MathTex(r"mgh = mg(2R) + \frac{1}{2}mv^2", font_size=40)
        eq3.move_to([3.55, -3.3, 0.0])
        self.play(FadeOut(box2, run_time=0.4),
                  FadeTransform(eq2, eq3), run_time=1.2)
        self.wait(1.5)

        # ================= T5: substitute -> answer, loop payoff ======
        bar5 = bar_for(B5)
        self.play(FadeOut(bar4, run_time=0.5),
                  FadeIn(bar5, run_time=0.5),
                  B4.animate.set_opacity(0.45),
                  B5.animate.set_opacity(1.0), run_time=0.5)
        self.wait(0.5)
        eq4 = MathTex(r"mgh = 2mgR + \frac{1}{2}m(gR)", font_size=40)
        eq4.move_to([3.55, -3.3, 0.0])
        self.play(FadeTransform(eq3, eq4), run_time=1.2)
        self.wait(0.8)
        eq5 = MathTex(r"h = 2{,}5R", font_size=46)
        eq5.move_to([3.55, -3.3, 0.0])
        self.play(FadeTransform(eq4, eq5), run_time=1.2)
        self.wait(0.8)
        eq6 = MathTex(r"h = 1{,}25\ \text{m}", font_size=50, color=YELLOW)
        eq6.move_to([3.55, -3.3, 0.0])
        self.play(FadeTransform(eq5, eq6), run_time=1.2)
        self.wait(1.0)
        # payoff: the ball completes the loop
        self.play(FadeOut(mg_arr, run_time=0.5), FadeOut(n_arr, run_time=0.5),
                  FadeOut(mg_lab, run_time=0.5), FadeOut(n_lab, run_time=0.5))
        self.play(s.animate.set_value(1.0), run_time=5, rate_func=linear)
        self.wait(1.0)

        # ================= T6: answer + options =================
        bar6 = bar_for(B6)
        self.play(FadeOut(bar5, run_time=0.5),
                  FadeIn(bar6, run_time=0.5),
                  B5.animate.set_opacity(0.45),
                  B6.animate.set_opacity(1.0), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(eq6, run_time=0.6))
        big_ans = MathTex(r"h = 1{,}25\ \text{m}", font_size=60,
                          color=YELLOW)
        big_ans.move_to([4.9, 2.75, 0.0])
        self.play(Write(big_ans, run_time=1.2))
        self.wait(0.6)
        opts = VGroup(*[MathTex(s, font_size=24) for s in
                        [r"(A)\ 0{,}50\ \text{m}", r"(B)\ 0{,}75\ \text{m}",
                         r"(C)\ 1{,}00\ \text{m}", r"(D)\ 1{,}25\ \text{m}",
                         r"(E)\ 1{,}50\ \text{m}"]])
        opts.arrange(RIGHT, buff=0.25)
        opts.move_to([3.55, -3.3, 0.0])
        self.play(FadeIn(opts, run_time=1.0))
        self.wait(0.6)
        obox = SurroundingRectangle(opts[3], color=YELLOW, buff=0.13,
                                    stroke_width=3)
        self.play(Create(obox, run_time=0.8),
                  opts[3].animate.set_color(YELLOW), run_time=0.8)
        self.wait(3.0)
