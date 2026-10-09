"""Jarak dari percepatan via integral: dari definisi a=dv/dt, v=dx/dt,
integralkan dua kali -> v=v0+at -> s=v0t+1/2 at^2, plus tafsir luas
grafik. Menghubungkan ke No.4 (s=25 m)."""
from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

W_RED = "#b86e64"
WIRE = "#D8D8D8"
AREA = "#2b6a7d"


def tline(parts, size=30):
    mob = VGroup(*[serif(t, size=size, color=c or WHITE) for t, c in parts])
    mob.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    return mob


class JarakIntegral(Scene):
    def construct(self):
        # ============ beat 1: title ============
        title = serif("Jarak dari Percepatan: via Integral", size=48)
        self.play(Write(title), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(title, run_time=0.7))

        divider = Line([0, 3.8, 0], [0, -3.8, 0], color=GRAY, stroke_width=2)
        self.play(Create(divider), run_time=0.5)

        # ============ beat 2: definitions ============
        d0 = tline([("Mulai dari definisi:", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        d1 = tline([("$a = \\dfrac{dv}{dt}$", BLUE)], size=38).move_to([-3.55, 2.4, 0])
        d1b = tline([("percepatan = laju perubahan $v$", GRAY)], size=22).move_to([-3.55, 1.9, 0])
        d2 = tline([("$v = \\dfrac{dx}{dt}$", BLUE)], size=38).move_to([-3.55, 1.2, 0])
        d2b = tline([("kecepatan = laju perubahan $x$", GRAY)], size=22).move_to([-3.55, 0.7, 0])
        self.play(Write(d0, run_time=0.7))
        self.play(Write(d1, run_time=0.8), FadeIn(d1b, run_time=0.4))
        self.wait(0.4)
        self.play(Write(d2, run_time=0.8), FadeIn(d2b, run_time=0.4))
        self.wait(1.0)
        self.play(*[FadeOut(m, run_time=0.5) for m in (d0, d1, d1b, d2, d2b)])

        # ============ beat 3: integrate a -> v, with a-t graph ============
        # axes on right
        ax1 = Axes(x_range=[0, 10, 5], y_range=[0, 1.2, 1],
                   x_length=4.6, y_length=2.6,
                   axis_config={"color": GRAY, "stroke_width": 3},
                   tips=False).move_to([3.4, 0.4, 0])
        ax1_labx = serif("$t$", size=24, color=GRAY).next_to(ax1.x_axis, DOWN, buff=0.15)
        ax1_laby = serif("$a$", size=24, color=GRAY).next_to(ax1.y_axis, LEFT, buff=0.15)
        a_line = ax1.plot(lambda t: 0.5, x_range=[0, 10], color=BLUE, stroke_width=5)
        a_area = ax1.get_area(a_line, x_range=[0, 10], color=AREA, opacity=0.45)

        s1 = tline([("Integralkan $a$:", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        e1 = tline([("$v(t)-v_0 = \\int_0^t a\\,dt'$", WHITE)], size=32).move_to([-3.55, 2.4, 0])
        e2 = tline([("untuk $a$ tetap:", GRAY)], size=26).move_to([-3.55, 1.75, 0])
        e3 = tline([("$v(t) = v_0 + at$", GREEN)], size=38).move_to([-3.55, 1.05, 0])
        note = tline([("luas di bawah grafik $a$--$t$", GRAY)], size=22).move_to([-3.55, 0.4, 0])
        note2 = tline([("= perubahan kecepatan", GRAY)], size=22).move_to([-3.55, -0.05, 0])

        self.play(Write(s1, run_time=0.7))
        self.play(Create(ax1, run_time=0.6), FadeIn(ax1_labx), FadeIn(ax1_laby),
                  run_time=0.4)
        self.play(Write(e1, run_time=1.0))
        self.play(Create(a_line, run_time=0.8))
        self.wait(0.4)
        self.play(Write(e2, run_time=0.6), FadeIn(a_area, run_time=0.6))
        self.play(Write(e3, run_time=0.9))
        self.play(FadeIn(note, run_time=0.4), FadeIn(note2, run_time=0.4))
        self.wait(1.4)
        self.play(*[FadeOut(m, run_time=0.5) for m in
                    (s1, e1, e2, e3, note, note2, ax1, ax1_labx, ax1_laby,
                     a_line, a_area)])

        # ============ beat 4: integrate v -> x, with v-t graph ============
        ax2 = Axes(x_range=[0, 10, 5], y_range=[0, 6, 2],
                   x_length=4.6, y_length=2.6,
                   axis_config={"color": GRAY, "stroke_width": 3},
                   tips=False).move_to([3.4, 0.4, 0])
        ax2_labx = serif("$t$", size=24, color=GRAY).next_to(ax2.x_axis, DOWN, buff=0.15)
        ax2_laby = serif("$v$", size=24, color=GRAY).next_to(ax2.y_axis, LEFT, buff=0.15)
        # v(t) = 0.5 t  (v0=0, a=0.5 as in No.4)
        v_line = ax2.plot(lambda t: 0.5 * t, x_range=[0, 10], color=BLUE, stroke_width=5)
        v_area = ax2.get_area(v_line, x_range=[0, 10], color=AREA, opacity=0.45)

        s2 = tline([("Integralkan $v$:", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        q1 = tline([("$x(t)-x_0 = \\int_0^t v\\,dt'$", WHITE)], size=32).move_to([-3.55, 2.4, 0])
        q2 = tline([("$= \\int_0^t (v_0+at')\\,dt'$", WHITE)], size=32).move_to([-3.55, 1.75, 0])
        q3 = tline([("$x(t) = x_0+v_0t+\\tfrac{1}{2}at^2$", GREEN)], size=36).move_to([-3.55, 1.0, 0])
        qn = tline([("luas trapesium di bawah $v$--$t$", GRAY)], size=22).move_to([-3.55, 0.35, 0])

        self.play(Write(s2, run_time=0.7))
        self.play(Create(ax2, run_time=0.6), FadeIn(ax2_labx), FadeIn(ax2_laby),
                  run_time=0.4)
        self.play(Write(q1, run_time=1.0))
        self.play(Create(v_line, run_time=1.0))
        self.wait(0.3)
        self.play(Write(q2, run_time=0.9), FadeIn(v_area, run_time=0.6))
        self.wait(0.4)
        self.play(Write(q3, run_time=1.1))
        self.play(FadeIn(qn, run_time=0.4))
        self.wait(1.4)
        self.play(*[FadeOut(m, run_time=0.5) for m in
                    (s2, q1, q2, q3, qn, ax2, ax2_labx, ax2_laby, v_line, v_area)])

        # ============ beat 5: apply to No.4 ============
        a0 = tline([("Terapkan ke No. 4:", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        a1 = tline([("$v_0=0,\\ a=0{,}5,\\ t=10$", WHITE)], size=32).move_to([-3.55, 2.4, 0])
        a2 = tline([("$s = 0+\\tfrac{1}{2}(0{,}5)(10)^2$", WHITE)], size=34).move_to([-3.55, 1.7, 0])
        a3 = tline([("$s = 25$ m", GREEN)], size=40).move_to([-3.55, 0.9, 0])
        a4 = tline([("inilah pernyataan (3).", GRAY)], size=26).move_to([-3.55, 0.2, 0])
        self.play(Write(a0, run_time=0.7))
        self.play(Write(a1, run_time=0.8))
        self.play(Write(a2, run_time=0.9))
        self.wait(0.4)
        self.play(Write(a3, run_time=0.8))
        self.play(FadeIn(a4, run_time=0.4))
        self.wait(1.6)
