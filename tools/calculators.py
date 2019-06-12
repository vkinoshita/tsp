import numpy as np
from scipy.spatial import distance

def get_matrix_of_distances(tsp_points):
    return distance.cdist(tsp_points, tsp_points, 'euclidean')

def calculate_total_dist(matrix_of_distances, tour):
    dist = 0
    for i in range(-1, len(tour) - 1):
        dist += matrix_of_distances[tour[i], tour[i + 1]]
    return dist

def calculate_total_dist_by_arcs(matrix_of_distances, arcs):
    dist = 0
    for i in range(len(arcs)):
        dist += matrix_of_distances[arcs[i][0], arcs[i][1]]
    return dist
