"""Koreksi No.4 Day 9 (Usaha/PGK): N != W ketika ada komponen vertikal F.
Video LENGKAP: FBD bertahap, uraian komponen, ΣFy=0 -> N=70, f=35,
ΣFx=ma -> a=0.5, s=25, evaluasi tiap pernyataan, pelajaran umum."""
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
LBLUE = "#8fd0e8"   # components of F


def tline(parts, size=30):
    mob = VGroup(*[serif(t, size=size, color=c or WHITE) for t, c in parts])
    mob.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    return mob


def xmark(pos, size=0.32, color=W_RED):
    d = size / 2
    l1 = Line(pos + [-d, d, 0], pos + [d, -d, 0], color=color, stroke_width=8)
    l2 = Line(pos + [-d, -d, 0], pos + [d, d, 0], color=color, stroke_width=8)
    return VGroup(l1, l2)


def checkmark(pos, size=0.34, color=GREEN):
    p = np.array(pos, dtype=float)
    l1 = Line(p + [-0.28 * size / 0.34, -0.02, 0], p + [-0.02, -0.22 * size / 0.34, 0],
              color=color, stroke_width=8)
    l2 = Line(p + [-0.02, -0.22 * size / 0.34, 0], p + [0.3 * size / 0.34, 0.25 * size / 0.34, 0],
              color=color, stroke_width=8)
    return VGroup(l1, l2)


def arrow(s, e, color, w=7):
    return Arrow(np.array(s, dtype=float), np.array(e, dtype=float),
                 color=color, stroke_width=w, buff=0,
                 max_tip_length_to_length_ratio=0.22)


THETA = np.arctan(0.75)  # 36.87 deg


