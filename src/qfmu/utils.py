import datetime
import json
import logging
import os
import pathlib
import shutil
import subprocess
import tempfile
import time
import uuid

import numpy as np
from jinja2 import Environment, FileSystemLoader, select_autoescape

from qfmu import __include_path__, __platform__, __template_path__, __version__
from qfmu.codegen.utils import array2cstr
from qfmu.model.lti import LTI

env = Environment(
    loader=FileSystemLoader(__template_path__),
    autoescape=select_autoescape(),
    trim_blocks=True,
)
env.filters["array2cstr"] = array2cstr


def str_to_mat(data: str) -> np.ndarray:
    m = np.array(json.loads(data), dtype=float)
    if len(m.shape) != 2:
        raise ValueError("Invalid matrix format.")
    return m


def str_to_arr(data: str) -> np.ndarray:
    m = np.array(json.loads(data), dtype=float)
    if len(m.shape) != 1:
        raise ValueError("Invalid array format.")
    return m


def find_vcvarsall_location():
    try:
        # Find vswhere.exe
        vswhere = rf'{os.environ["ProgramFiles(x86)"]}\Microsoft Visual Studio\Installer\vswhere.exe'  # noqa: E501
        # Run vswhere and capture its output as JSON.
        vswhere_output = subprocess.check_output(
            [
                f"{vswhere}",
                "-latest",
                "-products",
                "*",
                "-requires",
                "Microsoft.Component.MSBuild",
                "-format",
                "json",
            ]
        )

        # Parse the JSON output.
        vswhere_data = json.loads(vswhere_output.decode("utf-8"))

        if vswhere_data and isinstance(vswhere_data, list):
            # Extract the installation path from the vswhere data.
            installation_path = vswhere_data[0].get("installationPath")

            if installation_path:
                # Construct the full path to vcvarsall.bat.
                vcvarsall_path = os.path.join(
                    installation_path, "VC", "Auxiliary", "Build", "vcvarsall.bat"
                )
                return vcvarsall_path
    except subprocess.CalledProcessError:
        pass

    return None


def compile_dll(src_dir: pathlib.Path, identifier: str) -> pathlib.Path:
    if __platform__.startswith("win"):
        compiler = "vc"
    elif __platform__.startswith("darwin"):
        compiler = "clang"
    else:
        compiler = "gcc"

    if compiler == "vc":
        target = identifier + ".dll"
        toolset = "x86_amd64" if "64" in __platform__ else "x86"
        compiler_options = "/Oy /Ob1 /Oi /LD"
        cmd = rf'call "{find_vcvarsall_location()}" {toolset}'
        cmd += f" && cl {compiler_options} /I./include /DDISABLE_PREFIX /Fe{target} shlwapi.lib fmi2model.c"  # noqa: E501
    elif compiler == "gcc":
        target = identifier + ".so"
        cmd = "gcc -c -I ./include -fPIC -DDISABLE_PREFIX fmi2model.c "
        cmd += f" && gcc -static-libgcc -shared -o{target} *.o -lm"
    elif "darwin" in __platform__:
        target = identifier + ".dylib"
        cmd = "clang -c -arch x86_64 -arch arm64 -I ./include fmi2model.c"
        cmd += f" && clang -shared -arch x86_64 -arch arm64 -o{target} *.o -lm"
    else:
        raise RuntimeError("Unknown compiler")

    wd = os.getcwd()
    os.chdir(src_dir)
    status = os.system(cmd)
    os.chdir(wd)

    dll_path = src_dir / target
    if status != 0 or not dll_path.exists():
        raise Exception("Failed to compile shared library")

    return dll_path


def build_fmu(
    model: LTI,
    output: pathlib.Path = pathlib.Path("."),
    identifier: str = "model",
    dt: float = 0.001,
) -> None:
    _guid = str(uuid.uuid1())
    _datetime = str(datetime.datetime.now())

    # TODO: Support fmi3 by loading different templates
    fmu_model_tmpl = env.get_template("fmi2model.jinja")
    fmu_desc_tmpl = env.get_template("fmi2modelDescription.jinja")

    # TODO: Fix me on Windows
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = pathlib.Path(tmpdir)
        # Create folder structure
        logging.debug(f"Creating folder structure at {tmpdir}")
        bin_dir = tmpdir / "binaries"
        bin_dir.mkdir()
        platform_dir = bin_dir / __platform__
        platform_dir.mkdir()
        src_dir = tmpdir / "sources"
        src_dir.mkdir()

        # Write source files
        logging.debug(f"Writing source files to {src_dir}")
        fmu_model = fmu_model_tmpl.render(
            model=model, identifier=identifier, version=__version__, guid=_guid, dt=dt
        )
        with open(src_dir / "fmi2model.c", "w") as f:
            f.write(fmu_model)
        # Copy header files to source folder
        shutil.copytree(__include_path__, src_dir / "include")

        # Compile model
        logging.debug("Compiling dll")
        dll_path = compile_dll(src_dir, identifier=identifier)
        shutil.move(dll_path, platform_dir / dll_path.name)

        # Write model description
        logging.debug("Writing model description")
        fmu_desc = fmu_desc_tmpl.render(
            model=model,
            identifier=identifier,
            version=__version__,
            guid=_guid,
            datetime=_datetime,
            dt=dt,
        )
        with open(tmpdir / "modelDescription.xml", "w") as f:
            f.write(fmu_desc)

        # Generate FMU
        logging.debug("Generating FMU")
        zippath = shutil.make_archive(identifier, "zip", tmpdir)
        shutil.move(zippath, str(output.parent / f"{identifier}.fmu"))

        logging.info(f"FMU generated successfully at {output}")

        # FIXME:
        # - vc holds on to files for a while and prevents deletion
        # - need to delete compiler generated temp files
        if __platform__.startswith("win"):
            time.sleep(1)  # thank you windose...
            # for file in src_dir.glob("*"):
            #     if file.suffix not in [".c", ".h"]:
            #         file_path = src_dir / file
            #         file_path.unlink()
            #         print(f"Removed file: {file_path}")

        shutil.rmtree(tmpdir)
