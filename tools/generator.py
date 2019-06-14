import random
import numpy as np


def random_100():
    return random.random() * 100


def random_x_y():
    return (random_100(), random_100())


def get_n_random_x_y(n):
    m = [random_x_y() for x in range(0, n)]
    return np.matrix(m)


def random_10000_as_integer():
    return random.randint(0, 10000)


def random_x_y_as_integer():
    return (random_10000_as_integer(), random_10000_as_integer())


def get_n_random_x_y_as_integer(n):
    m = []
    for i in range(n):
        c = random_x_y_as_integer()
        while c in m:
            c = random_x_y_as_integer()
        m = [*m, c]
    return np.matrix(m)
