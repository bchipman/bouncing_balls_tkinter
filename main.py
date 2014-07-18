from collections import namedtuple
from functools import partial
from itertools import combinations
from random import choice as PICK
from random import uniform as RND
import sys
from threading import Timer
from tkinter import N, S, E, W
import tkinter
import calculations
from coordinate import Coordinate, Oval
from random_seeds import BallOptionsSeeded
import random_seeds
from tk_colors import all_colors as colors
WindowOptions = namedtuple('WindowOptions', 'bg, fps, trace_xy, trace_hits, trace_n')
BallOptionsRandom = namedtuple('BallOptionsRandom', 'N, XY, R, V')
CollisionOptions = namedtuple('CollisionOptions', 'trace')
class Game:
    def __init__(self, window_options, ball_options, collision_options):
        self.window_options = window_options
        self.ball_options = ball_options
        self.collision_options = collision_options
        self.game_window = Window(self.window_options)
        self.balls = Balls(self.ball_options)
        self.collisions = Collisions(self.balls.ball_list, self.collision_options)
        self.collision_handler = CollisionHandler(self.balls.ball_list)
    def GAME_LOOP(self):
        ball_list = self.collision_handler(self.balls.ball_list, self.collisions)
        ball_list = self.balls.advance_ball_positions(ball_list)
        self.game_window.DRAW_BALLS(ball_list)
        self.game_window.root_window.after(self.game_window._mSPF, self.GAME_LOOP)
    def START(self):
        self.GAME_LOOP()
        self.game_window.root_window.mainloop()
class Window:
    def __init__(self, options):
        self._SETUP_variables(options)
        self._SETUP_window()
        self._SETUP_controls()
    def _SETUP_variables(self, options):
        self._bg_color = options.bg
        self._FPS = options.fps
        self._trace_xy = options.trace_xy
        self._trace_hits = options.trace_hits
        self._trace_n = options.trace_n
        self._mSPF = calculations.mSPF_from_FPS(self._FPS)
        self._CLICK_PAUSE = False
        self._RESIZE_PAUSE = False
    def _SETUP_window(self):
        self.root_window = tkinter.Tk()
        self._canvas = tkinter.Canvas(master=self.root_window, background=self._bg_color, highlightthickness=0, height=600, width=600)
        self._canvas.grid(column=0, row=0, sticky=N + S + E + W)
        self.root_window.columnconfigure(index=0, weight=1)
        self.root_window.rowconfigure(index=0, weight=1)
    def _SETUP_controls(self):
        self.root_window.bind('<Configure>', self._CTRL_on_configure)
        self.root_window.bind('<Button-1>', self._CTRL_on_mouse_click_left)
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
    def _GET_WH(self):
        return (self.root_window.winfo_width(), self.root_window.winfo_height())
    def DRAW_BALLS(self, ball_list):
        if not self._CLICK_PAUSE and not self._RESIZE_PAUSE:
            self._canvas.delete(tkinter.ALL)
            for ball in ball_list:
                self._draw_ball(ball)
                if self._trace_xy:
                    self._trace_ball_position(ball, len(ball_list) - 1)
                if self._trace_hits:
                    self._trace_number_hits(ball)
                if self._trace_n:
                    self._trace_ball_number(ball)
            self.root_window.update_idletasks()
    def _draw_ball(self, ball):
        X1, Y1, X2, Y2 = Oval(ball.position, ball.radius).all()
        X1, Y1 = Coordinate((X1, Y1)).absolute(self._GET_WH())
        X2, Y2 = Coordinate((X2, Y2)).absolute(self._GET_WH())
        self._canvas.create_oval(X1, Y1, X2, Y2, fill=ball.color)
    def _trace_ball_position(self, ball, num_balls):
        x, y = ball.position
        print('{:20} : ( {:.2f} , {:.2f} )'.format(ball.color, x, y))
        if ball.n == num_balls:
            print()
    def _trace_number_hits(self, ball):
        X0, Y0 = Coordinate(ball.position).absolute(self._GET_WH())
        total_hits = ball.total_hits
        self._canvas.create_text(X0, Y0, text=total_hits)
        pass
    def _trace_ball_number(self, ball):
        X0, Y0 = Coordinate(ball.position).absolute(self._GET_WH())
        self._canvas.create_text(X0, Y0, text=ball.n)
    def _draw_arc(self, ball):
        pass
