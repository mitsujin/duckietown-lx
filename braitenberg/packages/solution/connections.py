from typing import Tuple

import numpy as np


def get_motor_left_matrix(shape: Tuple[int, int]) -> np.ndarray:
    # TODO: write your function instead of this one

    half = int(shape[1]/2)
    res = np.zeros(shape=shape, dtype="float32")
    res[:]=0
    res[:, :half] = 1
   
    return res


def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
    # TODO: write your function instead of this one

    res = np.zeros(shape=shape, dtype="float32")
    half = int(shape[1]/2)
    res[:]=1
    res[:, :half] = 0

    return res
