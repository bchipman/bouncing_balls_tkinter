import balls
import collision_tracker
import window
import functools
class Game:
    def __init__(self, options):
        self.window = window.Window(options)
        self.balls = balls.BallCreator(options).balls
        self.collision_tracker = collision_tracker.CollisionTracker(options, self.balls)
    def START(self):
        self.GAME_LOOP(self.balls)
        self.window.root_window.mainloop()
    def GAME_LOOP(self, balls):
        balls = self.collision_tracker(balls)
        for ball in balls:
            ball.move()
        self.window.NEXT_FRAME(balls)
        game_loop_fn = functools.partial(self.GAME_LOOP, balls)
        self.window.root_window.after(self.window._mSPF, game_loop_fn)
class GameOptions:
    def __init__(self):
        self.fps = 50
        self.bg_color = 'grey'
        self.trace_xy = False
        self.trace_n = True
        self.N = 25
        self.XY = (0.01, 0.99)
        self.R = (0.025, 0.25)
        self.V = (0.0005, 0.0020)
        self.seed_on = True
        self.threshold = 5
        self.frame_window_size = 20
if __name__ == '__main__':
    Game(GameOptions()).START()
