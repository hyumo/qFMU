
# qfmu

Generate standard form system **FMUs** through CLI. `q` is for quick.

Currently, `qfmu` supports:

- LTI system in state space (ABCD matrices) form.

## Installation

Install `qfmu` through PyPI

```
pip install qfmu
```

*Noted* that a proper C compiler is required on your OS. 

- `gcc` for Linux and Debian. 
- `msvc` for windows (WIP).

## HelloWorld

Generate an LTI system in state space form using the following command: 

```
qfmu --name helloWorld ss -A="1,2;3,4" -B="1;2" -C="1,0;0,1" -D="0;0"
```

If `qfmu` is installed properly, you should see a `helloWorld.fmu` file generated in your current working directory.

If you have `fmpy` installed, you can run `fmpy info hellowWorld.fmu` to see detailed model information.

```
Model Info

  FMI Version        2.0
  FMI Type           Model Exchange, Co-Simulation
  Model Name         helloWorld
  Description        None
  Platforms          c-code, linux64
  Continuous States  2
  Event Indicators   0
  Variables          10
  Generation Tool    qfmu
  Generation Date    2021-10-23 16:36:22.700250

Default Experiment

  Stop Time          1.0
  Tolerance          0.0001

Variables (input, output)

  Name               Causality              Start Value  Unit     Description
  u1                 input                          0.0           Model input 1
  y1                 output                                       Model output 1
  y2                 output                                       Model output 2
```

## Usage

```
usage: qfmu [-h] [--name NAME] [--dir DIR] [-v] [-n] {ss} ...

Generate standard form system FMUs through commandline

optional arguments:
  -h, --help     show this help message and exit
  --name NAME    Target FMU identifier
  --dir DIR      Target FMU path
  -v, --verbose  Verbose output
  -n, --dry-run  Only print system information without generating an FMU.

System form:
  {ss}
    ss           State space model: A, B, C, D
```

## Knwon issues

- No Windows support yet (WIP)

## For developers

Install required packages

```
pip install -r requirements_dev.txt 
```

Dry run bumpversion

```
make major/minor/patch
```

Make a test release to testpipy

```
make testrelease
```

Make a release manually (until gitaction works)

```
bumpversion major/minor/patch
make release
```

## Acknowledgement
- [fmusdk](https://github.com/qtronic/fmusdk)
- [fmpy](https://github.com/CATIA-Systems/FMPy)

`qfmu`'s code template is modified based on `fmusdk`. Some functions of `qfmu` is borrowed from fmpy.
