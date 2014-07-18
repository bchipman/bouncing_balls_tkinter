from collections import namedtuple
from functools import partial
from itertools import combinations
from random import choice as PICK
from random import uniform as RND
from threading import Timer
from tkinter import N, S, E, W
import tkinter
import calculations
from coordinate import Coordinate, Oval
from tk_colors import all_colors as colors
WindowOptions = namedtuple('WindowOptions',       'bg, fps, trace_xy, trace_hits')
BallOptions = namedtuple('BallOptions',         'N, XY, R, V')
CollisionOptions = namedtuple('CollisionOptions',    'trace')
class Game:
    def __init__(self, window_options, ball_options, collision_options):
        self.window_options = window_options
        self.ball_options = ball_options
        self.collision_options = collision_options
        self.game_window = Window(self.window_options)
        self.balls = Balls(self.ball_options)
        self.collisions = Collisions(self.balls.ball_list, self.collision_options)
    def GAME_LOOP(self):
        ball_list = CollisionHandler().handle_any_collisions(self.balls.ball_list, self.collisions)
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
        self.root_window.bind('<Configure>',   self._CTRL_on_configure)
        self.root_window.bind('<Button-1>',    self._CTRL_on_mouse_click_left)
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
            self.root_window.update_idletasks()
    def _draw_ball(self, ball):
        X1, Y1, X2, Y2 = Oval(ball.position, ball.radius).all()
        X1, Y1 = Coordinate((X1, Y1)).absolute(self._GET_WH())
        X2, Y2 = Coordinate((X2, Y2)).absolute(self._GET_WH())
        self._canvas.create_oval(X1, Y1, X2, Y2, fill=ball.color)
        self._canvas.create_arc(X1, Y1, X2, Y2)
    def _trace_ball_position(self, ball, num_balls):
        x, y = ball.position
        print('{:20} : ( {:.2f} , {:.2f} )'.format(ball.color, x, y))
        if ball.n == num_balls:
            print()
    def _trace_number_hits(self, ball):
        X0, Y0 = Coordinate(ball.position).absolute(self._GET_WH())
        total_hits = ball.total_hits
        self._canvas.create_text(X0, Y0, text=total_hits)
    def _draw_arc(self, ball):
        pass
class Balls:
    def __init__(self, options):
        self.N = options.N
        self.xy,    self.XY = options.XY
        self.r,     self.R = options.R
        self.v,     self.V = options.V
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
        X = RND(self.xy, self.XY)
        Y = RND(self.xy, self.XY)
        R = RND(self.r, self.R)
        V = RND(self.v, self.V)
        V = PICK([V, V * -1])
        C = PICK(colors)
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
    def handle_any_collisions(self, ball_list, collisions):
        ball_list = self._handle_wall_collision(ball_list)
        ball_list = self._handle_ball_collision(ball_list, collisions)
        return ball_list
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
                if collisions.trace:
                    self._trace_collisions(ball_A, ball_B)
                ball_A, ball_B = self._update_last_hits(ball_A, ball_B)
                if self._blacklist(ball_A, ball_B, collisions):
                    if collisions.trace:
                        self._trace_blacklisted_collisions(ball_A, ball_B)
                elif not self._blacklist(ball_A, ball_B, collisions):
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
    def _add_to_collisions_this_frame(self, ball_A, ball_B):
        ij = calculations.ball_order(ball_A, ball_B)
        self._collisions_this_frame_li.append(ij)
    def _update_colisions_in_recent_frames(self):
        pass
        pass
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
    def _blacklist(self, ball_A, ball_B, collisions):
        ij = calculations.ball_order(ball_A, ball_B)
        if ball_A.number_hit > 10 and ball_B.number_hit > 10:
            collisions.set(ij, True)
            t = Timer(1, partial(collisions.set, ij, False))
            t.start()
        return collisions.get(ij)
    def _trace_collisions(self, ball_A, ball_B):
        last_hit_for_A = '{:2}-{:20}'.format(str(ball_A.last_hit.n), ball_A.last_hit.color)
        last_hit_for_B = '{:2}-{:20}'.format(str(ball_B.last_hit.n), ball_B.last_hit.color)
        A = 'A: {:2}-{:20} Last Hit: {} Total Hits: {}'.format(ball_A.n, ball_A.color, last_hit_for_A, ball_A.number_hit)
        B = 'B: {:2}-{:20} Last Hit: {} Total Hits: {}'.format(ball_B.n, ball_B.color, last_hit_for_B, ball_B.number_hit)
        print(A, B, sep='\t')
    def _trace_blacklisted_collisions(self, ball_A, ball_B):
        A = '{}-{}'.format(ball_A.n, ball_A.color)
        B = '{}-{}'.format(ball_B.n, ball_B.color)
        star = '*' * 20
        print('{} BREAKING {} and {}!! {}'.format(star, A, B, star))
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
    window_options = WindowOptions(bg='grey', fps=100, trace_xy=False, trace_hits=True)
    ball_options = BallOptions(N=25, XY=(0.01, 0.99), R=(0.03, 0.05), V=(0.0005, 0.0075))
    collision_options = CollisionOptions(trace=False)
    game = Game(window_options, ball_options, collision_options)
    game.START()
