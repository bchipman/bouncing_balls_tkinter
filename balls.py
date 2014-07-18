import calculations
import random_seeds
import tk_colors
import random
class Ball:
    def __init__(self, number, center, radius, velocity, color):
        self.n = number
        self.position = center
        self.radius = radius
        self.velocity = velocity
        self.color = color
        self.mass = calculations.ball_mass(self.radius)
        self.edges = calculations.ball_edge_values(self.position, self.radius)
    def move(self):
        x,   y = self.position
        dx, dy = self.velocity
        self.position = (x + dx, y + dy)
        self.edges = calculations.ball_edge_values(self.position, self.radius)
class BallCreator:
    def __init__(self, options):
        self.options = options
        self.balls = self._setup_balls()
    def _setup_balls(self):
        balls = []
        for n in range(0, self.options.N):
            while True:
                new_ball = self._create_random_ball(n)
                if self._new_ball_ok(new_ball, balls):
                    break
            balls.append(new_ball)
        return balls
    def _create_random_ball(self, n):
        if self.options.seed_on:
            X, Y, R, V, C = random_seeds.RNDX[0], random_seeds.RNDY[0], random_seeds.RNDR[0], random_seeds.RNDV[0], random_seeds.RNDC[0]
            del random_seeds.RNDX[0], random_seeds.RNDY[0], random_seeds.RNDR[0], random_seeds.RNDV[0], random_seeds.RNDC[0]
        elif not self.options.seed_on:
            xy, XY = self.options.XY
            r, R = self.options.R
            v, V = self.options.V
            X = random.uniform(xy, XY)
            Y = random.uniform(xy, XY)
            R = random.uniform(r, R)
            V = random.uniform(v, V)
            V = random.choice([V, V * -1])
            C = random.choice(tk_colors.all_colors)
        return Ball(number=n, center=(X, Y), radius=(R, R), velocity=(V, V), color=C)
    def _new_ball_ok(self, new_ball, balls):
        for ball in balls:
            if calculations.ball_collision(new_ball, ball):
                return False
            if ball.color == new_ball.color:
                return False
        if calculations.wall_collision(new_ball):
            return False
        return True
