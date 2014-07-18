import calculations
import collections
import itertools
class CollisionTracker:
    def __init__(self, options, balls):
        self.original_ball_colors = [b.color for b in balls]
        self.COLLISION_PAUSE = False
    def __call__(self, balls):
        self.hits_this_frame = []
        balls = self.handle_wall_collisions(balls)
        balls = self.handle_ball_collisions(balls)
        self.collision_track_thingy(balls)
        return balls
    def collision_track_thingy(self, balls):
        di = {k: [] for k in range(0, len(balls))}
        di['N'], di['S'], di['E'], di['W'] = [], [], [], []
        for A, B in self.hits_this_frame:
            di[A].append(B)
            di[B].append(A)
        pause_this_frame = False
        for ball, hits in di.items():
            if len(hits) > 1:
                pause_this_frame = True
                print(ball, hits, end='  ')
        print()
        if pause_this_frame:
            self.COLLISION_PAUSE = True
        else:
            self.COLLISION_PAUSE = False
        del di
    def handle_wall_collisions(self, balls):
        for i in range(0, len(balls)):
            ball = balls[i]
            Up, Dn, L, R = ball.edges
            dx, dy = ball.velocity
            if Up < 0:
                self.append_wall_collision(ball, 'N')
                dy = max(dy, dy * -1)
            if Dn > 1:
                self.append_wall_collision(ball, 'S')
                dy = min(dy, dy * -1)
            if L < 0:
                self.append_wall_collision(ball, 'W')
                dx = max(dx, dx * -1)
            if R > 1:
                self.append_wall_collision(ball, 'E')
                dx = min(dx, dx * -1)
            ball.velocity = (dx, dy)
            balls[i] = ball
        return balls
    def handle_ball_collisions(self, balls):
        index_combo_list = list(itertools.combinations(range(0, len(balls)), 2))
        for i, j in index_combo_list:
            A, B = balls[i], balls[j]
            Av, Bv = A.velocity, B.velocity
            if calculations.ball_collision(A, B):
                Av, Bv = calculations.new_velocity(A, B)
                self.append_ball_collision(A, B)
            A.velocity, B.velocity = Av, Bv
            balls[i], balls[j] = A, B
        return balls
    def append_ball_collision(self, A, B):
        ij = calculations.ball_order(A, B)
        self.hits_this_frame.append(ij)
    def append_wall_collision(self, A, wall):
        self.hits_this_frame.append((A.n, wall))
    def identify_wall_collisions(self, balls):
        for i in range(0, len(balls)):
            ball = balls[i]
            Up, Dn, L, R = ball.edges
            if Up < 0:
                self.append_wall_collision(ball, 'N')
            if Dn > 1:
                self.append_wall_collision(ball, 'S')
            if L < 0:
                self.append_wall_collision(ball, 'W')
            if R > 1:
                self.append_wall_collision(ball, 'E')
        return None
    def identify_ball_collisions(self, balls):
        index_combo_list = list(itertools.combinations(range(0, len(balls)), 2))
        for i, j in index_combo_list:
            A, B = balls[i], balls[j]
            if calculations.ball_collision(A, B):
                self.append_ball_collision(A, B)
        return None
