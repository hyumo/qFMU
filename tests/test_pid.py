import pytest

from qfmu.model.pid import PID


@pytest.mark.parametrize(
    "kp, ki, kd, tf, nx, nu, ny",
    [
        (8.8, 0.0, 0.0, 0.0, 1, 1, 1),
        (0.0, 8.8, 0.0, 0.0, 1, 1, 1),
        (0.0, 0.0, 1.0, 1.0, 1, 1, 1),
        (1.0, 1.0, 0.0, 0.0, 1, 1, 1),
        (0.0, 1.0, 1.0, 1.0, 2, 1, 1),
        (1.0, 1.0, 1.0, 1.0, 2, 1, 1),
    ],
)
def test_pid(kp, ki, kd, tf, nx, nu, ny):
    m = PID(kp, ki, kd, tf)
    assert m.nx == nx
    assert m.nu == nu
    assert m.ny == ny
