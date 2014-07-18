import calculations
import itertools
class CollisionTracker:
    def __init__(self, options, balls):
        self.original_ball_colors = [b.color for b in balls]
        self.blacklisted_collisions = {}
        self.blacklisted_collisions2 = []
        self.NUMFRAMESNOCOLLISIONS = 7
    def __call__(self, balls):
        balls = self._set_or_change_ball_color(balls)
        balls = self.handle_wall_collisions(balls)
        balls = self.handle_ball_collisions(balls)
        return balls
    def _set_or_change_ball_color(self, balls):
        balls_blacklisted_this_frame = set([ball for hit in self.blacklisted_collisions for ball in hit])
        for ball in balls:
            if ball.n in balls_blacklisted_this_frame:
                ball.color = 'yellow3'
            else:
                ball.color = self.original_ball_colors[ball.n]
        del balls_blacklisted_this_frame
        return balls
    def handle_wall_collisions(self, balls):
        for i in range(0, len(balls)):
            ball = balls[i]
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
            balls[i] = ball
        return balls
    def handle_ball_collisions(self, balls):
        index_combo_list = list(itertools.combinations(range(0, len(balls)), 2))
        for i, j in index_combo_list:
            A, B = balls[i], balls[j]
            Av, Bv = A.velocity, B.velocity
            if not self.blacklisted(A, B):
                if calculations.ball_collision(A, B):
                    self.blacklist_collision(A, B)
                    Av, Bv = calculations.new_velocity(A, B)
            elif self.blacklisted(A, B):
                self.decrement_blacklisted_collision_counter(A, B)
            A.velocity, B.velocity = Av, Bv
            balls[i], balls[j] = A, B
        return balls
    def blacklisted(self, A, B):
        ball_pair = calculations.ball_order(A, B)
        if ball_pair in self.blacklisted_collisions:
            return True
        else:
            return False
    def blacklist_collision(self, A, B):
        ball_pair = calculations.ball_order(A, B)
        self.blacklisted_collisions[ball_pair] = self.NUMFRAMESNOCOLLISIONS
    def decrement_blacklisted_collision_counter(self, A, B):
        ball_pair = calculations.ball_order(A, B)
        if self.blacklisted_collisions[ball_pair] > 0:
            self.blacklisted_collisions[ball_pair] -= 1
        elif self.blacklisted_collisions[ball_pair] == 0:
            del self.blacklisted_collisions[ball_pair]
