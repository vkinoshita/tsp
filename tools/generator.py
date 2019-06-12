import random
import numpy as np


def random_100():
    return random.random() * 100

def random_x_y():
    return (random_100(), random_100())

def get_n_random_x_y(n):
    m = [random_x_y() for x in range(0, n)]
    return np.matrix(m)
