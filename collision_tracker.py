import calculations
import collections
import itertools
class CollisionTracker:
    def __init__(self, options, balls):
        self.threshold = options.threshold
        self.frame_window_size = options.frame_window_size
        self.list_hits_last_50_frames = [[] for i in range(0, self.frame_window_size)]
        self.original_ball_colors = [b.color for b in balls]
        self.blacklisted_collisions = {}
        self.NUMFRAMESNOCOLLISIONS = 2
    def __call__(self, balls):
        self.hits_this_frame = []
        try:
            del self.hits_above_threshold_this_frame
        except AttributeError:
            pass
        self._number_same_hits_within_frame_window()
        balls = self._set_or_change_ball_color(balls)
        balls = self.handle_wall_collisions(balls)
        balls = self.handle_ball_collisions(balls)
        self._4_update_hits_for_last_50_frames_list()
        return balls
    def _number_same_hits_within_frame_window(self):
        hits_all_frames_nested = self.list_hits_last_50_frames
        hits_all_frames_flattened = [hit for hits_single_frame in hits_all_frames_nested for hit in hits_single_frame]
        counted_hits_all_frames = collections.Counter(hits_all_frames_flattened)
        self.hits_above_threshold_this_frame = [k for (k, v) in counted_hits_all_frames.items() if v > self.threshold]
        del hits_all_frames_nested, hits_all_frames_flattened, counted_hits_all_frames
    def _set_or_change_ball_color(self, balls):
        balls_above_threshold_this_frame = set([ball for hit in self.hits_above_threshold_this_frame for ball in hit])
        for ball in balls:
            if ball.n in balls_above_threshold_this_frame:
                ball.color = 'yellow'
            else:
                ball.color = self.original_ball_colors[ball.n]
        del balls_above_threshold_this_frame
        return balls
    def _add_to_hits_this_frame_li(self, A, B):
        ij = calculations.ball_order(A, B)
        self.hits_this_frame.append(ij)
    def _above_threshold_this_frame(self, A, B):
        ij = calculations.ball_order(A, B)
        if ij in self.hits_above_threshold_this_frame:
            print(ij, A.position, B.position)
            return True
        return False
    def _4_update_hits_for_last_50_frames_list(self):
        if len(self.hits_this_frame) > 0:
            self.list_hits_last_50_frames = self.list_hits_last_50_frames[1::] + [self.hits_this_frame]
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
            A,  B = balls[i], balls[j]
            Av, Bv = A.velocity, B.velocity
            if calculations.ball_collision(A, B):
                self._add_to_hits_this_frame_li(A, B)
                if not self._above_threshold_this_frame(A, B):
                    Av, Bv = calculations.new_velocity(A, B)
            A.velocity, B.velocity = Av, Bv
            balls[i], balls[j] = A,  B
        return balls
    def blacklist_collision(self, A, B):
        ball_pair = calculations.ball_order(A, B)
        self.blacklisted_collisions[ball_pair] = self.NUMFRAMESNOCOLLISIONS
    def blacklisted(self, A, B):
        ball_pair = calculations.ball_order(A, B)
        if ball_pair in self.blacklisted_collisions:
            return True
        else:
            return False
    def decrement_blacklisted_collision_counter(self, A, B):
        ball_pair = calculations.ball_order(A, B)
        if self.blacklisted_collisions[ball_pair] > 0:
            self.blacklisted_collisions[ball_pair] -= 1
        elif self.blacklisted_collisions[ball_pair] == 0:
            del self.blacklisted_collisions[ball_pair]
