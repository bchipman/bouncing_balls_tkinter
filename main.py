import tkinter
from tkinter import N, S, E, W
from random import uniform as RND
from random import choice as PICK
from copy import deepcopy
from threading import Timer
from itertools import combinations
from tk_colors import select_colors
from functools import partial
from coordinate import Coordinate, Oval
class View:
    def __init__(self):
        self.__SETUP__variables()
        self.__SETUP__window()
        self.__SETUP__controls()
    def __SETUP__variables(self):
        self._bg_color = 'grey'
        self._FPS = 100
        self._mSPF = self._FPS_to_mSPF(self._FPS)
        self._CLICK_PAUSE = False
        self._RESIZE_PAUSE = False
    def __SETUP__window(self):
        self._root_window = tkinter.Tk()
        self._canvas = tkinter.Canvas(master=self._root_window, background=self._bg_color, highlightthickness=0, height=400, width=400)
        self._canvas.grid(column=0, row=0, sticky=N + S + E + W)
        self._root_window.columnconfigure(index=0, weight=1)
        self._root_window.rowconfigure(index=0, weight=1)
    def __SETUP__controls(self):
        self._root_window.bind('<Configure>',   self.__CTRL__on_configure)
        self._root_window.bind('<Button-1>',    self.__CTRL__on_mouse_click_left)
    def __CTRL__on_configure(self, event):
        self._RESIZE_PAUSE = True
        t = Timer(0.5, self._set_resizing_to_false)
        t.start()
    def _set_resizing_to_false(self):
        self._RESIZE_PAUSE = False
    def __CTRL__on_mouse_click_left(self, event):
        if self._CLICK_PAUSE == True:
            self._CLICK_PAUSE = False
        elif self._CLICK_PAUSE == False:
            self._CLICK_PAUSE = True
    def _FPS_to_mSPF(self, FPS):
        return int((1 / FPS) * 1000)
    def _get_WH(self):
        return (self._root_window.winfo_width(), self._root_window.winfo_height())
    def draw_balls(self, balls):
        for ball in balls:
            X0, Y0, X1, Y1 = Oval(ball.center_xy, ball.radius_xy).all()
            X0, Y0 = Coordinate((X0, Y0)).absolute(self._get_WH())
            X1, Y1 = Coordinate((X1, Y1)).absolute(self._get_WH())
            self._canvas.create_oval(X0, Y0, X1, Y1, fill=ball.color)
    def trace_ball_position(self, balls):
        for ball in balls:
            x, y = ball.center_xy
            print('{:20} : ( {:.2f} , {:.2f} )'.format(ball.color, x, y))
        print()
    def GO(self, balls, trace=False):
        if not self._CLICK_PAUSE and not self._RESIZE_PAUSE:
            self._canvas.delete(tkinter.ALL)
            self.draw_balls(balls)
            if trace:
                self.trace_ball_position(balls)
            self._root_window.update_idletasks()
    def MAINLOOP(self):
        self._root_window.mainloop()
class Model:
    def __init__(self):
        self.__SETUP__model_variables()
        self.__SETUP__balls()
        self.__SETUP__collision_timer_dictionary()
        self.__SETUP__add_ball_wall_entries_to_collision_timer_dictionary()
    def __SETUP__model_variables(self):
        self.num_balls = 25
    def __SETUP__balls(self):
        ball_list = []
        for n in range(0, self.num_balls):
            while True:
                new_ball = self.__SETUP__balls__make_random_ball(n)
                new_ball_OK = not self.__SETUP__balls__check_if_new_ball_overlapping_with_existing_balls(new_ball, ball_list)
                if new_ball_OK:
                    break
            ball_list.append(new_ball)
        self.balls = ball_list
    def __SETUP__collision_timer_dictionary(self):
        index_combo_list = list(combinations(range(0, len(self.balls)), 2))
        ball_timers_dict = {}
        for index_combo in index_combo_list:
            recent_collision = False
            ball_timers_dict[index_combo] = recent_collision
        self._ball_timers_dict = ball_timers_dict
    def __SETUP__add_ball_wall_entries_to_collision_timer_dictionary(self):
        di_copy = deepcopy(self._ball_timers_dict)
        del self._ball_timers_dict
        for n in range(0, len(self.balls)):
            di_copy[(n, 'NS')] = False
            di_copy[(n, 'EW')] = False
        self._ball_timers_dict = deepcopy(di_copy)
        del di_copy
    def __SETUP__balls__make_random_ball(self, n):
        XY = RND(0.1, 0.9), RND(0.1, 0.9)
        R = RND(0.03, 0.05)
        V = RND(15, 35) / 10000
        C = PICK(select_colors)
        return Ball(number=n, center=XY, radius=(R, R), velocity=(V, V), color=C)
    def __SETUP__balls__check_if_new_ball_overlapping_with_existing_balls(self, new_ball, ball_list):
        for ball in ball_list:
            overlapping = self._ball_ball_collision(new_ball, ball)
            if overlapping:
                return True
        return False
    def _change_position_of_balls(self):
        for ball in self.balls:
            ball.move()
    def MOVE(self):
        self._handle_wall_collision()
        self._ball_BALL_collision_main()
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
                DX, DY = DX * -1, DY * -1
                dx, dy = dx * -1, dy * -1
            ball_A.velocity_xy = DX, DY
            ball_B.velocity_xy = dx, dy
            self.balls[i] = ball_A
            self.balls[j] = ball_B
    def _ball_BALL_collision_main(self):
        index_combo_list = list(combinations(range(0, len(self.balls)), 2))
        for i, j in index_combo_list:
            ball_A = self.balls[i]
            ball_B = self.balls[j]
            DX, DY = ball_A.velocity_xy
            dx, dy = ball_B.velocity_xy
            collision = self._ball_ball_collision(ball_A, ball_B)
            if collision:
                if self._recent_ball_collision((i, j)) == False:
                    self._set_ball_collision_timer_bool_to_True((i, j))
                    timer = Timer(3, partial(self._set_ball_collision_timer_bool_to_False, ij=(i, j)))
                    timer.start()
                    DX, DY = DX * -1, DY * -1
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
    def _recent_ball_collision(self, ij):
        return self._ball_timers_dict[(ij)]
    def _set_ball_collision_timer_bool_to_True(self, ij):
        self._ball_timers_dict[(ij)] = True
    def _set_ball_collision_timer_bool_to_False(self, ij):
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
class Ball:
    def __init__(self, number, center, radius, velocity, color):
        self.number = number
        self.center_xy = center
        self.radius_xy = radius
        self.velocity_xy = velocity
        self.color = color
        self.edges = self._calculate_edge_values()
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
    def _calculate_edge_values(self):
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
        self.edges = self._calculate_edge_values()
class Game:
    def __init__(self):
        self.game_model = Model()
        self.game_view = View()
    def _play_game(self):
        balls = self.game_model.MOVE()
        self.game_view.GO(balls)
        self.game_view._root_window.after(self.game_view._mSPF, self._play_game)
    def START(self):
        self._play_game()
        self.game_view.MAINLOOP()
if __name__ == '__main__':
    Game().START()
