from time import time
import sys
from tools.calculators import calculate_total_dist, get_matrix_of_distances


def find_closest(matrix_of_distances, tours):
    index = tours[-1]
    best_index = 0
    best_dist = sys.float_info.max
    for i in range(len(matrix_of_distances)):
        if i not in tours and i != index:
            dist = matrix_of_distances[index, i]
            if dist < best_dist:
                best_index = i
                best_dist = dist
    tours.append(best_index)
    return tours


def greedy(matrix_of_distances, index):
    tour = [index]
    dist = 0
    for j in range(len(matrix_of_distances) - 1):
        tour = find_closest(matrix_of_distances, tour)
    dist = calculate_total_dist(matrix_of_distances, tour)
    return tour, dist
    


def solve_tsp_by_greedy_method(tsp_matrix):
    start = time()
    matrix_of_distances = get_matrix_of_distances(tsp_matrix)
    best_distance = sys.float_info.max
    best_tour = range(len(tsp_matrix))
    for i in range(len(tsp_matrix)):
        tour, dist = greedy(matrix_of_distances, i)
        if dist < best_distance:
            best_distance = dist
            best_tour = tour
    time_diff = time() - start
    return best_tour, time_diff, best_distance