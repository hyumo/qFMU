from qfmu.utils import str_to_1d_array, str_to_2d_array
import numpy as np
import pytest

@pytest.mark.parametrize("data,expected", [
    ("1", np.array([1], dtype=float)),
    ("1 ", np.array([1], dtype=float)),
    ("  1   ", np.array([1], dtype=float)),
    ("  1   ;", np.array([1], dtype=float)),
    ("  1   ;   ", np.array([1], dtype=float)),
])
def test_str2array_1d_scalar(data,expected):
    assert np.array_equal(str_to_1d_array(data), expected)

@pytest.mark.parametrize("data,expected", [
    ("1,2", np.array([1,2.0], dtype=float)),
    ("1,2;", np.array([1,2.0], dtype=float)),
    ("1 , 2", np.array([1,2.0], dtype=float)),
    ("1 ,   2", np.array([1,2.0], dtype=float)),
    ("1 ,   2;", np.array([1,2.0], dtype=float)),
])
def test_str2array_1d_comma_sep(data,expected):
    assert np.array_equal(str_to_1d_array(data), expected)

@pytest.mark.parametrize("data,expected", [
    ("1 2", np.array([1,2.0], dtype=float)),
    ("1 2;", np.array([1,2.0], dtype=float)),
    ("1 2  ;  ", np.array([1,2.0], dtype=float)),
    ("1   2", np.array([1,2.0], dtype=float)),
    ("1 2  ", np.array([1,2.0], dtype=float)),
    ("1    2;", np.array([1,2.0], dtype=float)),
    ("  1 2;", np.array([1,2.0], dtype=float)),
])
def test_str2array_1d_space_sep(data,expected):
    assert np.array_equal(str_to_1d_array(data), expected)

@pytest.mark.parametrize("data,expected", [
    ("1 2; 3 4", np.array([[1,2.0],[3,4]], dtype=float)),
    ("1 2  ;   3 4", np.array([[1,2.0],[3,4]], dtype=float)),
    ("   1    2  ;   3   4   ", np.array([[1,2.0],[3,4]], dtype=float)),
])
def test_str2array_2d(data,expected):
    assert np.array_equal(str_to_2d_array(data), expected)




