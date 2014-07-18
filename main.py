from functools import partial
from itertools import combinations
from math import sqrt
from coordinate import Coordinate, Oval
from random import choice as PICK
from random import uniform as RND
from threading import Timer
from tk_colors import select_colors
from tkinter import N, S, E, W
import tkinter
class Window:
    def __init__(self):
        self._SETUP_variables()
        self._SETUP_window()
        self._SETUP_controls()
    def _SETUP_variables(self):
        self._bg_color = 'grey'
        self._FPS = 100
        self._mSPF = self._CALC_FPS_to_mSPF(self._FPS)
        self._CLICK_PAUSE = False
        self._RESIZE_PAUSE = False
    def _SETUP_window(self):
        self._root_window = tkinter.Tk()
        self._canvas = tkinter.Canvas(master=self._root_window, background=self._bg_color, highlightthickness=0, height=400, width=400)
        self._canvas.grid(column=0, row=0, sticky=N + S + E + W)
        self._root_window.columnconfigure(index=0, weight=1)
        self._root_window.rowconfigure(index=0, weight=1)
    def _SETUP_controls(self):
        self._root_window.bind('<Configure>',   self._CTRL_on_configure)
        self._root_window.bind('<Button-1>',    self._CTRL_on_mouse_click_left)
    def _CTRL_on_configure(self, event):
        self._RESIZE_PAUSE = True
        t = Timer(0.5, self._CTRL_on_configure_set_resize_pause)
        t.start()
    def _CTRL_on_configure_set_resize_pause(self):
        self._RESIZE_PAUSE = False
    def _CTRL_on_mouse_click_left(self, event):
        if self._CLICK_PAUSE == True:
            self._CLICK_PAUSE = False
        elif self._CLICK_PAUSE == False:
            self._CLICK_PAUSE = True
    def _CALC_FPS_to_mSPF(self, FPS):
        return int((1 / FPS) * 1000)
    def _GET_WH(self):
        return (self._root_window.winfo_width(), self._root_window.winfo_height())
    def _DO_draw_balls(self, balls):
        for ball in balls:
            X0, Y0, X1, Y1 = Oval(ball.center_xy, ball.radius_xy).all()
            X0, Y0 = Coordinate((X0, Y0)).absolute(self._GET_WH())
            X1, Y1 = Coordinate((X1, Y1)).absolute(self._GET_WH())
            self._canvas.create_oval(X0, Y0, X1, Y1, fill=ball.color)
    def _DEBUG_trace_ball_position(self, balls):
        for ball in balls:
            x, y = ball.center_xy
            print('{:20} : ( {:.2f} , {:.2f} )'.format(ball.color, x, y))
        print()
    def GO(self, balls, trace=False):
        if not self._CLICK_PAUSE and not self._RESIZE_PAUSE:
            self._canvas.delete(tkinter.ALL)
            self._DO_draw_balls(balls)
            if trace:
                self._DEBUG_trace_ball_position(balls)
            self._root_window.update_idletasks()
    def MAINLOOP(self):
        self._root_window.mainloop()
