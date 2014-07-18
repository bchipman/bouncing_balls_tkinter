import math
def mSPF_from_FPS(FPS):
    return int((1 / FPS) * 1000)
def new_velocity_wall_hit(ball, wall):
    dx, dy = ball.velocity
    if wall == 'N':
        dy = max(dy, dy * -1)
    if wall == 'S':
        dy = min(dy, dy * -1)
    if wall == 'E':
        dx = max(dx, dx * -1)
    if wall == 'W':
        dx = min(dx, dx * -1)
    return (dx, dy)
def new_velocity(ball_A, ball_B):
    x1, y1 = ball_A.position
    x2, y2 = ball_B.position
    v1 = ball_A.velocity
    v2 = ball_B.velocity
    try:
        m1 = ball_A.mass
    except AttributeError:
        m1 = 1
    try:
        m2 = ball_B.mass
    except AttributeError:
        m2 = 1
    n = x1 - x2, y1 - y2  # normal vector
    n_mag = math.sqrt(n[0] ** 2 + n[1] ** 2)  # magnitude of normal vector
    un = n[0] / n_mag, n[1] / n_mag  # unit vector of n
    ut = -1 * un[1], un[0]  # unit tangent vector of n
    v1n = dot_product(un, v1)
    v1t = dot_product(ut, v1)
    v2n = dot_product(un, v2)
    v2t = dot_product(ut, v2)
    v1t_ = v1t
    v2t_ = v2t
    v1n_ = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
    v2n_ = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)
    v1n__ = (un[0] * v1n_, un[1] * v1n_)
    v1t__ = (ut[0] * v1t_, ut[1] * v1t_)
    v2n__ = (un[0] * v2n_, un[1] * v2n_)
    v2t__ = (ut[0] * v2t_, ut[1] * v2t_)
    _v1_ = v1n__[0] + v1t__[0], v1n__[1] + v1t__[1]
    _v2_ = v2n__[0] + v2t__[0], v2n__[1] + v2t__[1]
    return (_v1_, _v2_)
def dot_product(vector_1, vector_2):
    x, y = vector_1
    X, Y = vector_2
    return x * X + y * Y
def ball_edge_values(position, radius):
    x, y = position
    rx, ry = radius
    U = y - ry
    D = y + ry
    L = x - rx
    R = x + rx
    return (U, D, L, R)
def ball_order(ball_A, ball_B):
    return min(ball_A.n, ball_B.n), max(ball_A.n, ball_B.n)
def ball_collision(ball_A, ball_B):
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
def wall_collision(ball):
    Up, Dn, L, R = ball.edges
    if Up < 0:
        return True
    if Dn > 1:
        return True
    if L < 0:
        return True
    if R > 1:
        return True
    return False
def distance_between(coordinate1, coordinate2):
    x, y = coordinate1
    X, Y = coordinate2
    return math.sqrt((x - X) ** 2 + (Y - y) ** 2)
def ball_mass(r):
    return math.pi * (4 / 3) * r[0] ** 3
def new_position_post_collision_single(A):
    Ax, Ay = A.position  # current positions (balls overlap)
    dAx, dAy = A.velocity  # current velocities
    new_Ax = (-1 * dAx) + Ax
    new_Ay = (-1 * dAy) + Ay
    new_Axy = new_Ax, new_Ay
    return new_Axy
def new_position_post_collision(A, B):
    Ax, Ay = A.position  # current positions (balls overlap)
    dAx, dAy = A.velocity  # current velocities
    new_Ax = (-1 * dAx) + Ax
    new_Ay = (-1 * dAy) + Ay
    new_Axy = new_Ax, new_Ay
    Bx, By = B.position  # current positions (balls overlap)
    dBx, dBy = B.velocity  # current velocities
    new_Bx = (-1 * dBx) + Bx
    new_By = (-1 * dBy) + By
    new_Bxy = new_Bx, new_By
    return (new_Axy, new_Bxy)
def new_x_position_post_LR_wall_collision(A):
    Ax = A.position[0]  # current positions (balls overlap)
    dAx = A.velocity[0]  # current velocities
    new_Ax = (-1 * dAx) + Ax
    return new_Ax
def new_y_position_post_UD_wall_collision(A):
    Ay = A.position[1]  # current positions (balls overlap)
    dAy = A.velocity[1]  # current velocities
    new_Ay = (-1 * dAy) + Ay
    return new_Ay
def sum_vectors(vector_li):
    x_sum, y_sum = 0, 0
    for x, y in vector_li:
        x_sum += x
        y_sum += y
    return (x_sum, y_sum)
def avg_vectors(vector_li):
    n = len(vector_li)
    x_sum, y_sum = 0, 0
    print(n)
    for x, y in vector_li:
        x_sum += x
        y_sum += y
    x_avg = x_sum / n
    y_avg = y_sum / n
    return (x_avg, y_avg)
