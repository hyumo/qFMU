import logging
import pathlib
from typing import Optional

import typer

from qfmu import __version__, model
from qfmu.utils import build_fmu, str_to_arr, str_to_mat

app = typer.Typer(rich_markup_mode="rich")


@app.command()
def ss(
    A: Optional[str] = typer.Option(
        None, "--A", "-A", help="A matrix as a json str, zero if empty"
    ),  # noqa: E501
    B: Optional[str] = typer.Option(
        None, "--B", "-B", help="B matrix as a json str, inferred if empty"
    ),  # noqa: E501
    C: Optional[str] = typer.Option(
        None,
        "--C",
        "-C",
        help="C matrix as a json str, identity matrix if empty, unless D is provided",
    ),  # noqa: E501
    D: Optional[str] = typer.Option(
        None, "--D", "-D", help="D matrix as a json str, inferred if empty"
    ),  # noqa: E501
    x0: Optional[str] = typer.Option(
        None,
        "--x0",
        "-x0",
        help="Initial state vector as a json str. Zero vector if empty",
    ),
    u0: Optional[str] = typer.Option(
        None,
        "--u0",
        "-u0",
        help="Initial input vector as a json str. Zero vector if empty",
    ),
    dt: float = typer.Option(
        0.001, "--dt", "-h", help="Euler integrator step size", min=0.0
    ),
    output: pathlib.Path = typer.Option(
        "./q.fmu",
        "--output",
        "-o",
        help="FMU Output path",
        writable=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
):
    """
    Generate a continuous-time state space system fmu

    Examples:

    qfmu ss -A "[[1,2],[3,4]]" -o ./q.fmu
    - A[2, 2] = [[1.0, 2.0], [3.0, 4.0]]
    - B[2, 0] = [[], []]
    - C[2, 2] = [[1.0, 0.0], [0.0, 1.0]]
    - D[2, 0] = [[], []]
    """
    # Hanlde case where only D is provided
    A = str_to_mat(A) if A is not None else None
    B = str_to_mat(B) if B is not None else None
    C = str_to_mat(C) if C is not None else None
    D = str_to_mat(D) if D is not None else None
    x0 = str_to_arr(x0) if x0 is not None else None
    u0 = str_to_arr(u0) if u0 is not None else None

    # Get filename as identifier
    if output.suffix != ".fmu":
        raise ValueError("Output file must be an FMU")
    identifier = output.stem

    # Construct a state space model
    m = model.StateSpace(A, B, C, D, x0, u0)

    # Build FMU
    build_fmu(m, output, identifier=identifier, dt=dt)


@app.command()
def tf(
    num: str = typer.Option("--num", help="Numerator polynomial coefficients"),
    den: str = typer.Option("--den", help="Denominator polynomial coefficients"),
    x0: Optional[float] = typer.Option(
        None, "--x0", "-x0", help="Initial state vector. Zero vector if empty"
    ),
    u0: Optional[float] = typer.Option(
        None, "--u0", "-u0", help="Initial input vector. Zero vector if empty"
    ),
    dt: float = typer.Option(
        0.001, "--dt", "-h", help="Euler integrator step size", min=0.0
    ),
    output: pathlib.Path = typer.Option(
        "./q.fmu",
        "--output",
        "-o",
        help="FMU Output path",
        writable=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
):
    """Generate a continuous-time transfer function fmu

    tf(num, den) =

    num[0]*s**(n-1) + ... + num[n-1]*s + num[n]
    -----------------------------------
    den[0]*s**(n-1) + ... + den[n-1]*s + den[n]
    """
    # Get filename as identifier
    if output.suffix != ".fmu":
        raise ValueError("Output file must be an FMU")
    identifier = output.stem

    # Construct a state space model
    m = model.TransferFunction(str_to_arr(num), str_to_arr(den), x0, u0)

    # Build FMU
    build_fmu(m, output, identifier=identifier, dt=dt)


@app.command()
def pid(
    kp: float = typer.Option(0.0, "--kp", help="Proportional gain"),
    ki: float = typer.Option(0.0, "--ki", help="Integral gain"),
    kd: float = typer.Option(0.0, "--kd", help="Derivative gain"),
    T: float = typer.Option(
        0.0, "--T", "-T", help="First-order derivative filter time constant"
    ),  # noqa: E501
    x0: Optional[float] = typer.Option(
        None, "--x0", "-x0", help="Initial state vector. Zero vector if empty"
    ),
    u0: Optional[float] = typer.Option(
        None, "--u0", "-u0", help="Initial input vector. Zero vector if empty"
    ),
    dt: float = typer.Option(
        0.001, "--dt", "-h", help="Euler integrator step size", min=0.0
    ),
    output: pathlib.Path = typer.Option(
        "./q.fmu",
        "--output",
        "-o",
        help="FMU Output path",
        writable=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
):
    """Generate a PID controller fmu

    pid(kp, ki, kd) =

    kp + ki/s + kd*s/(tf*s + 1)

    """
    # Get filename as identifier
    if output.suffix != ".fmu":
        raise ValueError("Output file must be an FMU")
    identifier = output.stem

    # Construct a state space model
    m = model.PID(kp, ki, kd, T, x0, u0)

    # Build FMU
    build_fmu(m, output, identifier=identifier, dt=dt)


def version_callback(value: bool):
    if value:
        typer.echo(f"qfmu version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    logging.basicConfig(level=logging.INFO)
    return


if __name__ == "__main__":
    app()