class Logic:
    def __init__(self):
        self._num_balls = 25
        self.__SETUP__balls()
        self.__SETUP__collision_dictionary()
    def __SETUP__balls(self):
        ball_list = []
        for n in range(0, self._num_balls):
            while True:
                new_ball = self.__SETUP__balls__make_random_ball(n)
                new_ball_XY_OK = not self.__SETUP__balls__check_if_new_ball_overlapping_with_existing_balls(new_ball, ball_list)
                new_ball_color_OK = not self.__SETUP__balls__check_if_new_ball_same_color_as_an_existing_balls(new_ball, ball_list)
                if new_ball_XY_OK and new_ball_color_OK:
                    break
            ball_list.append(new_ball)
        self.balls = ball_list
    def __SETUP__balls__make_random_ball(self, n):
        XY = RND(0.1, 0.9), RND(0.1, 0.9)
        R = RND(0.03, 0.05)
        V = RND(15, 35) / 10000
        V = PICK([V, V * -1])
        C = PICK(select_colors)
        return Ball(number=n, center=XY, radius=(R, R), velocity=(V, V), color=C)
    def __SETUP__balls__check_if_new_ball_overlapping_with_existing_balls(self, new_ball, ball_list):
        for ball in ball_list:
            overlapping = self._ball_ball_collision(new_ball, ball)
            if overlapping:
                return True
        return False
    def __SETUP__balls__check_if_new_ball_same_color_as_an_existing_balls(self, new_ball, ball_list):
        for ball in ball_list:
            if ball.color == new_ball.color:
                return True
        return False
    def __SETUP__collision_dictionary(self):
        index_combo_list = list(combinations(range(0, len(self.balls)), 2))
        ball_collision_dict = {}
        for index_combo in index_combo_list:
            currently_blacklisted = False
            ball_collision_dict[index_combo] = currently_blacklisted
        self._ball_collision_dict = ball_collision_dict
    def _change_position_of_balls(self):
        for ball in self.balls:
            ball.move()
    def MOVE(self):
        self._handle_wall_collision()
        self._handle_ball_collision()
        self._change_position_of_balls()
        return self.balls
    def _handle_wall_collision(self):
        for i in range(0, len(self.balls)):
            ball = self.balls[i]
            Up, Dn, L, R = ball.edges
            dx, dy = ball.velocity_xy
            if Up < 0:
                dy = max(dy, dy * -1)
            if Dn > 1:
                dy = min(dy, dy * -1)
            if L < 0:
                dx = max(dx, dx * -1)
            if R > 1:
                dx = min(dx, dx * -1)
            ball.velocity_xy = (dx, dy)
            self.balls[i] = ball
    def _handle_ball_collision(self):
        index_combo_list = list(combinations(range(0, len(self.balls)), 2))
        for i, j in index_combo_list:
            ball_A = self.balls[i]
            ball_B = self.balls[j]
            DX, DY = ball_A.velocity_xy
            dx, dy = ball_B.velocity_xy
            collision = self._ball_ball_collision(ball_A, ball_B)
            if collision:
                ball_A, ball_B = self._update_last_hits(ball_A, ball_B)
                blacklisted = self._blacklist(ball_A, ball_B)
                if not blacklisted:
                    DXDY, dxdy = self._CALC_new_velocity(ball_A, ball_B)
                    DX, DY = DXDY
                    dx, dy = dxdy
            ball_A.velocity_xy = DX, DY
            ball_B.velocity_xy = dx, dy
            self.balls[i] = ball_A
            self.balls[j] = ball_B
    def _CALC_new_velocity(self, ball_A, ball_B):
        x1, y1 = ball_A.center_xy
        x2, y2 = ball_B.center_xy
        v1 = ball_A.velocity_xy
        v2 = ball_B.velocity_xy
        m1 = 1
        m2 = 1
        n = x1 - x2, y1 - y2  # normal vector
        n_mag = sqrt(n[0] ** 2 + n[1] ** 2)  # magnitude of normal vector
        un = n[0] / n_mag, n[1] / n_mag  # unit vector of n
        ut = -1 * un[1], un[0]  # unit tangent vector of n
        v1n = self._CALC_dot_product(un, v1)
        v1t = self._CALC_dot_product(ut, v1)
        v2n = self._CALC_dot_product(un, v2)
        v2t = self._CALC_dot_product(ut, v2)
        v1t_ = v1t
        v2t_ = v2t
        v1n_ = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
        v2n_ = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)
        v1n__ = (un[0] * v1n_, un[1] * v1n_)
        v1t__ = (ut[0] * v1t_, ut[1] * v1t_)
        v2n__ = (un[0] * v2n_, un[1] * v2n_)
        v2t__ = (ut[0] * v2t_, ut[1] * v2t_)
        _v1_ = v1n__[0] + v1t__[0], v1n__[1] + v1t__[1]
        _v2_ = v2n__[0] + v2t__[0], v2n__[1] + v2t__[1]
        return (_v1_, _v2_)
    def _CALC_dot_product(self, vector_1, vector_2):
        x, y = vector_1
        X, Y = vector_2
        return x * X + y * Y
    def _ball_ball_collision(self, ball_A, ball_B):
        X, Y = ball_A.center_xy
        R = ball_A.radius_xy[0]
        x, y = ball_B.center_xy
        r = ball_B.radius_xy[0]
        Rr_sum_sqd = (R + r) ** 2
        D_sqd = (X - x) ** 2 + (Y - y) ** 2
        if D_sqd < Rr_sum_sqd:
            last_hit_for_A = '{:2}-{:20}'.format(str(ball_A.last_hit.number), ball_A.last_hit.color)
            last_hit_for_B = '{:2}-{:20}'.format(str(ball_B.last_hit.number), ball_B.last_hit.color)
            A = 'A: {:2}-{:20} Last Hit: {} Total Hits: {}'.format(ball_A.number, ball_A.color, last_hit_for_A, ball_A.number_hit)
            B = 'B: {:2}-{:20} Last Hit: {} Total Hits: {}'.format(ball_B.number, ball_B.color, last_hit_for_B, ball_B.number_hit)
            print(A, B, sep='\t')
            return True
        else:
            return False
    def _update_last_hits(self, ball_A, ball_B):
        if ball_A.last_hit == ball_B:
            ball_A.increment_last_hit()
        else:
            ball_A.set_new_last_hit(ball_B)
        if ball_B.last_hit == ball_A:
            ball_B.increment_last_hit()
        else:
            ball_B.set_new_last_hit(ball_A)
        return (ball_A, ball_B)
    def _blacklist(self, ball_A, ball_B):
        ij = min(ball_A.number, ball_B.number), max(ball_A.number, ball_B.number)
        if ball_A.number_hit > 10 and ball_B.number_hit > 10:
            A = '{}-{}'.format(ball_A.number, ball_A.color)
            B = '{}-{}'.format(ball_B.number, ball_B.color)
            star = '*' * 20
            print('{} BREAKING {} and {}!! {}'.format(star, A, B, star))
            self._set_ball_collision_timer_bool(ij, True)
            t = Timer(5, partial(self._set_ball_collision_timer_bool, ij, False))
            t.start()
        return self._ball_collision_dict[ij]
    def _set_ball_collision_timer_bool(self, ij, TF):
        self._ball_collision_dict[(ij)] = TF
