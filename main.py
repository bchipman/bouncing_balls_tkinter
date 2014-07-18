import tkinter
from tkinter import N, S, E, W
from random import uniform as RND
from random import choice as PICK
from threading import Timer
from coordinate import Coordinate, Oval
from itertools import combinations
from tk_colors import select_colors
class Ball:
    def __init__(self, center, radius, velocity, color=None):
        self.center_xy = center
        self.radius_xy = radius
        self.velocity_xy = velocity
        self.color = color
    def set_color(self, color):
        self.color = color
class Game:
    def __init__(self):
        self.__SETUP__variables()
        self.__SETUP__balls()
        self.__SETUP__window()
        self.__SETUP__controls()
        self.GO()
    def __SETUP__variables(self):
        self._bg_color = 'grey'
        self._FPS = 100
        self._mSPF = self._FPS_to_mSPF(self._FPS)
        self._CLICK_PAUSE = False
        self._RESIZE_PAUSE = False
    def __SETUP__balls(self):
        num_balls = 10
        ball_list = []
        for n in range(0, num_balls):
            while True:
                new_ball = self._make_random_ball()
                new_ball_OK = not self._check_if_new_ball_overlapping_with_existing_balls(new_ball, ball_list)
                if new_ball_OK:
                    break
            ball_list.append(new_ball)
        self.balls = ball_list
    def _check_if_new_ball_overlapping_with_existing_balls(self, new_ball, ball_list):
        for ball in ball_list:
            overlapping = self._check_for_ball_ball_collision(new_ball, ball)
            if overlapping:
                return True
        return False
    def _make_random_ball(self):
        XY = RND(0.1, 0.9), RND(0.1, 0.9)
        R = RND(0.03, 0.05)
        V = RND(15, 35) / 10000
        C = PICK(select_colors)
        BALL = Ball(center=XY, radius=(R, R), velocity=(V, V), color=C)
        return BALL
    def __SETUP__window(self):
        self._root_window = tkinter.Tk()
        self._canvas = tkinter.Canvas(master=self._root_window, background=self._bg_color, highlightthickness=0, height=400, width=400)
        self._canvas.grid(column=0, row=0, sticky=N + S + E + W)
        self._root_window.columnconfigure(index=0, weight=1)
        self._root_window.rowconfigure(index=0, weight=1)
    def __SETUP__controls(self):
        self._root_window.bind('<Configure>', self._on_configure)
        self._root_window.bind('<Button-1>', self._on_mouse_click)
    def GO(self):
        self._move_balls()
        self._trace_ball_coordinates()
    def _trace_ball_coordinates(self):
        for ball in self.balls:
            N, S, E, W = self._get_ball_edges(ball)
            print('{:10}:    E {:.2f}   W {:.2f}     N {:.2f}   S {:.2f}'.format(ball.color, W, E, N, S))
        print()
    def _move_balls(self):
        if not self._CLICK_PAUSE and not self._RESIZE_PAUSE:
            self._canvas.delete(tkinter.ALL)
            self._change_position_of_balls()
            self._check_if_any_ball_hit_wall()
            self._change_ball_direction_if_ball_ball_collision()
            self._draw_balls()
            self._trace_ball_coordinates()
            self._root_window.update_idletasks()
        self._root_window.after(self._mSPF, self._move_balls)
    def _draw_balls(self):
        for ball in self.balls:
            X0, Y0, X1, Y1 = Oval(ball.center_xy, ball.radius_xy).all()
            X0, Y0 = Coordinate((X0, Y0)).absolute(self._get_WH())
            X1, Y1 = Coordinate((X1, Y1)).absolute(self._get_WH())
            self._canvas.create_oval(X0, Y0, X1, Y1, fill=ball.color)
    def _change_position_of_balls(self):
        for ball in self.balls:
            x, y = ball.center_xy
            dx, dy = ball.velocity_xy
            ball.center_xy = (x + dx, y + dy)
    def _check_if_any_ball_hit_wall(self):
        for ball in self.balls:
            N, S, E, W = self._get_ball_edges(ball)
            dx, dy = ball.velocity_xy
            if W < 0 or E > 1:
                dx *= -1
            if N < 0 or S > 1:
                dy *= -1
            ball.velocity_xy = (dx, dy)
    def _get_ball_edges(self, ball):
        x, y = ball.center_xy
        rx, ry = ball.radius_xy
        N, S = y - ry, y + ry
        W, E = x - rx, x + rx
        return (N, S, E, W)
    def _change_ball_direction_if_ball_ball_collision(self):
        index_combo_list = list(combinations(range(0, len(self.balls)), 2))
        for i, j in index_combo_list:
            ball_A = self.balls[i]
            ball_B = self.balls[j]
            DX, DY = ball_A.velocity_xy
            dx, dy = ball_B.velocity_xy
            collision = self._check_for_ball_ball_collision(ball_A, ball_B)
            if collision:
                dx, dy = dx * -1, dy * -1
                DX, DY = DX * -1, DY * -1
            ball_A.velocity_xy = DX, DY
            ball_B.velocity_xy = dx, dy
            self.balls[i] = ball_A
            self.balls[j] = ball_B
    def _check_for_ball_ball_collision(self, ball_A, ball_B):
        X, Y = ball_A.center_xy
        R = ball_A.radius_xy[0]
        x, y = ball_B.center_xy
        r = ball_B.radius_xy[0]
        Rr_sum_sqd = (R + r) ** 2
        D_sqd = (X - x) ** 2 + (Y - y) ** 2
        if D_sqd <= Rr_sum_sqd:
            return True
        else:
            return False
    def _get_WH(self):
        return (self._root_window.winfo_width(), self._root_window.winfo_height())
    def _on_configure(self, event):
        self._RESIZE_PAUSE = True
        t = Timer(0.5, self._set_resizing_to_false)
        t.start()
    def _set_resizing_to_false(self):
        self._RESIZE_PAUSE = False
    def _on_mouse_click(self, event):
        if self._CLICK_PAUSE == True:
            self._CLICK_PAUSE = False
        elif self._CLICK_PAUSE == False:
            self._CLICK_PAUSE = True
    def _FPS_to_mSPF(self, FPS):
        return int((1 / FPS) * 1000)
    def start(self):
        self._root_window.mainloop()
if __name__ == '__main__':
    Game().start()
