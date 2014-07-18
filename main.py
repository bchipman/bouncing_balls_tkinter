import tkinter
from tkinter import N, S, E, W
from random import uniform as RND
from random import choice as PICK
from threading import Timer
from coordinate import Coordinate, Oval
from itertools import combinations
from tk_colors import select_colors
from functools import partial
class Ball:
    def __init__(self, number, center, radius, velocity, color=None):
        self.number = number
        self.center_xy = center
        self.radius_xy = radius
        self.velocity_xy = velocity
        self.color = color
        self.recent_wall_collision = False
        self.recent_ball_collision = False
    def set_color(self, color):
        self.color = color
    def start_wall_collision_timer(self):
        self.recent_wall_collision = True
        wall_timer = Timer(0.1, self.reset_recent_wall_collision)
        wall_timer.start()
    def reset_recent_wall_collision(self):
        self.recent_wall_collision = False
    def start_ball_collision_timer(self):
        self.recent_ball_collision = True
        ball_timer = Timer(25 / 1000, self.reset_recent_ball_collision)
        ball_timer.start()
    def reset_recent_ball_collision(self):
        self.recent_ball_collision = False
class Game:
    def __init__(self):
        self.__SETUP__variables()
        self.__SETUP__balls()
        self.__SETUP__ball_collision_timer_dictionary()
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
        num_balls = 25
        ball_list = []
        for n in range(0, num_balls):
            while True:
                new_ball = self._make_random_ball(n)
                new_ball_OK = not self._check_if_new_ball_overlapping_with_existing_balls(new_ball, ball_list)
                if new_ball_OK:
                    break
            ball_list.append(new_ball)
        self.balls = ball_list
    def __SETUP__ball_collision_timer_dictionary(self):
        index_combo_list = list(combinations(range(0, len(self.balls)), 2))
        [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (0, 24), (0, 25), (0, 26), (0, 27), (0, 28), (0, 29), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 22), (1, 23), (1, 24), (1, 25), (1, 26), (1, 27), (1, 28), (1, 29), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18), (2, 19), (2, 20), (2, 21), (2, 22), (2, 23), (2, 24), (2, 25), (2, 26), (2, 27), (2, 28), (2, 29), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 19), (3, 20), (3, 21), (3, 22), (3, 23), (3, 24), (3, 25), (3, 26), (3, 27), (3, 28), (3, 29), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17), (4, 18), (4, 19), (4, 20), (4, 21), (4, 22), (4, 23), (4, 24), (4, 25), (4, 26), (4, 27), (4, 28), (4, 29), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23), (5, 24), (5, 25), (5, 26), (5, 27), (5, 28), (5, 29), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (6, 21), (6, 22), (6, 23), (6, 24), (6, 25), (6, 26), (6, 27), (6, 28), (6, 29), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13), (7, 14), (7, 15), (7, 16), (7, 17), (7, 18), (7, 19), (7, 20), (7, 21), (7, 22), (7, 23), (7, 24), (7, 25), (7, 26), (7, 27), (7, 28), (7, 29), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (8, 17), (8, 18), (8, 19), (8, 20), (8, 21), (8, 22), (8, 23), (8, 24), (8, 25), (8, 26), (8, 27), (8, 28), (8, 29), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15),
         (9, 16), (9, 17), (9, 18), (9, 19), (9, 20), (9, 21), (9, 22), (9, 23), (9, 24), (9, 25), (9, 26), (9, 27), (9, 28), (9, 29), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15), (10, 16), (10, 17), (10, 18), (10, 19), (10, 20), (10, 21), (10, 22), (10, 23), (10, 24), (10, 25), (10, 26), (10, 27), (10, 28), (10, 29), (11, 12), (11, 13), (11, 14), (11, 15), (11, 16), (11, 17), (11, 18), (11, 19), (11, 20), (11, 21), (11, 22), (11, 23), (11, 24), (11, 25), (11, 26), (11, 27), (11, 28), (11, 29), (12, 13), (12, 14), (12, 15), (12, 16), (12, 17), (12, 18), (12, 19), (12, 20), (12, 21), (12, 22), (12, 23), (12, 24), (12, 25), (12, 26), (12, 27), (12, 28), (12, 29), (13, 14), (13, 15), (13, 16), (13, 17), (13, 18), (13, 19), (13, 20), (13, 21), (13, 22), (13, 23), (13, 24), (13, 25), (13, 26), (13, 27), (13, 28), (13, 29), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19), (14, 20), (14, 21), (14, 22), (14, 23), (14, 24), (14, 25), (14, 26), (14, 27), (14, 28), (14, 29), (15, 16), (15, 17), (15, 18), (15, 19), (15, 20), (15, 21), (15, 22), (15, 23), (15, 24), (15, 25), (15, 26), (15, 27), (15, 28), (15, 29), (16, 17), (16, 18), (16, 19), (16, 20), (16, 21), (16, 22), (16, 23), (16, 24), (16, 25), (16, 26), (16, 27), (16, 28), (16, 29), (17, 18), (17, 19), (17, 20), (17, 21), (17, 22), (17, 23), (17, 24), (17, 25), (17, 26), (17, 27), (17, 28), (17, 29), (18, 19), (18, 20), (18, 21), (18, 22), (18, 23), (18, 24), (18, 25), (18, 26), (18, 27), (18, 28), (18, 29), (19, 20), (19, 21), (19, 22), (19, 23), (19, 24), (19, 25), (19, 26), (19, 27), (19, 28), (19, 29), (20, 21), (20, 22), (20, 23), (20, 24), (20, 25), (20, 26), (20, 27), (20, 28), (20, 29), (21, 22), (21, 23), (21, 24), (21, 25), (21, 26), (21, 27), (21, 28), (21, 29), (22, 23), (22, 24), (22, 25), (22, 26), (22, 27), (22, 28), (22, 29), (23, 24), (23, 25), (23, 26), (23, 27), (23, 28), (23, 29), (24, 25), (24, 26), (24, 27), (24, 28), (24, 29), (25, 26), (25, 27), (25, 28), (25, 29), (26, 27), (26, 28), (26, 29), (27, 28), (27, 29), (28, 29)]
        ball_timers_dict = {}
        for index_combo in index_combo_list:
            recent_collision = False
            ball_timers_dict[index_combo] = recent_collision
        self._ball_timers_dict = ball_timers_dict
    def _check_if_new_ball_overlapping_with_existing_balls(self, new_ball, ball_list):
        for ball in ball_list:
            overlapping = self._ball_ball_collision(new_ball, ball)
            if overlapping:
                return True
        return False
    def _make_random_ball(self, n):
        XY = RND(0.1, 0.9), RND(0.1, 0.9)
        R = RND(0.03, 0.05)
        V = RND(15, 35) / 10000
        C = PICK(select_colors)
        BALL = Ball(number=n, center=XY, radius=(R, R), velocity=(V, V), color=C)
        return BALL
    def __SETUP__window(self):
        self._root_window = tkinter.Tk()
        self._canvas = tkinter.Canvas(master=self._root_window, background=self._bg_color, highlightthickness=0, height=400, width=400)
        self._canvas.grid(column=0, row=0, sticky=N + S + E + W)
        self._root_window.columnconfigure(index=0, weight=1)
        self._root_window.rowconfigure(index=0, weight=1)
    def __SETUP__controls(self):
        self._root_window.bind('<Configure>',   self._on_configure)
        self._root_window.bind('<Button-1>',    self._on_mouse_click)
    def _trace_ball_position(self):
        for ball in self.balls:
            x, y = ball.center_xy
            print('{:20} : ( {:.2f} , {:.2f} )'.format(ball.color, x, y))
        print()
    def GO(self):
        if not self._CLICK_PAUSE and not self._RESIZE_PAUSE:
            self._canvas.delete(tkinter.ALL)
            self._ball_WALL_collision_main()
            self._ball_BALL_collision_main()
            self._change_ball_position()
            self._draw_balls()
            self._trace_ball_position()
            self._root_window.update_idletasks()
        self._root_window.after(self._mSPF, self.GO)
    def _draw_balls(self):
        for ball in self.balls:
            X0, Y0, X1, Y1 = Oval(ball.center_xy, ball.radius_xy).all()
            X0, Y0 = Coordinate((X0, Y0)).absolute(self._get_WH())
            X1, Y1 = Coordinate((X1, Y1)).absolute(self._get_WH())
            self._canvas.create_oval(X0, Y0, X1, Y1, fill=ball.color)
    def _change_ball_position(self):
        for ball in self.balls:
            x, y = ball.center_xy
            dx, dy = ball.velocity_xy
            ball.center_xy = (x + dx, y + dy)
    def _ball_WALL_collision_main(self):
        for i in range(0, len(self.balls)):
            ball = self.balls[i]
            x, y = ball.center_xy
            rx, ry = ball.radius_xy
            dx, dy = ball.velocity_xy
            if self._ball_wall_collision(x, rx):
                if self._recent_wall_collision(ball) == False:
                    dx *= -1
                    ball.start_wall_collision_timer()
            if self._ball_wall_collision(y, ry):
                if self._recent_wall_collision(ball) == False:
                    dy *= -1
                    ball.start_wall_collision_timer()
            ball.velocity_xy = (dx, dy)
            self.balls[i] = ball
    def _ball_wall_collision(self, z, rz):
        if z - rz < 0:
            return True
        elif z + rz > 1:
            return True
        else:
            return False
    def _recent_wall_collision(self, ball):
        return ball.recent_wall_collision
    def _ball_BALL_collision_main(self):
        index_combo_list = list(combinations(range(0, len(self.balls)), 2))
        for i, j in index_combo_list:
            ball_A = self.balls[i]
            ball_B = self.balls[j]
            DX, DY = ball_A.velocity_xy
            dx, dy = ball_B.velocity_xy
            collision = self._ball_ball_collision(ball_A, ball_B)
            if collision:
                if self._recent_ball_collision(ball_A) == False:
                    ball_A.start_ball_collision_timer()
                    DX, DY = DX * -1, DY * -1
                if self._recent_ball_collision(ball_B) == False:
                    ball_B.start_ball_collision_timer()
                    dx, dy = dx * -1, dy * -1
            ball_A.velocity_xy = DX, DY
            ball_B.velocity_xy = dx, dy
            self.balls[i] = ball_A
            self.balls[j] = ball_B
    def _ball_ball_collision(self, ball_A, ball_B):
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
    def _recent_ball_collision(self, ball):
        return ball.recent_ball_collision
    def _set_collision_timer_bool_to_True(self, ij):
        self._ball_timers_dict[(ij)] = True
    def _set_collision_timer_bool_to_False(self, ij):
        self._ball_timers_dict[(ij)] = False
    def _random_direction_change_for_ball_ball_collision(self, DXDYdxdy):
        DX, DY, dx, dy = DXDYdxdy
        choices = ['XY', 'XY', 'XY']
        choice = PICK(choices)
        if choice == 'X':
            DX, dx = DX * -1, dx * -1
            DY, dy = DY,    dy
        elif choice == 'Y':
            DX, dx = DX,    dx
            DY, dy = DY * -1, dy * -1
        elif choice == 'XY':
            DX, dx = DX * -1, dx * -1
            DY, dy = DY * -1, dy * -1
        return (DX, DY, dx, dy)
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