class Balls:
    def __init__(self, options):
        self.N = options.N
        self.options = options
        self.ball_list = self.__SETUP__balls()
    def __SETUP__balls(self):
        ball_list = []
        for n in range(0, self.N):
            while True:
                new_ball = self._create_random_ball(n)
                new_ball_XY_OK = not self._new_ball_overlaps_with_existing_ball(new_ball, ball_list)
                new_ball_color_OK = not self._new_ball_same_color_as_existing_ball(new_ball, ball_list)
                if new_ball_XY_OK and new_ball_color_OK:
                    break
            ball_list.append(new_ball)
        return ball_list
    def _create_random_ball(self, n):
        print(type(self.options))
        print(type(self.options) == BallOptionsRandom)
        print(type(self.options) == BallOptionsSeeded)
        if type(self.options) == BallOptionsRandom:
            xy, XY = self.options.XY
            r, R = self.options.R
            v, V = self.options.V
            X = RND(xy, XY)
            Y = RND(xy, XY)
            R = RND(r, R)
            V = RND(v, V)
            V = PICK([V, V * -1])
            C = PICK(colors)
            return Ball(number=n, center=(X, Y), radius=(R, R), velocity=(V, V), color=C)
        elif type(self.options) == BallOptionsSeeded:
            X = self.options.X[n]
            Y = self.options.Y[n]
            R = self.options.R[n]
            V = self.options.V[n]
            C = self.options.C[n]
            return Ball(number=n, center=(X, Y), radius=(R, R), velocity=(V, V), color=C)
    def _new_ball_overlaps_with_existing_ball(self, new_ball, ball_list):
        for ball in ball_list:
            overlapping = CollisionHandler._ball_collision(self, new_ball, ball)
            if overlapping:
                return True
        return False
    def _new_ball_same_color_as_existing_ball(self, new_ball, ball_list):
        for ball in ball_list:
            if ball.color == new_ball.color:
                return True
        return False
    def advance_ball_positions(self, ball_list):
        self.ball_list = ball_list
        for ball in self.ball_list:
            ball.move()
        return self.ball_list
class Ball:
    def __init__(self, number, center, radius, velocity, color):
        self.n = number
        self.position = center
        self.radius = radius
        self.velocity = velocity
        self.color = color
        self.edges = calculations.ball_edge_values(self.position, self.radius)
        self.last_hit = self
        self.number_hit = 0
        self.total_hits = 0
    def __str__(self):
        n = '{:<2}'.format(self.n)
        number = 'Ball ' + n
        clr = '{:20}'.format(self.color)
        color = 'Color: ' + clr
        rx, ry = self.radius
        rx = '{:.3f}'.format(rx)
        ry = '{:.3f}'.format(ry)
        radius = 'Radius: ' + rx + ', ' + ry
        dx, dy = self.velocity
        dx = '{:.3f}'.format(dx)
        dy = '{:.3f}'.format(dy)
        velocity = 'Velocity: ' + dx + ', ' + dy
        x, y = self.position
        x = '{:.3f}'.format(x)
        y = '{:.3f}'.format(y)
        position = 'Position: ' + x + ', ' + y
        return '      '.join([number, position, radius, velocity, color])
    def move(self):
        x, y = self.position
        dx, dy = self.velocity
        self.position = (x + dx, y + dy)
        self.edges = calculations.ball_edge_values(self.position, self.radius)
    def increment_last_hit(self):
        self.number_hit += 1
        self.total_hits += 1
    def set_new_last_hit(self, ball):
        self.last_hit = ball
        self.number_hit = 1
        self.total_hits += 1
