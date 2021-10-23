
# qfmu

Generate standard form system **FMUs** through CLI.

Currently, `qfmu` supports:

- LTI system in state space (ABCD matrices) form.

## Installation

*NOTED that a proper C compiler is required on your OS. gcc for Linux or Debian. msvc for windows (WIP).

Installation through PyPI

```
pip install qfmu
```
## HelloWorld

Generate an LTI system in state space form using the following command: 

```
qfmu --name helloWorld ss -A="1,2;3,4" -B="1;2" -C="1,0;0,1" -D="[0;0]"
```

If `qfmu` is installed properly, you should see a `helloWorld.fmu` file generated in your current working directory.

## Usage

```
usage: qfmu [-h] [--name NAME] [--dir DIR] [-v] [-n] {ss} ...

Generate standard form system FMUs through commandline

optional arguments:
  -h, --help     show this help message and exit
  --name NAME    Target FMU identifier
  --dir DIR      Target FMU path
  -v, --verbose  Verbose output
  -n, --dry-run  Only print system information, use with -v.

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
make patch
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
