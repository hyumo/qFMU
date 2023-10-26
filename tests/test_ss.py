import json
import pathlib
import random
import uuid

import numpy as np
import pytest
from click.testing import CliRunner

from qfmu import model
from qfmu.cli import cli


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

    @pytest.mark.parametrize(
        "A,B,C,D,x0,u0",
        [
            (A, None, None, None, None, None),
            (None, B, None, None, None, None),
            (None, None, None, D, None, None),
            (A, B, None, None, None, None),
            (A, None, C, None, None, None),
            (A, None, None, D, None, None),
            (None, B, C, None, None, None),
            (None, B, None, D, None, None),
            (None, None, C, D, None, None),
            (A, B, C, None, None, None),
            (A, None, C, D, None, None),
            (None, B, C, D, None, None),
            (A, B, C, D, None, None),
            (A, None, None, None, np.zeros(nx), None),
            (None, B, None, None, np.zeros(nx), None),
            (A, B, None, None, np.zeros(nx), None),
            (A, None, C, None, np.zeros(nx), None),
            (A, None, None, D, np.zeros(nx), None),
            (None, B, C, None, np.zeros(nx), None),
            (None, B, None, D, np.zeros(nx), None),
            (None, None, C, D, np.zeros(nx), None),
            (A, B, C, None, np.zeros(nx), None),
            (A, None, C, D, np.zeros(nx), None),
            (None, B, C, D, np.zeros(nx), None),
            (A, B, C, D, np.zeros(nx), None),
            (None, B, None, None, None, np.zeros(nu)),
            (None, None, None, D, None, np.zeros(nu)),
            (A, B, None, None, None, np.zeros(nu)),
            (A, None, None, D, None, np.zeros(nu)),
            (None, B, C, None, None, np.zeros(nu)),
            (None, B, None, D, None, np.zeros(nu)),
            (None, None, C, D, None, np.zeros(nu)),
            (A, B, C, None, None, np.zeros(nu)),
            (A, None, C, D, None, np.zeros(nu)),
            (None, B, C, D, None, np.zeros(nu)),
            (A, B, C, D, None, np.zeros(nu)),
            (None, B, None, None, np.zeros(nx), np.zeros(nu)),
            (A, B, None, None, np.zeros(nx), np.zeros(nu)),
            (A, None, None, D, np.zeros(nx), np.zeros(nu)),
            (None, B, C, None, np.zeros(nx), np.zeros(nu)),
            (None, B, None, D, np.zeros(nx), np.zeros(nu)),
            (None, None, C, D, np.zeros(nx), np.zeros(nu)),
            (A, B, C, None, np.zeros(nx), np.zeros(nu)),
            (A, None, C, D, np.zeros(nx), np.zeros(nu)),
            (None, B, C, D, np.zeros(nx), np.zeros(nu)),
            (A, B, C, D, np.zeros(nx), np.zeros(nu)),
        ],
    )
    def test_cli_ss(self, A, B, C, D, x0, u0, tmp_path):
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            filename = f"{td}/{uuid.uuid4()}.fmu"
            result = runner.invoke(
                cli,
                [
                    "ss",
                    "--dt",
                    "0.001",
                    "--output",
                    f"{filename}",
                ]
                + (["--A", json.dumps(A.tolist())] if A is not None else [])
                + (["--B", json.dumps(B.tolist())] if B is not None else [])
                + (["--C", json.dumps(C.tolist())] if C is not None else [])
                + (["--D", json.dumps(D.tolist())] if D is not None else [])
                + (["--x0", json.dumps(x0.tolist())] if x0 is not None else [])
                + (["--u0", json.dumps(u0.tolist())] if u0 is not None else [])
            )
            assert result.exit_code == 0
            assert pathlib.Path(filename).exists()
            assert result.output == ""
