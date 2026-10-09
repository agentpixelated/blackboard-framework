"""Koreksi No.3 Day 9: tumbukan elastik. Naby memakai rumus tidak-elastik
(menempel); video menunjukkan bedanya lalu penurunan elastik -> (C) 3 m/s."""
from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

W_RED = "#b86e64"
CAR1 = "#58C4DD"
CAR2 = "#d4b84a"


def tline(parts, size=30):
    mob = VGroup(*[serif(t, size=size, color=c or WHITE) for t, c in parts])
    mob.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    return mob


def xmark(pos, size=0.32, color=W_RED):
    d = size / 2
    l1 = Line(pos + [-d, d, 0], pos + [d, -d, 0], color=color, stroke_width=8)
    l2 = Line(pos + [-d, -d, 0], pos + [d, d, 0], color=color, stroke_width=8)
    return VGroup(l1, l2)


def car(x, y, color, label):
    body = Rectangle(width=1.5, height=0.7, color=color, stroke_width=5,
                     fill_color=color, fill_opacity=0.25).move_to([x, y, 0])
    tag = serif(label, size=24, color=color).next_to(body, UP, buff=0.1)
    return VGroup(body, tag)


class KoreksiTumbukan(Scene):
    def construct(self):
        # ---- beat 1: title ----
        title = serif("Koreksi No. 3: Tumbukan Elastik", size=52)
        self.play(Write(title), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(title, run_time=0.7))

        divider = Line([0, 3.8, 0], [0, -3.8, 0], color=GRAY, stroke_width=2)
        self.play(Create(divider), run_time=0.5)

        # ---- beat 2: his wrong equation ----
        head = tline([("Persamaanmu:", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        w1 = tline([("1000$\\cdot$15 = 2500$v$", W_RED)], size=34).move_to([-3.55, 2.3, 0])
        w2 = tline([("$v$ = 6 m/s  (B)", W_RED)], size=34).move_to([-3.55, 1.6, 0])
        x1 = xmark(np.array([-0.9, 1.95, 0]))
        why = tline([("ini rumus tumbukan", GRAY)], size=24).move_to([-3.55, 0.9, 0])
        why2 = tline([("TIDAK elastik (menempel)!", GRAY)], size=24).move_to([-3.55, 0.45, 0])

        # right: two cars stuck together (his mental model)
        c1 = car(1.6, 1.9, CAR1, "1000 kg")
        c2 = car(3.3, 1.9, CAR2, "1500 kg")
        stuck = tline([("menempel, jalan bareng", GRAY)], size=24).move_to([2.45, 0.9, 0])

        self.play(FadeIn(head, run_time=0.5))
        self.play(Write(w1, run_time=0.9), FadeIn(c1, run_time=0.5), FadeIn(c2, run_time=0.5))
        self.play(Write(w2, run_time=0.7), FadeIn(x1, run_time=0.4))
        self.play(FadeIn(why, run_time=0.4), FadeIn(why2, run_time=0.4),
                  FadeIn(stuck, run_time=0.4))
        # cars stick and crawl right together
        self.play(c1.animate.shift(RIGHT * 1.2), c2.animate.shift(RIGHT * 1.2),
                  run_time=1.0)
        self.wait(0.8)

        # ---- beat 3: elastic reality ----
        self.play(*[FadeOut(m, run_time=0.5) for m in
                    (head, w1, w2, x1, why, why2, stuck, c1, c2)])
        head2 = tline([("Elastik sempurna:", GREEN)], size=32).move_to([-3.55, 3.1, 0])
        e1 = tline([("tidak menempel,", GREEN)], size=28).move_to([-3.55, 2.5, 0])
        e2 = tline([("mobil ringan mental balik.", GREEN)], size=28).move_to([-3.55, 1.95, 0])

        d1 = car(1.4, 1.9, CAR1, "1000 kg")
        d2 = car(3.6, 1.9, CAR2, "1500 kg")
        arr = Arrow([2.35, 1.9, 0], [3.0, 1.9, 0], color=WHITE,
                    stroke_width=6, buff=0.05)
        self.play(FadeIn(head2, run_time=0.5), FadeIn(d1), FadeIn(d2), Create(arr),
                  run_time=0.8)
        self.play(FadeIn(e1, run_time=0.5), FadeIn(e2, run_time=0.5))
        # elastic: light car approaches, bounces back left, heavy car drifts right
        self.play(d1.animate.shift(RIGHT * 1.1), run_time=0.6)
        self.play(d1.animate.shift(LEFT * 1.6), d2.animate.shift(RIGHT * 0.7),
                  FadeOut(arr, run_time=0.3), run_time=0.9)
        self.wait(0.8)

        # ---- beat 4: derive from FUNDAMENTAL laws (no shortcut formula) ----
        self.play(*[FadeOut(m, run_time=0.5) for m in (head2, e1, e2, d1, d2)])
        g0 = tline([("Dari rumus dasar:", YELLOW)], size=32).move_to([-3.55, 3.0, 0])
        g1 = tline([("kekekalan momentum", GREEN)], size=28).move_to([-3.55, 2.4, 0])
        f1 = tline([("$1000\\cdot 15 = 1000v_1' + 1500v_2'$", WHITE)], size=32).move_to([-3.55, 1.8, 0])
        g2 = tline([("elastik: $e=1$", GREEN)], size=28).move_to([-3.55, 1.1, 0])
        f2 = tline([("$v_2' - v_1' = 15$", WHITE)], size=32).move_to([-3.55, 0.5, 0])
        f3 = tline([("$\\Rightarrow v_1' = -3$ m/s", YELLOW)], size=36).move_to([-3.55, -0.3, 0])
        note = tline([("negatif = mental balik", GRAY)], size=24).move_to([-3.55, -0.9, 0])
        ans = tline([("Jawaban: (C) 3 m/s", YELLOW)], size=40).move_to([-3.55, -1.7, 0])

        # right: number line showing bounce
        nl = NumberLine(x_range=[-4, 16, 5], length=5.5, color=GRAY,
                        stroke_width=3, include_numbers=False).move_to([3.4, 1.6, 0])
        dot = Dot(point=nl.n2p(15), color=CAR1, radius=0.12)
        lab = serif("$v_1'$ = $-3$", size=26, color=YELLOW).next_to(nl.n2p(-3), DOWN, buff=0.25)
        self.play(Write(g0, run_time=0.7))
        self.play(Write(g1, run_time=0.6), Write(f1, run_time=1.0))
        self.wait(0.4)
        self.play(Write(g2, run_time=0.6), Write(f2, run_time=0.8))
        self.wait(0.4)
        self.play(Write(f3, run_time=0.8), FadeIn(note, run_time=0.4),
                  Create(nl, run_time=0.6))
        self.play(FadeIn(dot, run_time=0.3))
        self.play(dot.animate.move_to(nl.n2p(-3)), run_time=0.9)
        self.play(FadeIn(lab, run_time=0.4))
        box = SurroundingRectangle(ans, color=YELLOW, buff=0.18, stroke_width=3)
        self.play(Write(ans, run_time=0.8), Create(box, run_time=0.5))
        self.wait(1.6)
