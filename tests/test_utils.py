import sys

import numpy as np
import pytest

from qfmu.utils import find_vcvarsall_location, str_to_arr, str_to_mat


def test_str_to_mat():
    assert np.array_equal(str_to_mat("[[1,2],[3,4]]"), np.array([[1, 2], [3, 4]]))


def test_str_to_arr():
    assert np.array_equal(str_to_arr("[1,2,3,4]"), np.array([1, 2, 3, 4]))


@pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="This test is only for Windows"
)
def test_find_vcvarsall_location():
    assert find_vcvarsall_location() is not None
