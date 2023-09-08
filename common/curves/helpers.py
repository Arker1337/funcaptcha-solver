import numpy as np


def is_numeric(val):
    return isinstance(val, (float, int, np.int32, np.int64, np.float32, np.float64))


def is_list_of_points(input_list):
    if not isinstance(input_list, list):
        return False
    try:
        return all(map(lambda p: ((len(p) == 2) and is_numeric(p[0]) and is_numeric(p[1])), input_list))
    except (KeyError, TypeError) as e:
        return False
