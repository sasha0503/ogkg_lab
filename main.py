"""finding the largest area triangle in a convex hull"""
import time
import matplotlib.pyplot as plt

from functions import random_points, circle_points, convex_hull_from_points, largest_triangle


def plot(points, convex_hull, triangle):
    plt.plot([p[0] for p in points], [p[1] for p in points], 'bo')
    plt.plot([p[0] for p in convex_hull], [p[1] for p in convex_hull], 'r-')
    plt.plot([p[0] for p in triangle] + [triangle[0][0]], [p[1] for p in triangle] + [triangle[0][1]], 'g-')

    plt.savefig('plot.png')
    plt.show()


def compare(iterations=1000):
    """compare how fast function largest_triangle works depending on the number of points"""
    times = []
    for i in range(3, iterations):
        print(i)
        points = circle_points(N=i, radius=10000)
        convex_hull = convex_hull_from_points(points)
        start = time.time()
        largest_triangle(convex_hull[:-1], 0)
        times.append(time.time() - start)
    # take the average of each 10 runs
    times = [sum(times[i:i + 100]) / 100 for i in range(0, len(times), 100)]
    plt.plot(range(3, iterations, 100), times)
    plt.xlabel('number of points')
    plt.ylabel('time, s')
    # add points for each 100 runs
    for i in range(3, iterations, 100):
        plt.plot(i, times[i // 100 - 1], 'bo')
        plt.annotate('{}'.format(round(times[i // 100 - 1], 3)), xy=(i, times[i // 100 - 1]))
    plt.savefig('compare.png')
    plt.show()


def one_try():
    points = circle_points(N=20, radius=10000)
    convex_hull = convex_hull_from_points(points)

    start = time.time()
    a, b, c = largest_triangle(convex_hull[:-1], 0)
    print('time: {}'.format(time.time() - start))

    plot(points, convex_hull, [a, b, c])


if __name__ == '__main__':
    compare()
