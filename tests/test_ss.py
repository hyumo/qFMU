import random

import numpy as np
import pytest

from qfmu import model


class TestStateSpace:
    nx = random.randint(1, 20)
    nu = random.randint(1, 20)
    ny = random.randint(1, 20)

    A = np.random.rand(nx, nx)
    B = np.random.rand(nx, nu)
    C = np.random.rand(ny, nx)
    D = np.random.rand(ny, nu)

    @pytest.mark.parametrize(
        "A,B,C,D,nx,nu,ny",
        [
            (A, None, None, None, nx, 0, nx),
            (None, B, None, None, nx, nu, nx),
            (None, None, None, D, 0, nu, ny),
            (A, B, None, None, nx, nu, nx),
            (A, None, C, None, nx, 0, ny),
            (A, None, None, D, nx, nu, ny),
            (None, B, C, None, nx, nu, ny),
            (None, B, None, D, nx, nu, ny),
            (None, None, C, D, nx, nu, ny),
            (A, B, C, None, nx, nu, ny),
            (A, None, C, D, nx, nu, ny),
            (None, B, C, D, nx, nu, ny),
            (A, B, C, D, nx, nu, ny),
        ],
    )
    def test_ctor(self, A, B, C, D, nx, nu, ny):
        m = model.StateSpace(A, B, C, D)
        assert m.nx == nx
        assert m.nu == nu
        assert m.ny == ny

    @pytest.mark.parametrize(
        "A,B,C,D",
        [
            (None, None, None, None),
            (None, None, C, None),
        ],
    )
    def test_invalid_ctor(self, A, B, C, D):
        with pytest.raises(ValueError):
            model.StateSpace(A, B, C, D)
