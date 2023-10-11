import pathlib
import subprocess
import sys

import numpy as np
import pandas as pd

OPT = {
    "StartTime": 0.0,
    "StopTime": 1.0,
    "StepSize": 0.001,
    "RelTol": 0.0001,
    "OutputIntervalLength": 0.001,
}


def build_tf(
    identifier: str, output_dir: pathlib.Path, num: str, den: str, modelType: str = "cs"
):
    model_dir = output_dir / identifier
    model_dir.mkdir(parents=True, exist_ok=True)

    fmu_filename = model_dir / f"{identifier}.fmu"
    ref_opt_filename = model_dir / f"{identifier}_ref.opt"
    in_csv_filename = model_dir / f"{identifier}_in.csv"
    ref_csv_filename = model_dir / f"{identifier}_ref.csv"

    # Create fmu
    subprocess.run(
        [
            "qfmu",
            "tf",
            "--num",
            num,
            "--den",
            den,
            "-o",
            str(fmu_filename),
        ]
    )

    # Create opt file
    with open(ref_opt_filename, "w") as fp:
        for key, value in OPT.items():
            fp.write(f"{key}, {value}\n")

    # Create input file
    df = pd.DataFrame()
    df["time"] = np.linspace(
        OPT["StartTime"],
        OPT["StopTime"],
        int((OPT["StopTime"] - OPT["StartTime"]) / OPT["StepSize"]) + 1,
    )
    df["u1"] = np.zeros(df.shape[0])
    df["u1"].iloc[df.index > len(df) / 5] = 1.0
    df.to_csv(in_csv_filename, index=False)

    # Simulate
    sim_cmd = [
        "fmpy",
        "simulate",
        "--stop-time",
        f"{OPT['StopTime']}",
        str(fmu_filename),
        "--output-interval",
        f"{OPT['OutputIntervalLength']}",
        "--input-file",
        str(in_csv_filename),
        "--output-file",
        str(ref_csv_filename),
    ] + ["--interface-type", "CoSimulation" if modelType == "cs" else "ModelExchange"]
    subprocess.run(sim_cmd)


def build_ss(
    identifier: str,
    output_dir: pathlib.Path,
    A: str,
    B: str,
    C: str,
    nu: int,
    modelType: str = "cs",
):
    model_dir = output_dir / identifier
    model_dir.mkdir(parents=True, exist_ok=True)

    fmu_filename = model_dir / f"{identifier}.fmu"
    ref_opt_filename = model_dir / f"{identifier}_ref.opt"
    in_csv_filename = model_dir / f"{identifier}_in.csv"
    ref_csv_filename = model_dir / f"{identifier}_ref.csv"

    # Create fmu
    subprocess.run(
        [
            "qfmu",
            "ss",
            "--A",
            A,
            "--B",
            B,
            "--C",
            C,
            "-o",
            str(fmu_filename),
        ]
    )

    # Create opt file
    with open(ref_opt_filename, "w") as fp:
        for key, value in OPT.items():
            fp.write(f"{key}, {value}\n")

    # Create input file
    df = pd.DataFrame()
    df["time"] = np.linspace(
        OPT["StartTime"],
        OPT["StopTime"],
        int((OPT["StopTime"] - OPT["StartTime"]) / OPT["StepSize"]) + 1,
    )
    for i in range(nu):
        df[f"u{i+1}"] = np.zeros(df.shape[0])
        df[f"u{i+1}"].iloc[df.index > len(df) / 5] = 1.0
    df.to_csv(in_csv_filename, index=False)

    # Simulate
    sim_cmd = [
        "fmpy",
        "simulate",
        "--stop-time",
        f"{OPT['StopTime']}",
        str(fmu_filename),
        "--output-interval",
        f"{OPT['OutputIntervalLength']}",
        "--input-file",
        str(in_csv_filename),
        "--output-file",
        str(ref_csv_filename),
    ] + ["--interface-type", "CoSimulation" if modelType == "cs" else "ModelExchange"]
    subprocess.run(sim_cmd)


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        __platform__ = "win"
    elif sys.platform.startswith("linux"):
        __platform__ = "linux"
    elif sys.platform.startswith("darwin"):
        __platform__ = "darwin"
    else:
        raise Exception("Unsupported platform: " + sys.platform)

    if sys.maxsize > 2**32:
        __platform__ += "64"
    else:
        __platform__ += "32"

    examples_dir = pathlib.Path(__file__).parent.parent

    for modelType in ["me", "cs"]:
        platform_dir = examples_dir / "2.0" / modelType / __platform__
        build_tf("FirstOrder", platform_dir, "[10]", "[1,10]", modelType=modelType)
        build_tf(
            "SecondOrder", platform_dir, "[0.3]", "[4.0,1.6,1.0]", modelType=modelType
        )
        build_ss(
            "SISO",
            platform_dir,
            A="[[-1, 0],[0,-0.1]]",
            B="[[1],[1]]",
            C="[[1,1]]",
            nu=1,
            modelType=modelType,
        )
        build_ss(
            "MIMO",
            platform_dir,
            A="[[-1.0,0.0,0.0],[0.0,-2.0,0.0],[0.0,0.0,-3.0]]",
            B="[[0.0,1.0],[1.0,1.0],[-1.0,0.0]]",
            C="[[0.0,1.0,1.0],[1.0,1.0,1.0]]",
            nu=2,
            modelType=modelType,
        )
