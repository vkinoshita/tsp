import sys
from optparse import OptionParser
import numpy as np
from solutions.brute_force import solve_tsp_by_brute_force
from solutions.greedy import solve_tsp_by_greedy_method
from solutions.mip import solve_tsp_by_mip, solve_tsp_by_mip_with_sub_cycles, solve_tsp_by_mip_with_sub_cycles_2
from solutions.opt_3 import solve_tsp_by_3_opt
from tools.configs import tsp_base_file_name, tsp_sample_size
from tools.plotter import plot_connected_tsp_points, plot_connected_tsp_points_from_arcs
from tools.generator import get_n_random_x_y


def main():
    solvers = {
        'brute-force': {
            'solver': solve_tsp_by_brute_force,
            'plotter': plot_connected_tsp_points
        },
        'greedy': {
            'solver': solve_tsp_by_greedy_method,
            'plotter': plot_connected_tsp_points
        },
        'mip': {
            'solver': solve_tsp_by_mip,
            'plotter': plot_connected_tsp_points_from_arcs
        },
        'mip-s': {
            'solver': solve_tsp_by_mip_with_sub_cycles,
            'plotter': plot_connected_tsp_points_from_arcs
        },
        'mip-s-2': {
            'solver': solve_tsp_by_mip_with_sub_cycles_2,
            'plotter': plot_connected_tsp_points_from_arcs
        },
        '3-opt': {
            'solver': solve_tsp_by_3_opt,
            'plotter': plot_connected_tsp_points
        },
    }

    parser = OptionParser()
    parser.add_option("-r", "--rand-size", dest="rand_size", type="int", default=None)
    parser.add_option("-p", "--plot", dest="plot", action="store_true", default=False)
    parser.add_option("-f", "--plot-to-file", dest="plot_to_file", type="string", default=None)
    parser.add_option("-s", "--solver", dest="solver")
    parser.add_option("-b", "--benchmark", dest="benchmark", type='int', nargs=3, default=None)
    parser.add_option("-z", "--benchmark-file", dest="benchmark_file", type='string', default=None)
    parser.add_option("-m", "--matrix-file", dest="matrix_file", type='string', default=None)
    (options, args) = parser.parse_args()

    if options.solver not in solvers.keys():
        print('solver not found!')
        return
    
    solver = solvers[options.solver]['solver']
    plotter = solvers[options.solver]['plotter']

    print('  rand size:', options.rand_size)
    print('should plot:', options.plot)
    print('  plot file:', options.plot_to_file)
    print('     solver:', options.solver)
    print('  benchmark:', options.benchmark)

    if options.benchmark is None:
        tsp_matrix = None

        if options.rand_size is None:
            if options.matrix_file:
                tsp_matrix = np.load(options.matrix_file)
            else:
                tsp_matrix = np.load(tsp_base_file_name)
        else:
            tsp_matrix = get_n_random_x_y(options.rand_size)

        tour, time_diff, distance = solver(tsp_matrix)
        print('    tour:', tour)
        print('    time:', time_diff)
        print('distance:', distance)
        if options.plot_to_file or options.plot:
            plotter(tsp_matrix, tour, options.plot_to_file, options.plot)
    else:
        if options.benchmark_file:
            with open(options.benchmark_file, "w") as f:
                f.write('size,iteration,distance,time\n')
        print('size iteration distance     time')
        for n in range(options.benchmark[0], options.benchmark[1] + 1):
            for i in range(1, options.benchmark[2] + 1):
                tsp_matrix = get_n_random_x_y(n)
                tour, time_diff, distance = solver(tsp_matrix)
                if options.benchmark_file:
                    with open(options.benchmark_file, "a") as f:
                        f.write('{},{},{},{}\n'.format(n, i, distance, time_diff))
                print('{:<4} {:<9} {:<12f} {}'.format(n, i, distance, time_diff))
                if options.plot_to_file:
                    plotter(tsp_matrix, tour, '{}_size_{}_iter_{}'.format(options.plot_to_file, n, i))


if __name__ == "__main__":
    main()