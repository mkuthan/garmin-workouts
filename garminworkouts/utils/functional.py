from typing import Any
import numpy as np
from numpy.typing import NDArray


def flatten(xs) -> Any:
    result: list[Any] = []
    for x in xs:
        if isinstance(x, list):
            result.extend(flatten(x))
        else:
            result.append(x)
    return result


def fill(x, n) -> Any:
    return np.full(n, x)


def filter_empty(value) -> Any:
    if isinstance(value, list):
        return [filter_empty(val) for val in value if val not in (None, [], {})]
    elif isinstance(value, dict):
        return {key: filter_empty(val) for key, val in value.items() if val not in (None, [], {})}
    return value


def concatenate(x, y) -> NDArray[Any]:
    return np.concatenate((x, y))