class CollisionHandler:
    def __init__(self, ball_list):
        self.list_hits_last_50_frames = [[] for i in range(0, 50)]
        self.counted_hits_last_50_frames = {}
        self.hits_this_frame = []
        self.threshold = 5
        self.ball_color_list = self._get_ball_color_list(ball_list)
    def _get_ball_color_list(self, ball_list):
        li = []
        for b in ball_list:
            li.append(b.color)
        return li
    def __call__(self, ball_list, collisions):
        self._reset()
        self._count_number_of_same_hits_in_last_50_frames()
        self._count_all_number_same_hits_in_last_50_frames_above_threshold()
        self._change_ball_color_if_above_threshold(ball_list)
        ball_list = self._handle_wall_collision(ball_list)
        ball_list = self._handle_ball_collision(ball_list, collisions)
        self._update_hits_for_last_50_frames_list()
        return ball_list
    def _reset(self):
        self.hits_this_frame = []
        del self.counted_hits_last_50_frames
        self.counted_hits_last_50_frames = {}
    def _count_number_of_same_hits_in_last_50_frames(self):
        count_di = {}
        for hit_list in self.list_hits_last_50_frames:
            for balltuple in hit_list:
                if balltuple not in count_di.keys():
                    count_di[balltuple] = 1
                elif balltuple in count_di.keys():
                    count_di[balltuple] += 1
        self.counted_hits_last_50_frames = count_di
        del count_di
    def _count_all_number_same_hits_in_last_50_frames_above_threshold(self):
        li = []
        for ij in self.counted_hits_last_50_frames.keys():
            if self.counted_hits_last_50_frames[ij] > self.threshold:
                li.append(ij)
        self.above_threshold_this_frame = li
        print(self.above_threshold_this_frame)
    def _change_ball_color_if_above_threshold(self, ball_list):
        uniques = set()
        for i, j in self.above_threshold_this_frame:
            uniques.add(i)
            uniques.add(j)
        for ball in ball_list:
            if ball.n in uniques:
                ball.color = 'yellow'
                print('!')
            else:
                ball.color = self.ball_color_list[ball.n]
        del uniques
    def _handle_wall_collision(self, ball_list):
        for i in range(0, len(ball_list)):
            ball = ball_list[i]
            Up, Dn, L, R = ball.edges
            dx, dy = ball.velocity
            if Up < 0:
                dy = max(dy, dy * -1)
            if Dn > 1:
                dy = min(dy, dy * -1)
            if L < 0:
                dx = max(dx, dx * -1)
            if R > 1:
                dx = min(dx, dx * -1)
            ball.velocity = (dx, dy)
            ball_list[i] = ball
        return ball_list
    def _handle_ball_collision(self, ball_list, collisions):
        index_combo_list = list(combinations(range(0, len(ball_list)), 2))
        for i, j in index_combo_list:
            ball_A, ball_B = ball_list[i], ball_list[j]
            DX, DY = ball_A.velocity
            dx, dy = ball_B.velocity
            if self._ball_collision(ball_A, ball_B):
                self._add_to_hits_this_frame_li(ball_A, ball_B)
                if not self._above_threshold_this_frame(ball_A, ball_B):
                    DXDY, dxdy = calculations.new_velocity(ball_A, ball_B)
                    DX, DY = DXDY
                    dx, dy = dxdy
            ball_A.velocity = DX, DY
            ball_B.velocity = dx, dy
            ball_list[i] = ball_A
            ball_list[j] = ball_B
        return ball_list
    def _ball_collision(self, ball_A, ball_B):
        X, Y = ball_A.position
        R = ball_A.radius[0]
        x, y = ball_B.position
        r = ball_B.radius[0]
        Rr_sum_sqd = (R + r) ** 2
        D_sqd = (X - x) ** 2 + (Y - y) ** 2
        if D_sqd < Rr_sum_sqd:
            return True
        else:
            return False
    def _add_to_hits_this_frame_li(self, ball_A, ball_B):
        ij = calculations.ball_order(ball_A, ball_B)
        self.hits_this_frame.append(ij)
    def _above_threshold_this_frame(self, ball_A, ball_B):
        ij = calculations.ball_order(ball_A, ball_B)
        if ij in self.above_threshold_this_frame:
            return True
        return False
    def _update_hits_for_last_50_frames_list(self):
        if len(self.hits_this_frame) > 0:
            self.list_hits_last_50_frames = self.list_hits_last_50_frames[1::] + [self.hits_this_frame]
class Collisions:
    def __init__(self, ball_list, options):
        self.trace = options.trace
        self.di = self.new(ball_list)
    def new(self, ball_list):
        index_combo_list = list(combinations(range(0, len(ball_list)), 2))
        di = {}
        for index_combo in index_combo_list:
            currently_blacklisted = False
            di[index_combo] = currently_blacklisted
        return di
    def get(self, ij):
        return self.di[ij]
    def set(self, ij, TF):
        self.di[ij] = TF
if __name__ == '__main__':
    window_options = WindowOptions(bg='grey', fps=100, trace_xy=False, trace_hits=False, trace_n=True)
    ball_options = BallOptionsRandom(N=25, XY=(0.01, 0.99), R=(0.03, 0.05), V=(0.0005, 0.0075))
    collision_options = CollisionOptions(trace=False)
    game = Game(window_options, ball_options, collision_options)
    game.START()
