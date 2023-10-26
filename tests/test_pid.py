import pathlib
import uuid
from random import uniform

import pytest
from click.testing import CliRunner

from qfmu.cli import cli
from qfmu.model.pid import PID

def any_float():
    return uniform(-100, 100)

def any_pos_float():
    return uniform(0, 100)

@pytest.mark.parametrize(
    "kp, ki, kd, tf, nx, nu, ny",
    [
        (any_float(), 0.0, 0.0, 0.0, 1, 1, 1),
        (0.0, any_float(), 0.0, 0.0, 1, 1, 1),
        (0.0, 0.0, any_float(), any_pos_float(), 1, 1, 1),
        (any_float(), any_float(), 0.0, 0.0, 1, 1, 1),
        (0.0, any_float(), any_float(), any_pos_float(), 2, 1, 1),
        (
            any_float(),
            any_float(),
            any_float(),
            any_pos_float(),
            2,
            1,
            1,
        ),
    ],
)
def test_pid(kp, ki, kd, tf, nx, nu, ny):
    m = PID(kp, ki, kd, tf)
    assert m.nx == nx
    assert m.nu == nu
    assert m.ny == ny


@pytest.mark.parametrize(
    "kp, ki, kd, T, x0, u0",
    [
        (any_float(), any_float(), any_float(), any_pos_float(), None, None),
        (any_float(), 0.0, 0.0, 0.0, None, None),
        (0.0, any_float(), 0.0, 0.0, None, None),
        (0.0, 0.0, any_float(), any_pos_float(), None, None),
        (any_float(), any_float(), 0.0, 0.0, None, None),
        (any_float(), 0.0, any_float(), any_pos_float(), None, None),
        (0.0, any_float(), any_float(), any_pos_float(), None, None),
        (0.0, any_float(), 0.0, 0.0, [2], None),
        (0.0, 0.0, any_float(), any_pos_float(), [2], None),
        (0.0, 1.0, 1.0, 1.0, [2, 2], None),
        (1.0, 1.0, 1.0, 1.0, [2, 2], None),
        (1.0, 1.0, 1.0, 1.0, [2, 2], 8),
    ],
)
def test_cli_pid(kp, ki, kd, T, x0, u0, tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        filename = f"{td}/{uuid.uuid4()}.fmu"
        result = runner.invoke(
            cli,
            [
                "pid",
                "--kp",
                f"{kp}",
                "--ki",
                f"{ki}",
                "--kd",
                f"{kd}",
                "--T",
                f"{T}",
                "--dt",
                "0.001",
                "--output",
                f"{filename}",
            ]
            + (["--x0", f"{x0}"] if x0 is not None else [])
            + (["--u0", f"{u0}"] if u0 is not None else []),
        )
        assert result.exit_code == 0
        assert pathlib.Path(filename).exists()
        assert result.output == ""


@pytest.mark.parametrize(
    "kp, ki, kd, T, x0, u0",
    [
        pytest.param(0.0, 0.0, 0.0, 0.0, None, None),
        pytest.param(0.0, 0.0, 1.0, 0.0, None, None),
        pytest.param(0.0, 0.0, 1.0, -1.0, None, None),
        pytest.param(1.0, 1.0, 1.0, 1.0, [1], None),
        pytest.param(
            1.0,
            0.0,
            0.0,
            0.0,
            [1],
            None,
            marks=pytest.mark.xfail(reason="should contain no states"),
        ),
    ],
)
def test_cli_pid_error(kp, ki, kd, T, x0, u0, tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "pid",
            "--kp",
            f"{kp}",
            "--ki",
            f"{ki}",
            "--kd",
            f"{kd}",
            "--T",
            f"{T}",
            "--dt",
            "0.001",
            "--output",
            "q.fmu",
        ]
        + (["--x0", f"{x0}"] if x0 is not None else [])
        + (["--u0", f"{u0}"] if u0 is not None else []),
    )
    assert result.exit_code != 0

