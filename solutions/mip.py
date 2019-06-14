from time import time
import sys
from mip.model import Model, xsum
from mip.constants import BINARY
from tools.calculators import calculate_total_dist_by_arcs, get_matrix_of_distances
from tools.plotter import plot_connected_tsp_points_from_arcs
from numpy import inf


def solve_tsp_by_mip(tsp_matrix):
    start = time()
    matrix_of_distances = get_matrix_of_distances(tsp_matrix)
    length = len(tsp_matrix)

    model = Model(solver_name='gurobi')
    model.verbose = 1

    x = [[model.add_var(var_type=BINARY) for j in range(length)] for i in range(length)]

    y = [model.add_var() for i in range(length)]

    model.objective = xsum(matrix_of_distances[i][j]*x[i][j] for j in range(length) for i in range(length))

    for i in range(length):
        model += xsum(x[j][i] for j in range(length) if j != i) == 1
        model += xsum(x[i][j] for j in range(length) if j != i) == 1

    for i in range(1, length):
        for j in [x for x in range(1, length) if x != i]:
            model += y[i] - (length+1)*x[i][j] >= y[j] - length

    model.optimize(max_seconds=300)

    arcs = [(i, j) for i in range(length) for j in range(length) if x[i][j].x >= 0.99]

    best_distance = calculate_total_dist_by_arcs(matrix_of_distances, arcs)
    time_diff = time() - start
    return arcs, time_diff, best_distance


def find_arc_with(position, arcs):
    for arc in arcs:
        if position == arc[0]:
            return arc[1], arc
        elif position == arc[1]:
            return arc[0], arc
    raise Exception('arc not found')


def get_cycle(arcs):
    control_arcs = arcs.copy()
    all_cycles = []

    current_arc = None
    initial_position = None
    current_position = None
    cycle = None

    while True:
        if current_position == initial_position:
            if cycle:
                all_cycles = [*all_cycles, cycle]
            if len(control_arcs) == 0:
                break
            current_arc = control_arcs[0]
            initial_position = current_arc[0]
            current_position = current_arc[1]
            control_arcs.remove(current_arc)
            cycle = [current_arc]

        current_position, current_arc = find_arc_with(current_position, control_arcs)
        cycle = [*cycle, current_arc]
        control_arcs.remove(current_arc)

    return all_cycles


def solve(matrix_of_distances, length, cycles):
    model = Model(solver_name='gurobi')
    model.verbose = 0

    x = [[model.add_var(var_type=BINARY) for j in range(length)] for i in range(length)]

    y = [model.add_var() for i in range(length)]

    model.objective = xsum(matrix_of_distances[i][j]*x[i][j] for j in range(length) for i in range(length))

    for i in range(length):
        model += (xsum(x[i][j] for j in range(0, i)) + xsum(x[j][i] for j in range(i + 1, length))) == 2
    
    for cycle in cycles:
        cycle_len = len(cycle)
        model += xsum(x[c[0]][c[1]] for c in cycle) <= cycle_len - 1
        model += xsum(x[c[1]][c[0]] for c in cycle) <= cycle_len - 1

    model.optimize(max_seconds=300)

    arcs = [(i, j) for i in range(length) for j in range(length) if x[i][j].x >= 0.99]
    best_distance = calculate_total_dist_by_arcs(matrix_of_distances, arcs)

    return arcs, best_distance


def solve_tsp_by_mip_with_sub_cycles(tsp_matrix):
    start = time()
    matrix_of_distances = get_matrix_of_distances(tsp_matrix)
    total_length = len(tsp_matrix)
    best_distance = sys.float_info.max

    found_cycles = []
    cycles = []
    arcs = [(i, i + 1) for i in range(total_length - 1)]

    iteration = 0

    while len(found_cycles) != 1:
        arcs, best_distance = solve(matrix_of_distances, total_length, cycles)
        found_cycles = get_cycle(arcs)
        cycles = [*cycles, *found_cycles]
        # plot_connected_tsp_points_from_arcs(tsp_matrix, arcs, 'images/mip_sub_cycles/{}'.format(iteration))
        print(iteration)
        iteration += 1

    time_diff = time() - start
    return arcs, time_diff, best_distance


def solve_tsp_by_mip_with_sub_cycles_2(tsp_matrix):
    start = time()
    matrix_of_distances = get_matrix_of_distances(tsp_matrix)
    total_length = len(tsp_matrix)
    best_distance = sys.float_info.max

    found_cycles = []
    arcs = [(i, i + 1) for i in range(total_length - 1)]

    iteration = 0
    
    model = Model(solver_name='gurobi')
    model.verbose = 0

    x = [[model.add_var(var_type=BINARY) for j in range(total_length)] for i in range(total_length)]

    y = [model.add_var() for i in range(total_length)]

    model.objective = xsum(matrix_of_distances[i][j]*x[i][j] for j in range(total_length) for i in range(total_length))

    for i in range(total_length):
        model += (xsum(x[i][j] for j in range(0, i)) + xsum(x[j][i] for j in range(i + 1, total_length))) == 2

    while len(found_cycles) != 1:
        model.optimize(max_seconds=300)

        arcs = [(i, j) for i in range(total_length) for j in range(total_length) if x[i][j].x >= 0.99]
        best_distance = calculate_total_dist_by_arcs(matrix_of_distances, arcs)

        found_cycles = get_cycle(arcs)
        
        for cycle in found_cycles:
            points = {}
            for arc in cycle:
                points = {*points, arc[0]}
                points = {*points, arc[1]}
            possible_arcs = []
            points_temp = points.copy()
            for p in points:
                points_temp.remove(p)
                for pt in points_temp:
                    possible_arcs = [*possible_arcs, (p, pt)]
            cycle_len = len(cycle)
            model += xsum(x[arc[0]][arc[1]] + x[arc[1]][arc[0]] for arc in possible_arcs) <= cycle_len - 1

        plot_connected_tsp_points_from_arcs(tsp_matrix, arcs, '../images/mip_300/{}'.format(iteration))
        print(iteration)
        iteration += 1

    time_diff = time() - start
    return arcs, time_diff, best_distance

#        n: 500
#     time: 15839.2320947647095


