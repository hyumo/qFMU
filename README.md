
# qFMU

`qFMU` can **q**uickly export a classical form system as an **FMU** through CLI, for example:

- An LTI system in state space (A,B,C,D matrix) form.

## Usage

```
usage: [-h] [--name NAME] [--dir DIR] {ss,tf} ...

Quick FMU

optional arguments:
  -h, --help   show this help message and exit
  --name NAME  Target FMU identifier
  --dir DIR    Target FMU path

subcommands:
  {ss,tf}
    ss         State space model, A, B, C, D
    tf         Transfer function (WIP)
```

## Get started

Not implemented

## TODO:

Not implemented

## Development

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
