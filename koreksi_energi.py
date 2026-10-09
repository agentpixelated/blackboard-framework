"""Koreksi No.5 Day 9 (Energi kinetik proyektil): Naby memakai E=mgh
(potensial!) untuk energi kinetik. Video lengkap dari rumus dasar
Ek=1/2 mv^2: vx tetap, vy=0 di puncak -> Ek = E/4 -> (D)."""
from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

W_RED = "#b86e64"
WIRE = "#D8D8D8"
VEL = "#58C4DD"
VELX = "#8fd0e8"


def tline(parts, size=30):
    mob = VGroup(*[serif(t, size=size, color=c or WHITE) for t, c in parts])
    mob.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    return mob


def xmark(pos, size=0.32, color=W_RED):
    d = size / 2
    l1 = Line(pos + [-d, d, 0], pos + [d, -d, 0], color=color, stroke_width=8)
    l2 = Line(pos + [-d, -d, 0], pos + [d, d, 0], color=color, stroke_width=8)
    return VGroup(l1, l2)


def arrow(s, e, color, w=7):
    return Arrow(np.array(s, dtype=float), np.array(e, dtype=float),
                 color=color, stroke_width=w, buff=0,
                 max_tip_length_to_length_ratio=0.22)


class KoreksiEnergi(Scene):
    def construct(self):
        # ============ beat 1: title ============
        title = serif("Koreksi No. 5: Energi Kinetik Proyektil", size=48)
        self.play(Write(title), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(title, run_time=0.7))

        divider = Line([0, 3.8, 0], [0, -3.8, 0], color=GRAY, stroke_width=2)
        self.play(Create(divider), run_time=0.5)

        # ============ beat 2: his error ============
        head = tline([("Yang kamu tulis:", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        w1 = tline([("$E = mgh$", W_RED)], size=38).move_to([-3.55, 2.4, 0])
        x1 = xmark(np.array([-0.7, 2.4, 0]))
        why = tline([("itu energi POTENSIAL,", GRAY)], size=25).move_to([-3.55, 1.7, 0])
        why2 = tline([("bukan kinetik!", GRAY)], size=25).move_to([-3.55, 1.25, 0])
        self.play(FadeIn(head, run_time=0.5))
        self.play(Write(w1, run_time=0.7), FadeIn(x1, run_time=0.4))
        self.play(FadeIn(why, run_time=0.4), FadeIn(why2, run_time=0.4))
        self.wait(1.2)
        self.play(*[FadeOut(m, run_time=0.5) for m in (head, w1, x1, why, why2)])

        # ============ beat 3: fundamental + trajectory ============
        # parabola: y = 4h x (1-x), peak at x=0.5
        axes_x0, axes_y0 = 1.0, -2.2
        PW, PH = 5.2, 3.0
        def traj(t):
            return np.array([axes_x0 + t * PW, axes_y0 + 4 * PH * t * (1 - t), 0])
        curve = ParametricFunction(traj, t_range=[0, 1, 0.01], color=WIRE, stroke_width=4)
        ground = Line([0.6, axes_y0, 0], [6.6, axes_y0, 0], color=GRAY, stroke_width=3)

        f0 = tline([("Rumus dasar:", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        f1 = tline([("$E_k = \\tfrac{1}{2}mv^2$", GREEN)], size=36).move_to([-3.55, 2.45, 0])
        f2 = tline([("awal: $E = \\tfrac{1}{2}mv_0^2$", WHITE)], size=30).move_to([-3.55, 1.8, 0])
        self.play(Write(f0, run_time=0.6), Write(f1, run_time=0.8))
        self.play(Create(ground, run_time=0.4), Create(curve, run_time=1.2))
        self.play(Write(f2, run_time=0.8))
        self.wait(0.8)

        # ============ beat 4: velocity at launch vs top ============
        # launch velocity vector at 60 deg
        p_launch = traj(0.02)
        v0_vec = np.array([np.cos(np.pi / 3), np.sin(np.pi / 3), 0])
        v0_arr = arrow(p_launch, p_launch + 1.6 * v0_vec, VEL, w=7)
        v0_lab = serif("$v_0$", size=26, color=VEL).next_to(v0_arr, UP, buff=0.08)
        ang = Arc(radius=0.45, start_angle=0, angle=np.pi / 3, color=GRAY,
                  stroke_width=3).move_to(p_launch + np.array([0.45, 0, 0]))
        ang_lab = serif("$60^\\circ$", size=22, color=GRAY).move_to(p_launch + [0.75, 0.28, 0])

        # top: only horizontal velocity remains
        p_top = traj(0.5)
        vx_arr = arrow(p_top, p_top + np.array([1.3, 0, 0]), VELX, w=7)
        vx_lab = serif("$v_x = v_0\\cos 60^\\circ$", size=24, color=VELX).next_to(vx_arr, UP, buff=0.1)
        vx_lab2 = serif("$= \\tfrac{1}{2}v_0$", size=24, color=VELX).next_to(vx_lab, DOWN, buff=0.06)
        vy_note = tline([("$v_y = 0$ di puncak", GRAY)], size=24).move_to([3.6, -1.2, 0])

        s1 = tline([("Kecepatan di puncak:", WHITE)], size=30).move_to([-3.55, 1.1, 0])
        self.play(Write(s1, run_time=0.7))
        self.play(Create(v0_arr, run_time=0.6), FadeIn(v0_lab, run_time=0.3),
                  Create(ang, run_time=0.4), FadeIn(ang_lab, run_time=0.3))
        self.wait(0.6)
        dot = Dot(point=p_top, color=YELLOW, radius=0.1)
        self.play(FadeIn(dot, run_time=0.3),
                  Create(vx_arr, run_time=0.7), FadeIn(vx_lab, run_time=0.4))
        self.play(FadeIn(vx_lab2, run_time=0.4), FadeIn(vy_note, run_time=0.4))
        self.wait(1.2)
        self.play(*[FadeOut(m, run_time=0.5) for m in (f0, f1, f2, s1)])

        # ============ beat 5: derive Ek at top ============
        d1 = tline([("$E_{k} = \\tfrac{1}{2}m v_x^2$", WHITE)], size=34).move_to([-3.55, 2.6, 0])
        d2 = tline([("$= \\tfrac{1}{2}m\\left(\\tfrac{1}{2}v_0\\right)^2$", WHITE)], size=34).move_to([-3.55, 1.9, 0])
        d3 = tline([("$= \\tfrac{1}{4}\\left(\\tfrac{1}{2}mv_0^2\\right)$", WHITE)], size=34).move_to([-3.55, 1.2, 0])
        d4 = tline([("$= \\tfrac{1}{4}E$", YELLOW)], size=40).move_to([-3.55, 0.4, 0])
        ans = tline([("Jawaban: (D)", YELLOW)], size=40).move_to([-3.55, -0.5, 0])
        self.play(Write(d1, run_time=0.9))
        self.wait(0.3)
        self.play(Write(d2, run_time=0.9))
        self.wait(0.3)
        self.play(Write(d3, run_time=0.9))
        self.wait(0.3)
        self.play(Write(d4, run_time=0.8))
        box = SurroundingRectangle(ans, color=YELLOW, buff=0.18, stroke_width=3)
        self.play(Write(ans, run_time=0.8), Create(box, run_time=0.5))
        self.wait(1.0)
        self.play(*[FadeOut(m, run_time=0.6) for m in (d1, d2, d3, d4, ans, box)])

        # ============ beat 6: lesson ============
        lhead = tline([("Pelajaran:", YELLOW)], size=34).move_to([-3.55, 2.2, 0])
        l1 = tline([("Di puncak, peluru tetap", WHITE)], size=30).move_to([-3.55, 1.5, 0])
        l2 = tline([("bergerak horizontal.", WHITE)], size=30).move_to([-3.55, 0.95, 0])
        l3 = tline([("$E_k \\neq 0$ selama $v_x \\neq 0$.", GREEN)], size=30).move_to([-3.55, 0.2, 0])
        self.play(Write(lhead, run_time=0.7))
        self.play(Write(l1, run_time=0.7), Write(l2, run_time=0.7))
        self.wait(0.4)
        self.play(Write(l3, run_time=0.8))
        # animate dot along trajectory to reinforce motion continues
        self.play(MoveAlongPath(dot, curve), run_time=2.0, rate_func=linear)
        self.wait(1.0)
