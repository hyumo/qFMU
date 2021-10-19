import pytest

import numpy as np
import random

from qfmu.models.lti import StateSpace


class TestStateSpace:

    nx = random.randint(1, 10)
    nu = random.randint(1, 10)
    ny = random.randint(1, 10)

    A = np.random.rand(nx, nx)
    B = np.random.rand(nx, nu)
    C = np.random.rand(ny, nx)
    D = np.random.rand(ny, nu)

    @pytest.mark.parametrize("A,B,C,D,nx,nu,ny", [
        (A, B, C, D, nx, nu, ny),
        (A, B, C, None, nx, nu, ny),
        (A, B, None, None, nx, nu, nx),
        (A, None, None, None, nx, 0, nx),
        (None, None, None, D, 0, nu, ny),
    ])
    def test_ctor(self, A, B, C, D, nx, nu, ny):
        ss = StateSpace(A, B, C, D)
        assert ss.nx == nx
        assert ss.nu == nu
        assert ss.ny == ny

    @pytest.mark.parametrize("A,B,C,D", [
        (None, None, None, None),
        (None, B, None, None),
        (None, B, C, None),
        (None, B, C, D),
        (None, None, C, None),
        (None, None, C, D),
    ])
    def test_invalid_ctor(self, A, B, C, D):
        with pytest.raises(ValueError):
            StateSpace(A, B, C, D)
