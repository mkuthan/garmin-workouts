import numpy as np


def flatten(xs):
    if not xs:
        return xs
    if isinstance(xs[0], list):
        return flatten(xs[0]) + flatten(xs[1:])
    return xs[:1] + flatten(xs[1:])


def fill(x, n):
    return np.full(n, x)


def concatenate(x, y):
    return np.concatenate((x, y))
