import tkinter
from tkinter import N, S, E, W
from coordinate import Coordinate, Oval
from random import uniform as R
from threading import Timer
class Ball:
    def __init__(self, center, radius, velocity, color):
        self.center_xy = center
        self.radius_xy = radius
        self.velocity_xy = velocity
        self.color = color
class Game:
    def __init__(self):
        self.__SETUP__variables()
        self.__SETUP__window()
        self.__SETUP__controls()
        self.GO()
        self._move_balls()
    def __SETUP__variables(self):
        self._bg_color = 'grey'
        R1, R2 = 0.08, (0.03)
        self._ball_1 = Ball(center=(R(0.1, 0.9), R(0.1, 0.9)), radius=(R1, R1), velocity=(10 / 10000, 14 / 10000), color='orange')
        self._ball_2 = Ball(center=(R(0.1, 0.9), R(0.1, 0.9)), radius=(R2, R2), velocity=(25 / 10000, 25 / 10000), color='green')
        self.balls = [self._ball_1, self._ball_2]
        self._FPS = 100
        self._CLICK_PAUSE = False
        self._RESIZE_PAUSE = False
        self._size_is_big = True
    def __SETUP__window(self):
        self._root_window = tkinter.Tk()
        self._root_window.aspect(1, 1, 1, 1)
        self._canvas = tkinter.Canvas(master=self._root_window, background=self._bg_color, highlightthickness=0, height=400, width=400)
        self._canvas.grid(column=0, row=0, sticky=N + S + E + W)
        self._root_window.columnconfigure(index=0, weight=1)
        self._root_window.rowconfigure(index=0, weight=1)
    def __SETUP__controls(self):
        self._root_window.bind('<Button-1>', self._on_mouse_click)
    def GO(self):
        self._move_balls()
        self._trace_ball_coordinates()
    def _trace_ball_coordinates(self):
        W, H = self._root_window.winfo_width(), self._root_window.winfo_height()
        canvasW, canvasH = self._canvas.winfo_width(), self._canvas.winfo_height()
        print('Window: {},{}    Canvas: {},{}'.format(W, H, canvasW, canvasH))
        print()
    def _move_balls(self):
        if not self._CLICK_PAUSE and not self._RESIZE_PAUSE:
            self._canvas.delete(tkinter.ALL)
            self._change_position_of_balls()
            self._check_if_any_ball_hit_wall()
            self._check_for_ball_ball_collision()
            self._draw_balls()
            self._trace_ball_coordinates()
            self._root_window.update_idletasks()
        ms_per_frame = self._FPS_to_mSPF(self._FPS)
        self._root_window.after(ms_per_frame, self._move_balls)
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
    def _check_for_ball_ball_collision(self):
        for ball_1 in self.balls:
            N, S, E, W = self._get_ball_edges(ball_1)
            DX, DY = ball_1.velocity_xy
            for ball_2 in self.balls:
                if ball_1 == ball_2:
                    pass
                else:
                    horizontal_hit, vertical_hit = False, False
                    n, s, e, w, = self._get_ball_edges(ball_2)
                    dx, dy = ball_2.velocity_xy
                    if (W <= e <= E) or (W <= w <= E):
                        horizontal_hit = True
                    if (N <= n <= S) or (N <= s <= S):
                        vertical_hit = True
                    if horizontal_hit and vertical_hit:
                        dx, DX = dx * -1, DX * -1
                        dy, DY = dy * -1, DY * -1
                    ball_1.velocity_xy = (DX, DY)
                    ball_2.velocity_xy = (dx, dy)
    def _get_canvas_WH(self):
        W, H = self._canvas.winfo_width(), self._canvas.winfo_height()
        return (W, H)
    def _get_WH(self):
        W, H = self._root_window.winfo_width(), self._root_window.winfo_height()
        canvasW, canvasH = self._canvas.winfo_width(), self._canvas.winfo_height()
        print('Window: {},{}    Canvas: {},{}'.format(W, H, canvasW, canvasH))
        return (self._root_window.winfo_width(), self._root_window.winfo_height())
    def _on_configure(self, event):
        pass
    def _set_resizing_to_false(self):
        self._RESIZE_PAUSE = False
    def _set_window_and_canvas_size(self, WH):
        W, H = WH
        self._canvas.configure(width=W, height=H)
    def _on_right_click(self, event):
        print('click!!')
        if self._size_is_big == True:
            self._root_window.configure(height=200, width=200)
            self._canvas.configure(height=200, width=200)
            self._size_is_big = False
        elif self._size_is_big == False:
            self._root_window.configure(height=800, width=800)
            self._canvas.configure(height=800, width=800)
            self._size_is_big = True
        self._root_window.update()
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
