"""Top-level package for qFMU."""
import pathlib
import sys

__author__ = """Hang Yu"""
__email__ = "yuhang.neu@gmail.com"
__version__ = "0.2.4"

__module_path__ = pathlib.Path(__file__).parent
__template_path__ = __module_path__ / "codegen" / "templates"
__include_path__ = __module_path__ / "codegen" / "include"

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
