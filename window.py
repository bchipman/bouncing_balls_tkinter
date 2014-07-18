import calculations
import coordinate
import threading
import tkinter
from tkinter import N, S, E, W
class Window:
    def __init__(self, options):
        self._options = options
        self._mSPF = calculations.mSPF_from_FPS(options.fps)
        self._CLICK_PAUSE = False
        self._RESIZE_PAUSE = False
        self._COLLISION_PAUSE = False
        self.root_window = tkinter.Tk()
        self._canvas = tkinter.Canvas(master=self.root_window, background=options.bg_color, highlightthickness=0, height=600, width=600)
        self._canvas.grid(column=0, row=0, sticky=N + S + E + W)
        self.root_window.columnconfigure(index=0, weight=1)
        self.root_window.rowconfigure(index=0, weight=1)
        self.root_window.bind('<Configure>',   self._on_configure)
        self.root_window.bind('<Button-1>',    self._on_mouse_click_left)
        self.root_window.bind('<space>', self._on_press_spacebar)
    def _on_configure(self, event):
        self._RESIZE_PAUSE = True
        t = threading.Timer(0.5, self._on_configure_set_resize_pause)
        t.start()
    def _on_configure_set_resize_pause(self):
        self._RESIZE_PAUSE = False
    def _on_mouse_click_left(self, event):
        if self._CLICK_PAUSE == True:
            self._CLICK_PAUSE = False
        elif self._CLICK_PAUSE == False:
            self._CLICK_PAUSE = True
    def _on_press_spacebar(self, event):
        if self._COLLISION_PAUSE == True:
            self._COLLISION_PAUSE = False
    def _get_WH(self):
        return (self.root_window.winfo_width(), self.root_window.winfo_height())
    def NEXT_FRAME(self, ball_list):
        if not self._CLICK_PAUSE and not self._RESIZE_PAUSE:
            self._canvas.delete(tkinter.ALL)
            for ball in ball_list:
                self._draw_ball(ball)
                self._trace_xy(ball, len(ball_list) - 1)
                self._trace_n(ball)
            self.root_window.update_idletasks()
    def _draw_ball(self, ball):
        X1, Y1, X2, Y2 = coordinate.Oval(ball.position, ball.radius).all()
        X1, Y1 = coordinate.Coordinate((X1, Y1)).absolute(self._get_WH())
        X2, Y2 = coordinate.Coordinate((X2, Y2)).absolute(self._get_WH())
        self._canvas.create_oval(X1, Y1, X2, Y2, fill=ball.color)
    def _trace_xy(self, ball, num_balls):
        if self._options.trace_xy:
            x, y = ball.position
            print('{:20} : ( {:.2f} , {:.2f} )'.format(ball.color, x, y))
            if ball.n == num_balls:
                print()
    def _trace_n(self, ball):
        if self._options.trace_n:
            X0, Y0 = coordinate.Coordinate(ball.position).absolute(self._get_WH())
            self._canvas.create_text(X0, Y0, text=ball.n)
    def _sum_velocity(self, ball):
        dx, dy = ball.velocity
        self.total_velocity_x += dx
        self.total_velocity_y += dy
    def _write_velocities(self):
        X1, Y1 = coordinate.Coordinate((0.25, 0.1)).absolute(self._get_WH())
        X2, Y2 = coordinate.Coordinate((0.50, 0.1)).absolute(self._get_WH())
        X3, Y3 = coordinate.Coordinate((0.75, 0.1)).absolute(self._get_WH())
        total_vx = '{:.2f}'.format(abs(self.total_velocity_x) * 1000)
        total_vy = '{:.2f}'.format(abs(self.total_velocity_y) * 1000)
        total_v = '{:.2f}'.format(abs(self.total_velocity_x) * 1000 + abs(self.total_velocity_y) * 1000)
        self._canvas.create_text(X1, Y1, text=total_vx)
        self._canvas.create_text(X2, Y2, text=total_vy)
        self._canvas.create_text(X3, Y3, text=total_v)
