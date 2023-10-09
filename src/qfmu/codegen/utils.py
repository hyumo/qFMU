import numpy as np


def array2cstr(arr: np.ndarray) -> str:
    return (
        np.array2string(arr, separator=",")
        .replace("[", "{")
        .replace("]", "}")
        .replace("\n", "")
    )
