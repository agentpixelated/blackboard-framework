"""Koreksi No.1 Day 9: katrol + gesekan. Menunjukkan 2 kesalahan setup
persamaan Naby, lalu FBD dan penurunan yang benar -> (D) 1500 N."""
from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

W_RED = "#b86e64"
ORANGE = "#bf7f49"
WIRE = "#D8D8D8"


def tline(parts, size=30):
    mob = VGroup(*[serif(t, size=size, color=c or WHITE) for t, c in parts])
    mob.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    return mob


def arrow(s, e, color, w=7):
    return Arrow(np.array(s, dtype=float), np.array(e, dtype=float),
                 color=color, stroke_width=w, buff=0,
                 max_tip_length_to_length_ratio=0.22)


def xmark(pos, size=0.32, color=W_RED):
    """Red X mark drawn with two lines (LaTeX can't do U+2717)."""
    d = size / 2
    l1 = Line(pos + [-d, d, 0], pos + [d, -d, 0], color=color, stroke_width=8)
    l2 = Line(pos + [-d, -d, 0], pos + [d, d, 0], color=color, stroke_width=8)
    return VGroup(l1, l2)


class KoreksiKatrol(Scene):
    def construct(self):
        # ---- beat 1: title ----
        title = serif("Koreksi No. 1: Katrol + Gesekan", size=52)
        self.play(Write(title), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(title, run_time=0.7))

        divider = Line([0, 3.8, 0], [0, -3.8, 0], color=GRAY, stroke_width=2)
        self.play(Create(divider), run_time=0.5)

        # ---- beat 2: his two wrong equations ----
        head = tline([("Persamaanmu:", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        w1 = tline([("1500 $-$ T = 200a", W_RED)], size=34).move_to([-3.55, 2.3, 0])
        x1 = xmark(np.array([0, 0, 0])).next_to(w1, RIGHT, buff=0.25)
        why1 = tline([("1500 itu $N-f$, bukan gaya!", GRAY)], size=24).move_to([-3.55, 1.7, 0])
        w2 = tline([("T $-$ 3000 = 300a", W_RED)], size=34).move_to([-3.55, 0.9, 0])
        x2 = xmark(np.array([0, 0, 0])).next_to(w2, RIGHT, buff=0.25)
        why2 = tline([("tanda kebalik!", GRAY)], size=24).move_to([-3.55, 0.3, 0])

        # right side: minimal pulley sketch while errors show
        pul = Circle(radius=0.28, color=WIRE, stroke_width=4).move_to([3.3, 1.6, 0])
        rope_h = Line([1.2, 1.6, 0], [3.02, 1.6, 0], color=WIRE, stroke_width=4)
        rope_v = Line([3.58, 1.6, 0], [3.58, 0.4, 0], color=WIRE, stroke_width=4)
        blk = Rectangle(width=1.3, height=0.8, color=WIRE, stroke_width=4).move_to([1.9, 1.0, 0])
        hang = Rectangle(width=0.9, height=0.9, color=WIRE, stroke_width=4).move_to([3.58, -0.2, 0])
        surf = Line([0.6, 0.6, 0], [3.0, 0.6, 0], color=GRAY, stroke_width=3)

        self.play(FadeIn(head, run_time=0.5))
        self.play(Write(w1, run_time=0.8), FadeIn(x1, run_time=0.4),
                  Create(pul), Create(rope_h), Create(rope_v),
                  Create(blk), Create(hang), Create(surf), run_time=1.2)
        self.play(FadeIn(why1, run_time=0.5))
        self.wait(0.6)
        self.play(Write(w2, run_time=0.8), FadeIn(x2, run_time=0.4))
        self.play(FadeIn(why2, run_time=0.5))
        self.wait(1.0)

        # ---- beat 3: correct FBD on right, correct equations left ----
        self.play(*[FadeOut(m, run_time=0.6) for m in
                    (head, w1, x1, why1, w2, x2, why2)])

        # force arrows
        t_arr = arrow([2.55, 1.0, 0], [3.6, 1.0, 0], BLUE)          # T on 200kg
        f_arr = arrow([1.9, 0.35, 0], [0.9, 0.35, 0], ORANGE)        # friction
        w_arr = arrow([3.58, 0.35, 0], [3.58, -0.9, 0], W_RED)       # 3000 N down
        t2_arr = arrow([3.58, -0.75, 0], [3.58, 0.15, 0], BLUE)      # T up on hang
        lab_t = serif("T", size=28, color=BLUE).next_to(t_arr, UP, buff=0.08)
        lab_f = serif("500 N", size=26, color=ORANGE).next_to(f_arr, DOWN, buff=0.08)
        lab_w = serif("3000 N", size=26, color=W_RED).move_to([4.35, -0.5, 0])
        lab_t2 = serif("T", size=28, color=BLUE).move_to([4.0, -0.15, 0])

        eq1 = tline([("T $-$ 500 = 200a", GREEN)], size=34).move_to([-3.55, 2.6, 0])
        eq2 = tline([("3000 $-$ T = 300a", GREEN)], size=34).move_to([-3.55, 1.8, 0])

        self.play(Create(t_arr), Create(f_arr), Create(w_arr), Create(t2_arr),
                  FadeIn(lab_t), FadeIn(lab_f), FadeIn(lab_w), FadeIn(lab_t2),
                  run_time=1.4)
        self.play(Write(eq1, run_time=0.8))
        self.wait(0.4)
        self.play(Write(eq2, run_time=0.8))
        self.wait(1.0)

        # ---- beat 4: solve ----
        sol = tline([("a = 5 m/s$^2$,  T = 1500 N", YELLOW)], size=34).move_to([-3.55, 0.7, 0])
        ans = tline([("Jawaban: (D)", YELLOW)], size=40).move_to([-3.55, -0.2, 0])
        self.play(Write(sol, run_time=1.0))
        self.wait(0.5)
        box = SurroundingRectangle(ans, color=YELLOW, buff=0.18, stroke_width=3)
        self.play(Write(ans, run_time=0.8), Create(box, run_time=0.5))
        self.wait(0.8)

        # ---- beat 5: lesson ----
        self.play(*[FadeOut(m) for m in (eq1, eq2, sol, ans, box)],
                  run_time=0.6)
        lesson = tline([("Hasil tak ada di opsi?", YELLOW)], size=32).move_to([-3.55, 1.6, 0])
        lesson2 = tline([("cek ulang persamaan geraknya.", WHITE)], size=30).move_to([-3.55, 0.9, 0])
        self.play(Write(lesson, run_time=0.8), Write(lesson2, run_time=0.8))
        self.wait(1.6)
