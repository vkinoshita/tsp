import matplotlib.pyplot as plt
import numpy as np
from tools.configs import tsp_base_file_name, tsp_sample_size

def plot_connected_tsp_points(tsp_matrix, tour, file_name='', show=False):
    for i in range(-1, len(tour) - 1):
        x = [tsp_matrix.item((tour[i], 0)), tsp_matrix.item((tour[i + 1], 0))]
        y = [tsp_matrix.item((tour[i], 1)), tsp_matrix.item((tour[i + 1], 1))]
        plt.plot(x, y, 'ro-', linewidth=0.5, color='black', markersize=2)
    if file_name:
        plt.savefig(file_name + '.png')
    if show:
        plt.show()
    plt.clf()

def plot_connected_tsp_points_from_arcs(tsp_matrix, arcs, file_name='', show=False):
    for i in range(-1, len(arcs) - 1):
        x = [tsp_matrix.item((arcs[i][0], 0)), tsp_matrix.item((arcs[i][1], 0))]
        y = [tsp_matrix.item((arcs[i][0], 1)), tsp_matrix.item((arcs[i][1], 1))]
        plt.plot(x, y, 'ro-', linewidth=0.5, color='black', markersize=2)
    if file_name:
        plt.savefig(file_name + '.png')
    if show:
        plt.show()
    plt.clf()
