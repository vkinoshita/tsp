from time import time
import sys
from tools.calculators import calculate_total_dist, get_matrix_of_distances
from solvers.greedy import greedy
from tools.plotter import plot_connected_tsp_points
import random
import numpy as np
from itertools import combinations

def reverse(arr, start, end):
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
    # current distance
    d0 = matrix_of_distances[A,B] + matrix_of_distances[C,D] + matrix_of_distances[E,F]
    # 2-opt
    d1 = matrix_of_distances[A,C] + matrix_of_distances[B,D] + matrix_of_distances[E,F]
    d2 = matrix_of_distances[A,B] + matrix_of_distances[C,E] + matrix_of_distances[D,F]
    d3 = matrix_of_distances[F,B] + matrix_of_distances[C,D] + matrix_of_distances[E,A]
    # 3-opt
    d4 = matrix_of_distances[A,D] + matrix_of_distances[B,F] + matrix_of_distances[E,C]
    d5 = matrix_of_distances[C,F] + matrix_of_distances[B,D] + matrix_of_distances[E,A]
    d6 = matrix_of_distances[B,E] + matrix_of_distances[D,F] + matrix_of_distances[C,A]
    d7 = matrix_of_distances[A,D] + matrix_of_distances[E,B] + matrix_of_distances[C,F]

    # 3-opt
    if d0 > d7:
        tour = reverse(tour, i, j - 1)
        tour = reverse(tour, j, k - 1)
        tour = reverse(tour, k, i - 1)
        return d0 - d7, tour
    elif d0 > d6:
        tour = reverse(tour, i, j - 1)
        tour = reverse(tour, j, k - 1)
        return d0 - d6, tour
    elif d0 > d5:
        tour = reverse(tour, k, i - 1)
        tour = reverse(tour, i, j - 1)
        return d0 - d5, tour
    elif d0 > d4:
        tour = reverse(tour, j, k - 1)
        tour = reverse(tour, k, i - 1)
        return d0 - d4, tour

    # 2-opt
    elif d0 > d3:
        return d0 - d3, reverse(tour, k, i - 1)
    elif d0 > d2:
        return d0 - d2, reverse(tour, j, k - 1)
    elif d0 > d1:
        return d0 - d1, reverse(tour, i, j - 1)

    return 0, tour


def random_i_j_k(length):
    x = [random.randint(0, length - 1), random.randint(0, length - 1), random.randint(0, length - 1)]
    while x[0] >= x[1] - 1 or x[1] >= x[2] - 1:
        x = [random.randint(0, length - 1), random.randint(0, length - 1), random.randint(0, length - 1)]
    return x[0], x[1], x[2]


def solve_tsp_by_3_opt(tsp_matrix):
    start = time()
    matrix_of_distances = get_matrix_of_distances(tsp_matrix)
    length = len(tsp_matrix)
    best_tour, best_distance = greedy(matrix_of_distances, 0)
    # plot_connected_tsp_points(tsp_matrix, best_tour, '../images/3_opt_xql662/0')
    number_of_iterations = 100 + (length - 10) * (10000000 - 100) / (1000.0 - 10.0)
    for count in range(1, int(number_of_iterations)):
        i, j, k = random_i_j_k(length)
        dist_diff, new_tour = reverse_segment_if_better(matrix_of_distances, best_tour, i, j, k)
        if dist_diff > 0:
            total_dist = calculate_total_dist(matrix_of_distances, new_tour)
            if total_dist < best_distance:
                best_tour = new_tour
                # plot_connected_tsp_points(tsp_matrix, new_tour, '../images/3_opt_xql662/{}'.format(count))
                best_distance = total_dist
    time_diff = time() - start
    return best_tour, time_diff, best_distance

  
def get_closest_neighbors(matrix_of_distances):
    m = 40
    closest_neighbors = []
    for i in range(len(matrix_of_distances)):
        close = np.delete(np.argsort(matrix_of_distances[i]), 0)[0:m]
        closest_neighbors = [*closest_neighbors, close]
    return closest_neighbors


def get_closes_neighbors_combinations(index, length, closest_neighbors, best_tour):
    neighbors = closest_neighbors[index]
    for permutation in combinations(neighbors, 3):
        indices = [
            best_tour.index(permutation[0]),
            best_tour.index(permutation[1]),
            best_tour.index(permutation[2])
        ]
        indices.sort()
        if indices[0] < indices[1] - 1 and indices[1] < indices[2] - 1:
            yield indices[0], indices[1], indices[2]
            yield indices[0] + 1, indices[1] + 1, (indices[2] + 1) % length



def solve_tsp_by_3_opt_2(tsp_matrix):
    start = time()
    matrix_of_distances = get_matrix_of_distances(tsp_matrix)
    closest_neighbors = get_closest_neighbors(matrix_of_distances)
    length = len(tsp_matrix)
    best_tour, best_distance = greedy(matrix_of_distances, 0)
    # plot_connected_tsp_points(tsp_matrix, best_tour, '../images/3_opt_xql662/0')
    count = 1
    n_changes = 1
    while n_changes > 0:
        n_changes = 0
        index = 0
        while index != length:
            local_changes = 0
            for i, j, k in get_closes_neighbors_combinations(index, length, closest_neighbors, best_tour):
                dist_diff, new_tour = reverse_segment_if_better(matrix_of_distances, best_tour, i, j, k)
                if dist_diff > 0:
                    best_distance -= dist_diff
                    best_tour = new_tour
                    local_changes += 1
                    print(count)
                    # plot_connected_tsp_points(tsp_matrix, new_tour, '../images/3_opt_xql662/{}'.format(count))
                count += 1
            if local_changes == 0:
                index += 1
            n_changes += local_changes
    time_diff = time() - start
    return best_tour, time_diff, best_distance
