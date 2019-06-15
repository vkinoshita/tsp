from time import time
import sys
from tools.calculators import calculate_total_dist, get_matrix_of_distances
from solvers.greedy import greedy
from tools.plotter import plot_connected_tsp_points
import random

def reversed(arr, start, end):
    length = len(arr)
    new_arr = arr.copy()
    if end < start:
        end = end + length
    for i in range(end - start + 1):
        new_arr[(end - i) % length] = arr[(start + i) % length]
    return new_arr


def reverse_segment_if_better(matrix_of_distances, tour, i, j, k):
    try:
        A, B, C, D, E, F = tour[i-1], tour[i], tour[j-1], tour[j], tour[k-1], tour[k]
    except:
        print(i, j, k, len(tour))
        return
    d0 = matrix_of_distances[A,B] + matrix_of_distances[C,D] + matrix_of_distances[E,F]
    d1 = matrix_of_distances[A,C] + matrix_of_distances[B,D] + matrix_of_distances[E,F]
    d2 = matrix_of_distances[A,B] + matrix_of_distances[C,E] + matrix_of_distances[D,F]
    d3 = matrix_of_distances[A,D] + matrix_of_distances[E,B] + matrix_of_distances[C,F]
    d4 = matrix_of_distances[F,B] + matrix_of_distances[C,D] + matrix_of_distances[E,A]

    if d0 > d1:
      return d0 - d1, reversed(tour, i, j - 1)
    elif d0 > d2:
      return d0 - d2, reversed(tour, j, k - 1)
    elif d0 > d4:
      return d0 - d4, reversed(tour, k, i - 1)
    elif d0 > d3:
      tour = reversed(tour, i, j - 1)
      tour = reversed(tour, j, k - 1)
      tour = reversed(tour, k, i - 1)
      return d0 - d3, tour
    return 0, tour


def random_i_j_k(choice_range, length):
    x = [random.randint(0, length - 1), random.randint(0, length - 1), random.randint(0, length - 1)]
    while x[0] + 1 >= x[1] or x[1] + 1 >= x[2]:
        x = [random.randint(0, length - 1), random.randint(0, length - 1), random.randint(0, length - 1)]
    return x[0], x[1], x[2]

def solve_tsp_by_3_opt(tsp_matrix):
    start = time()
    matrix_of_distances = get_matrix_of_distances(tsp_matrix)
    length = len(tsp_matrix)
    choice_range = list(range(length + 1))
    best_tour, best_distance = greedy(matrix_of_distances, 0)
    plot_connected_tsp_points(tsp_matrix, best_tour, 'images/3_opt_br/0')
    number_of_iterations = 100 + (length - 10) * (10000000 - 100) / (1000.0 - 10.0)
    for count in range(1, int(number_of_iterations)):
        i, j, k = random_i_j_k(choice_range, length)
        dist_diff, new_tour = reverse_segment_if_better(matrix_of_distances, best_tour, i, j, k)
        if dist_diff > 0:
            total_dist = calculate_total_dist(matrix_of_distances, new_tour)
            if total_dist < best_distance:
                best_tour = new_tour
                plot_connected_tsp_points(tsp_matrix, new_tour, 'images/3_opt_br/{}'.format(count))
                best_distance = total_dist
    time_diff = time() - start
    return best_tour, time_diff, best_distance

#        n: 1000
#     time: 638.9722263813019
# distance: 2571.2597929484828
