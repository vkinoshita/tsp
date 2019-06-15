from itertools import permutations
from time import time
from math import factorial
import numpy as np
import sys
from tools.calculators import calculate_total_dist, get_matrix_of_distances


def solve_tsp_by_brute_force(tsp_matrix):
    start = time()
    matrix_of_distances = get_matrix_of_distances(tsp_matrix)
    length = len(tsp_matrix)
    tour = range(length)
    best_distance = sys.float_info.max
    best_tour = tour
    for p in permutations(range(1, length)):
        o = [0, *p]
        dist = calculate_total_dist(matrix_of_distances, o)
        if dist < best_distance:
            best_distance = dist
            best_tour = o
    time_diff = time() - start
    return best_tour, time_diff, best_distance


# old
# [0.0011088848114013672, 0.0009789466857910156, 0.0010008811950683594, 0.0009694099426269531, 0.001012563705444336, 0.001024484634399414, 0.001096487045288086, 0.0009911060333251953, 0.0011744499206542969, 0.0011119842529296875]
# [0.005197048187255859, 0.005281925201416016, 0.004629850387573242, 0.0034558773040771484, 0.0027763843536376953, 0.002459287643432617, 0.002122640609741211, 0.0020449161529541016, 0.0019001960754394531, 0.0017170906066894531]
# [0.009023427963256836, 0.007929325103759766, 0.007262229919433594, 0.008108377456665039, 0.00723719596862793, 0.006911039352416992, 0.0072307586669921875, 0.0068323612213134766, 0.007181882858276367, 0.0066928863525390625]
# [0.05287051200866699, 0.05030369758605957, 0.05162811279296875, 0.04960012435913086, 0.05033087730407715, 0.04989743232727051, 0.05060219764709473, 0.0494081974029541, 0.04989910125732422, 0.04998469352722168]
# [0.4152235984802246, 0.41158056259155273, 0.41223573684692383, 0.409696102142334, 0.4134976863861084, 0.4105360507965088, 0.4105346202850342, 0.41227293014526367, 0.411175012588501, 0.4083414077758789]
# [3.764982223510742, 3.7860453128814697, 3.816568613052368, 3.7764251232147217, 3.795814037322998, 3.7720043659210205, 3.767280101776123, 3.7885007858276367, 3.85619854927063, 4.0159993171691895]
# [38.640012979507446, 37.92974138259888, 38.04339408874512, 37.52380895614624, 38.016191244125366, 37.6026508808136, 37.565834522247314, 37.629249811172485, 37.58971571922302, 37.76301598548889]
# [403.7452356815338, 402.54881501197815, 404.0340030193329, 400.4472813606262, 404.7036600112915, 404.4255771636963, 411.50672364234924, 402.3145864009857, 401.47808814048767, 402.40224051475525]
# [4869.213384628296, 4871.113903045654, 4905.414040565491, 4867.206059217453, 4914.4232811927795, 4862.184355020523, 4867.441803216934, 4881.578690290451, 4873.287194728851, 5122.846216917038]

# 3	7.03334808349609E-05
# 4	4.17232513427734E-05
# 5	7.41481781005859E-05
# 6	0.00031852722168
# 7	0.001881837844849
# 8	0.014723062515259
# 9	0.124704122543335
# 10	1.2450053691864
# 11	12.9412565231323
# 12	159.082767963409
# 13	1995.33811807632
# 14	26806.4642205238