class Ball:
    def __init__(self, number, center, radius, velocity, color):
        self.number = number
        self.center_xy = center
        self.radius_xy = radius
        self.velocity_xy = velocity
        self.color = color
        self.edges = self._CALC_edge_values()
        self.last_hit = self
        self.number_hit = 0
        self.blacklist = []
    def __str__(self):
        n = '{:<2}'.format(self.number)
        number = 'Ball ' + n
        clr = '{:20}'.format(self.color)
        color = 'Color: ' + clr
        rx, ry = self.radius_xy
        rx = '{:.3f}'.format(rx)
        ry = '{:.3f}'.format(ry)
        radius = 'Radius: ' + rx + ', ' + ry
        dx, dy = self.velocity_xy
        dx = '{:.3f}'.format(dx)
        dy = '{:.3f}'.format(dy)
        velocity = 'Velocity: ' + dx + ', ' + dy
        x, y = self.center_xy
        x = '{:.3f}'.format(x)
        y = '{:.3f}'.format(y)
        position = 'Position: ' + x + ', ' + y
        return '      '.join([number, position, radius, velocity, color])
    def _CALC_edge_values(self):
        x, y = self.center_xy
        rx, ry = self.radius_xy
        U = y - ry
        D = y + ry
        L = x - rx
        R = x + rx
        return (U, D, L, R)
    def move(self):
        x, y = self.center_xy
        dx, dy = self.velocity_xy
        self.center_xy = (x + dx, y + dy)
        self.edges = self._CALC_edge_values()
    def increment_last_hit(self):
        self.number_hit += 1
    def set_new_last_hit(self, ball):
        self.last_hit = ball
        self.number_hit = 1
class Game:
    def __init__(self):
        self.game_logic = Logic()
        self.game_window = Window()
    def _play_game(self):
        balls = self.game_logic.MOVE()
        self.game_window.GO(balls)
        self.game_window._root_window.after(self.game_window._mSPF, self._play_game)
    def START(self):
        self._play_game()
        self.game_window.MAINLOOP()
Game().START()
