import logging
import pathlib
from typing import Optional

import click

from qfmu import __version__, model
from qfmu.utils import build_fmu, str_to_arr, str_to_mat


@click.group(context_settings={"show_default": True})
@click.version_option(__version__, "-v", "--version", prog_name="qfmu")
def cli():
    logging.basicConfig(level=logging.INFO)


@cli.command()
@click.option(
    "--A", "-A", "A", type=str, default=None, help="A matrix json str, zero if empty"
)
@click.option(
    "--B",
    "-B",
    "B",
    type=str,
    default=None,
    help="B matrix json str, inferred if empty",
)
@click.option(
    "--C",
    "-C",
    "C",
    type=str,
    default=None,
    help="C matrix json str, identity matrix if empty, unless D is provided",
)
@click.option(
    "--D",
    "-D",
    "D",
    type=str,
    default=None,
    help="D matrix json str, inferred if empty",
)
@click.option(
    "--x0",
    "-x0",
    type=str,
    default=None,
    help="Initial state vector json str. Zero vector with inferred size if empty",
)
@click.option(
    "--u0",
    "-u0",
    type=str,
    default=None,
    help="Initial input vector json str. Zero vector with inferred size if empty",
)
@click.option(
    "--dt",
    "-dt",
    type=click.FloatRange(min=0.0, min_open=True),
    default=0.001,
    help="Euler integrator step size",
)
@click.option(
    "--output",
    "-o",
    default="./q.fmu",
    help="FMU Output path",
    type=click.Path(
        writable=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
def ss(
    A: Optional[str],
    B: Optional[str],
    C: Optional[str],
    D: Optional[str],
    x0: Optional[str],
    u0: Optional[str],
    dt: float,
    output: pathlib.Path,
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


@cli.command()
@click.option(
    "--num",
    "-n",
    type=str,
    required=True,
    help="Numerator polynomial coefficients as a json list of floats",
)
@click.option(
    "--den",
    "-d",
    type=str,
    required=True,
    help="Denominator polynomial coefficients as json list of floats",
)
@click.option(
    "--x0",
    "-x0",
    type=str,
    default=None,
    help="Initial state vector as a json list of floats. `zero` vector with inferred size if empty",    # noqa: E501
)
@click.option(
    "--u0",
    "-u0",
    type=float,
    default=0,
    help="Initial input value",
)
@click.option(
    "--dt",
    "-dt",
    type=click.FloatRange(min=0.0, min_open=True),
    default=0.001,
    help="Euler integrator step size",
)
@click.option(
    "--output",
    "-o",
    default="./q.fmu",
    help="FMU Output path",
    type=click.Path(
        writable=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
def tf(
    num: str,
    den: str,
    x0: Optional[str],
    u0: float,
    dt: float,
    output: pathlib.Path,
):
    """Generate a continuous-time transfer function fmu

    tf(num, den) =

    num[0]*s**(n-1) + ... + num[n-1]*s + num[n]
    -----------------------------------
    den[0]*s**(n-1) + ... + den[n-1]*s + den[n]
    """

    # TODO: Check sigle gain case for x0 and u0

    # Get filename as identifier
    if output.suffix != ".fmu":
        raise ValueError("Output file must be an FMU")
    identifier = output.stem

    # Construct a state space model
    m = model.TransferFunction(
        str_to_arr(num), str_to_arr(den), str_to_arr(x0) if x0 is not None else None, u0
    )

    # Build FMU
    build_fmu(m, output, identifier=identifier, dt=dt)


@cli.command()
@click.option(
    "--zeros", "-z", "z", type=str, required=True, help="Transfer function Zeros"
)
@click.option(
    "--poles", "-p", "p", type=str, required=True, help="Transfer function Poles"
)
@click.option(
    "--k",
    "-k",
    "k",
    type=float,
    default=1.0,
    help="Transfer function gain scalar",
)
@click.option(
    "--x0",
    "-x0",
    type=str,
    default=None,
    help="Initial state vector. `zero` vector with inferred size if empty",
)
@click.option(
    "--u0",
    "-u0",
    type=float,
    default=0,
    help="Initial input value",
)
@click.option(
    "--dt",
    "-dt",
    type=click.FloatRange(min=0.0, min_open=True),
    default=0.001,
    help="Euler integrator step size",
)
@click.option(
    "--output",
    "-o",
    default="./q.fmu",
    help="FMU Output path",
    type=click.Path(
        writable=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
def zpk(
    z: str,
    p: str,
    k: float,
    x0: Optional[str],
    u0: float,
    dt: float,
    output: pathlib.Path,
):
    """Generate a continuous-time transfer function fmu using zeros, poles and gain (zpk) representation""" # noqa: E501
    # Get filename as identifier
    if output.suffix != ".fmu":
        raise ValueError("Output file must be an FMU")
    identifier = output.stem

    # Construct a state space model
    m = model.ZerosPolesGain(
        str_to_arr(z), str_to_arr(p), k, str_to_arr(x0) if x0 is not None else None, u0
    )

    # Build FMU
    build_fmu(m, output, identifier=identifier, dt=dt)


@cli.command()
@click.option("--kp", "-kp", type=float, default=1.0, help="Proportional gain")
@click.option("--ki", "-ki", type=float, default=0.0, help="Integral gain")
@click.option("--kd", "-kd", type=float, default=0.0, help="Derivative gain")
@click.option(
    "--T",
    "-T",
    "ts",
    type=float,
    default=0.0,
    help="First-order derivative filter time constant",
)
@click.option(
    "--x0",
    "-x0",
    type=str,
    default=None,
    help="Initial state vector. `zero` vector with inferred size if empty",
)
@click.option(
    "--u0",
    "-u0",
    type=float,
    default=0,
    help="Initial input value",
)
@click.option(
    "--dt",
    "-dt",
    type=click.FloatRange(min=0.0, min_open=True),
    default=0.001,
    help="Euler integrator step size",
)
@click.option(
    "--output",
    "-o",
    default="./q.fmu",
    help="FMU Output path",
    type=click.Path(
        writable=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
def pid(
    kp: float,
    ki: float,
    kd: float,
    ts: float,
    x0: Optional[str],
    u0: float,
    dt: float,
    output: pathlib.Path,
):
    """Generate a PID controller fmu

    pid(kp, ki, kd, T) =

    kp + ki/s + kd*s/(T*s + 1)

    """
    # Get filename as identifier
    if output.suffix != ".fmu":
        raise ValueError("Output file must be an FMU")
    identifier = output.stem

    # Construct a state space model
    m = model.PID(kp, ki, kd, ts, str_to_arr(x0) if x0 is not None else None, u0)

    # Build FMU
    build_fmu(m, output, identifier=identifier, dt=dt)
