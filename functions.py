import random
import math


def largest_triangle(P, start):
    """
    :param P: list of points forming a convex polygon
    :param start: index of point to start from
    :return: points that form the largest triangle in P
    """
    # print(f"{len(P)=}")

    assert len(P) >= 3, "P must have at least 3 points"
    if len(P) == 3:
        return P
    a = start
    T_a = largest_triangle_from_A(P, a)
    m = largest_median(P, T_a)
    T_m = largest_triangle_from_A(P, m)
    P_1, P_2, bad_p = sub_polygons(P, T_a, T_m)
    P_1_points = [P[i] for i in P_1]
    P_2_points = [P[i] for i in P_2]
    if bad_p is None:
        return max(largest_triangle(P_1_points, (start + 1) % len(P_1_points)),
                   largest_triangle(P_2_points, (start + 1) % len(P_2_points)), key=lambda x: area(*x))
    elif bad_p == 0:
        return largest_triangle(P_2_points, (start + 1) % len(P_2_points))
    else:
        return largest_triangle(P_1_points, (start + 1) % len(P_1_points))


def largest_triangle_from_A(P, idx_a):
    """
    :param P: convex hull that contains point A
    :param idx_a: index of point A
    :return: largest triangle in P rooted at A
    """
    def next(i):
        return (i + 1) % len(P)
    if len(P) == 3:
        return [0, 1, 2]
    idx_b = next(idx_a)
    idx_c = next(idx_b)
    best = [idx_a, idx_b, idx_c]
    while idx_b != idx_a:
        while area(P[idx_a], P[idx_b], P[idx_c]) <= area(P[idx_a], P[idx_b], P[next(idx_c)]):
            idx_c = next(idx_c)
        if area(P[idx_a], P[idx_b], P[idx_c]) > area(P[best[0]], P[best[1]], P[best[2]]):
            best = [idx_a, idx_b, idx_c]
        idx_b = next(idx_b)
    return best


def largest_median(P, points):
    """
    :param P: a convex hull
    :param points: 6 points of P
    :return: index of the largest median of P
    """
    points = sorted(points)
    distances = [points[1] - points[0], points[2] - points[1], len(P) - points[2] + points[0]]
    max_distance = max(distances)
    max_distance_idx = distances.index(max_distance)
    median = (max_distance // 2 + points[max_distance_idx]) % len(P)
    return median


def sub_polygons(P, t_1, t_2):
    """
    :param P: points that form a convex hull
    :param t_1: 3 points of P
    :param t_2: 3 points of P
    :return: 6 intervals of P divided by t_1 and t_2
    """
    total = len(P)
    res = [[], [], [], [], [], []]
    current = 0
    last_t_1 = False
    bad_p = None
    for p in range(total):
        res[current].append(p)
        if p in t_1 or p in t_2:
            res[current] = res[current][:-1]
            current = (current + 1) % 6
            res[current].append(p)
            if p in t_1:
                if p not in t_2:
                    if last_t_1:
                        bad_p = current % 2
                    last_t_1 = True
                else:
                    last_t_1 = False
                    current = (current + 1) % 6
                    res[current].append(p)
            else:
                last_t_1 = False
    p_1 = sorted(list({*res[0], *res[2], *res[4]}))
    p_2 = sorted(list({*res[1], *res[3], *res[5]}))
    return p_1, p_2, bad_p


def area(a, b, c):
    """area of triangle"""
    return abs((a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0])) / 2


def convex_hull_from_points(points):
    """
    :param points: list of 2d points
    :return: list of points that form a convex hull
    """

    def cross(o, a, b):
        """cross product"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    points = sorted(set(map(tuple, points)))
    if len(points) <= 1:
        return points
    right_hull = []
    for p in points:
        while len(right_hull) >= 2 and cross(right_hull[-2], right_hull[-1], p) <= 0:
            right_hull.pop()
        right_hull.append(p)
    left_hull = []
    for p in points:
        while len(left_hull) >= 2 and cross(left_hull[-2], left_hull[-1], p) >= 0:
            left_hull.pop()
        left_hull.append(p)
    return right_hull + left_hull[:-1][::-1]


def random_points(N, radius=10):
    """
    :param N: number of points
    :param radius: range of points
    :return: list of random points
    """
    points = [(random.uniform(-radius, radius), random.uniform(-radius, radius)) for _ in range(N)]
    return points


def circle_points(N, radius=10):
    """
    :param N: number of points
    :param radius: range of points
    :return: list of points on a circle
    """
    if N > radius * 2 - 1:
        raise ValueError("N must be smaller than 2*radius-1")

    unique_points = random.sample(range(-radius, radius), N)
    y = [math.sqrt(radius ** 2 - i ** 2) for i in unique_points]
    # make every second point negative
    for i in range(1, len(y), 2):
        y[i] *= -1
    return list(zip(unique_points, y))