class KoreksiUsaha(Scene):
    def construct(self):
        # ============ beat 1: title ============
        title = serif("Koreksi No. 4: Normal $\\neq$ Berat", size=50)
        self.play(Write(title), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(title, run_time=0.7))

        divider = Line([0, 3.8, 0], [0, -3.8, 0], color=GRAY, stroke_width=2)
        self.play(Create(divider), run_time=0.5)

        # ============ beat 2: his error ============
        head = tline([("Yang kamu tulis:", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        w1 = tline([("$N = W = 100$ N", W_RED)], size=36).move_to([-3.55, 2.4, 0])
        x1 = xmark(np.array([-0.7, 2.4, 0]))
        why = tline([("$F$ miring: ada komponen", GRAY)], size=25).move_to([-3.55, 1.75, 0])
        why2 = tline([("vertikal ke atas!", GRAY)], size=25).move_to([-3.55, 1.3, 0])
        self.play(FadeIn(head, run_time=0.5))
        self.play(Write(w1, run_time=0.8), FadeIn(x1, run_time=0.4))
        self.play(FadeIn(why, run_time=0.4), FadeIn(why2, run_time=0.4))
        self.wait(1.0)
        self.play(*[FadeOut(m, run_time=0.5) for m in (head, w1, x1, why, why2)])

        # ============ beat 3: FBD builds up ============
        # geometry (right panel)
        bx, by = 3.4, -0.6          # block centre
        bw, bh = 1.7, 1.1
        surf = Line([1.2, by - bh / 2, 0], [5.6, by - bh / 2, 0], color=GRAY, stroke_width=3)
        blk = Rectangle(width=bw, height=bh, color=WIRE, stroke_width=4).move_to([bx, by, 0])
        blk_lab = serif("10 kg", size=24, color=WIRE).move_to([bx, by + 0.1, 0])

        # F at angle theta, tail on TOP edge of block (not buried inside)
        f_len = 2.2
        f_tail = np.array([bx - 0.55, by + bh / 2, 0])
        f_head = f_tail + f_len * np.array([np.cos(THETA), np.sin(THETA), 0])
        f_arr = arrow(f_tail, f_head, BLUE, w=8)
        f_lab = serif("$F=50$ N", size=26, color=BLUE).next_to(f_arr, UP, buff=0.1)

        step = tline([("1. Gambar $F$ miring", WHITE)], size=30).move_to([-3.55, 3.1, 0])
        self.play(Write(step, run_time=0.7))
        self.play(Create(surf, run_time=0.4), Create(blk, run_time=0.5),
                  FadeIn(blk_lab, run_time=0.4))
        self.play(Create(f_arr, run_time=0.8), FadeIn(f_lab, run_time=0.4))
        self.wait(0.8)

        # decompose F
        fx_head = f_tail + np.array([f_len * np.cos(THETA), 0, 0])
        fy_top = fx_head + np.array([0, f_len * np.sin(THETA), 0])
        fx_arr = DashedLine(f_tail, fx_head, color=LBLUE, stroke_width=5)
        fy_arr = DashedLine(fx_head, fy_top, color=LBLUE, stroke_width=5)
        fx_lab = serif("$F_x=40$ N", size=24, color=LBLUE).next_to(fx_arr, DOWN, buff=0.1)
        fy_lab = serif("$F_y=30$ N", size=24, color=LBLUE).next_to(fy_arr, RIGHT, buff=0.1)
        tri = tline([("$\\tan\\theta=0{,}75 \\to$", GRAY)], size=22).move_to([-3.55, 2.4, 0])
        tri2 = tline([("$\\sin\\theta=0{,}6,\\ \\cos\\theta=0{,}8$", GRAY)], size=22).move_to([-3.55, 1.95, 0])

        step2 = tline([("2. Uraikan $F$", WHITE)], size=30).move_to([-3.55, 3.1, 0])
        self.play(FadeOut(step, run_time=0.4), FadeIn(step2, run_time=0.4))
        self.play(Create(fx_arr, run_time=0.6), Create(fy_arr, run_time=0.6))
        self.play(FadeIn(fx_lab, run_time=0.4), FadeIn(fy_lab, run_time=0.4),
                  Write(tri, run_time=0.6), Write(tri2, run_time=0.6))
        self.wait(1.2)

        # N (up) on RIGHT side of block, W (down) on LEFT side - no overlap
        n_arr = arrow([bx + 0.55, by - bh / 2, 0], [bx + 0.55, by + 0.45, 0], GREEN)
        w_arr = arrow([bx - 0.55, by + 0.3, 0], [bx - 0.55, by - 0.85, 0], W_RED)
        fr_arr = arrow([bx + 0.2, by - bh / 2 - 0.18, 0], [bx - 0.7, by - bh / 2 - 0.18, 0], ORANGE)
        n_lab = serif("$N$", size=28, color=GREEN).next_to(n_arr, RIGHT, buff=0.08)
        w_lab = serif("$W=100$ N", size=24, color=W_RED).next_to(w_arr, LEFT, buff=0.08)
        fr_lab = serif("$f$", size=28, color=ORANGE).next_to(fr_arr, DOWN, buff=0.08)

        step3 = tline([("3. Gaya vertikal lain", WHITE)], size=30).move_to([-3.55, 3.1, 0])
        self.play(FadeOut(step2, run_time=0.4), FadeIn(step3, run_time=0.4))
        self.play(Create(n_arr, run_time=0.6), Create(w_arr, run_time=0.6),
                  FadeIn(n_lab, run_time=0.3), FadeIn(w_lab, run_time=0.3))
        self.wait(0.6)
        self.play(Create(fr_arr, run_time=0.6), FadeIn(fr_lab, run_time=0.3))
        self.wait(1.0)
        self.play(*[FadeOut(m, run_time=0.5) for m in
                    (step3, tri, tri2)])

        # ============ beat 4: vertical equilibrium -> N = 70 ============
        vhead = tline([("Arah vertikal: diam", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        veq = tline([("$\\sum F_y = 0$", WHITE)], size=32).move_to([-3.55, 2.45, 0])
        veq2 = tline([("$N + 30 = 100$", WHITE)], size=34).move_to([-3.55, 1.8, 0])
        vres = tline([("$N = 70$ N", GREEN)], size=38).move_to([-3.55, 1.0, 0])
        st1 = tline([("pernyataan (1): BENAR", GREEN)], size=28).move_to([-3.55, 0.3, 0])
        c1 = checkmark(np.array([-0.7, 0.3, 0]))
        self.play(Write(vhead, run_time=0.8))
        self.play(Write(veq, run_time=0.7))
        # highlight Fy and N,W on diagram
        self.play(fy_arr.animate.set_stroke(width=9), run_time=0.4)
        self.play(Write(veq2, run_time=0.8))
        self.wait(0.4)
        self.play(Write(vres, run_time=0.8))
        self.wait(0.4)
        self.play(Write(st1, run_time=0.7), FadeIn(c1, run_time=0.4))
        self.wait(1.2)
        self.play(*[FadeOut(m, run_time=0.5) for m in (vhead, veq, veq2, vres, st1, c1)])

        # ============ beat 5: friction + horizontal -> a = 0.5 ============
        hhead = tline([("Gesek dan arah gerak", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        feq = tline([("$f = \\mu N = 0{,}5\\cdot 70$", WHITE)], size=32).move_to([-3.55, 2.45, 0])
        fres = tline([("$f = 35$ N", ORANGE)], size=36).move_to([-3.55, 1.8, 0])
        st4 = tline([("pernyataan (4): SALAH", W_RED)], size=28).move_to([-3.55, 1.15, 0])
        x4 = xmark(np.array([-0.7, 1.15, 0]))
        heq = tline([("$\\sum F_x = ma$", WHITE)], size=32).move_to([-3.55, 0.4, 0])
        heq2 = tline([("$40 - 35 = 10a$", WHITE)], size=34).move_to([-3.55, -0.25, 0])
        hres = tline([("$a = 0{,}5$ m/s$^2$", GREEN)], size=36).move_to([-3.55, -0.95, 0])
        st2 = tline([("pernyataan (2): BENAR", GREEN)], size=28).move_to([-3.55, -1.6, 0])
        c2 = checkmark(np.array([-0.7, -1.6, 0]))
        self.play(Write(hhead, run_time=0.8))
        self.play(Write(feq, run_time=0.9))
        self.play(fr_arr.animate.set_stroke(width=10), run_time=0.4)
        self.play(Write(fres, run_time=0.7))
        self.play(Write(st4, run_time=0.7), FadeIn(x4, run_time=0.4))
        self.wait(0.8)
        self.play(Write(heq, run_time=0.7))
        self.play(Write(heq2, run_time=0.8))
        self.wait(0.4)
        self.play(Write(hres, run_time=0.8))
        self.play(Write(st2, run_time=0.7), FadeIn(c2, run_time=0.4))
        self.wait(1.2)
        self.play(*[FadeOut(m, run_time=0.5) for m in
                    (hhead, feq, fres, st4, x4, heq, heq2, hres, st2, c2)])

        # ============ beat 6: distance -> s = 25 ============
        dhead = tline([("Jarak 10 sekon", YELLOW)], size=32).move_to([-3.55, 3.1, 0])
        deq = tline([("$s = v_0t + \\tfrac{1}{2}at^2$", WHITE)], size=32).move_to([-3.55, 2.45, 0])
        deq2 = tline([("$s = 0 + \\tfrac{1}{2}(0{,}5)(100)$", WHITE)], size=32).move_to([-3.55, 1.8, 0])
        dres = tline([("$s = 25$ m", GREEN)], size=38).move_to([-3.55, 1.05, 0])
        st3 = tline([("pernyataan (3): BENAR", GREEN)], size=28).move_to([-3.55, 0.4, 0])
        c3 = checkmark(np.array([-0.7, 0.4, 0]))
        ans = tline([("Jawaban: (1), (2), (3)", YELLOW)], size=36).move_to([-3.55, -0.6, 0])
        self.play(Write(dhead, run_time=0.8))
        self.play(Write(deq, run_time=0.9))
        self.play(Write(deq2, run_time=0.9))
        self.play(Write(dres, run_time=0.8))
        self.play(Write(st3, run_time=0.7), FadeIn(c3, run_time=0.4))
        self.wait(0.6)
        box = SurroundingRectangle(ans, color=YELLOW, buff=0.18, stroke_width=3)
        self.play(Write(ans, run_time=0.9), Create(box, run_time=0.5))
        self.wait(1.2)
        self.play(*[FadeOut(m, run_time=0.6) for m in
                    (dhead, deq, deq2, dres, st3, c3, ans, box)])

        # ============ beat 7: the general lesson ============
        lhead = tline([("Pelajaran:", YELLOW)], size=34).move_to([-3.55, 2.6, 0])
        l1 = tline([("$N = W$ hanya jika", WHITE)], size=30).move_to([-3.55, 1.9, 0])
        l2 = tline([("tak ada gaya vertikal lain.", WHITE)], size=30).move_to([-3.55, 1.35, 0])
        l3 = tline([("No. 1: tak ada $F_y$ $\\to$ $N=W$", GRAY)], size=26).move_to([-3.55, 0.5, 0])
        l4 = tline([("No. 4: ada $F_y$ $\\to$ $N=W-F_y$", GRAY)], size=26).move_to([-3.55, -0.05, 0])
        self.play(Write(lhead, run_time=0.7))
        self.play(Write(l1, run_time=0.7), Write(l2, run_time=0.7))
        self.wait(0.5)
        self.play(Write(l3, run_time=0.8))
        self.wait(0.3)
        self.play(Write(l4, run_time=0.8))
        self.wait(2.0)
