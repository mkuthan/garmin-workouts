import numpy as np


def flatten(xs):
    if not xs:
        return xs
    if isinstance(xs[0], list):
        return flatten(xs[0]) + flatten(xs[1:])
    return xs[:1] + flatten(xs[1:])


def fill(x, n):
    return np.full(n, x)


def filter_empty(value):
    if isinstance(value, list):
        return [filter_empty(val) for val in value if not (val is None or val == [] or val == {})]
    elif isinstance(value, dict):
        return {
            key: filter_empty(val)
            for key, val in value.items()
            if not (val is None or val == [] or val == {})
        }
    else:
        return value


def concatenate(x, y):
    return np.concatenate((x, y))
