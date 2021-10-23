import argparse
import sys
import logging
import os

from qfmu.models.lti import StateSpace
from qfmu.codegen.fmi2 import Lti

def main():
    """Console script for qfmu."""
    parser = argparse.ArgumentParser(description="Generate standard form system FMUs through commandline")
    parser.add_argument("--name", default="qmodel", type=str, help="Target FMU identifier")
    parser.add_argument("--dir", default=os.getcwd(), type=str, help="Target FMU path")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-n", "--dry-run", help="Only print system information, use with -v.", action="store_true")

    subparsers = parser.add_subparsers(title="System form", dest="subcmd")
    ss = subparsers.add_parser("ss", help="State space model: A, B, C, D",
                            description="Define ABCD matrices using string. The string is interpreted as a matrix with commas or spaces separating columns, and semicolons separating rows. e.g. '1,2;3,4' -> 2x2 matrix")
    ss.add_argument("-A", required=False, type=str, help="A matrix")
    ss.add_argument("-B", required=False, type=str, help="B matrix")
    ss.add_argument("-C", required=False, type=str, help="C matrix")
    ss.add_argument("-D", required=False, type=str, help="D matrix")
    ss.add_argument("-x0", required=False, type=str, help="Init state values, zero vector if empty")
    ss.add_argument("-u0", required=False, type=str, help="Init input values, zero vector if empty")

    # tf = subparsers.add_parser("tf", help="Transfer function (WIP)")
    # tf.add_argument("-n", default="1,0", type=str, help="Numerator")
    # tf.add_argument("-d", default="1", type=str, help="Denominator")

    try:
        args = parser.parse_args()
        if args.subcmd == "ss":
            from qfmu.utils import str_to_1d_array, str_to_2d_array
            A = None if args.A is None or args.A=="" else str_to_2d_array(args.A)
            B = None if args.B is None or args.B=="" else str_to_2d_array(args.B)
            C = None if args.C is None or args.C=="" else str_to_2d_array(args.C)
            D = None if args.D is None or args.D=="" else str_to_2d_array(args.D)
            x0 = None if args.x0 is None or args.x0=="" else str_to_1d_array(args.x0)
            u0 = None if args.u0 is None or args.u0=="" else str_to_1d_array(args.u0)
            ss = StateSpace(A, B, C, D, x0, u0)
            m = Lti(ss, identifier=args.name)
            if args.verbose:
                logging.basicConfig(level=logging.INFO)
            if args.dry_run:
                print(f"Target FMU:\n{os.path.join(os.path.abspath(args.dir), args.name)}.fmu")
                print(f"System info:\n{ss}")
            else:
                m.buildFMU(args.dir)
        else:
            raise Exception("Unknown system form")
    except Exception as ex:
        logging.error(ex)
        return -1

    return 0

if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover