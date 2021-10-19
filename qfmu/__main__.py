

import argparse
import sys
import os
import logging

from models.lti import StateSpace
from codegen.fmi2 import Lti

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Quick FMU")
parser.add_argument("--name", default="qmodel", type=str, help="Target FMU identifier")
parser.add_argument("--dir", type=str, help="Target FMU directory")

subparsers = parser.add_subparsers(title="subcommands", dest="subcmd")
ss = subparsers.add_parser("ss", help="State space model, A, B, C, D",
                           description="Define ABCD matrices using string. The string is interpreted as a matrix with commas or spaces separating columns, and semicolons separating rows (see `numpy.matrix`). e.g. '1 2; 3 4' -> 2x2 matrix")
ss.add_argument("-A", required=False, type=str, help="A matrix")
ss.add_argument("-B", required=False, type=str, help="B matrix")
ss.add_argument("-C", required=False, type=str, help="C matrix")
ss.add_argument("-D", required=False, type=str, help="D matrix")
ss.add_argument("-x0", required=False, type=str, help="Init state values, zero vector if empty")
ss.add_argument("-u0", required=False, type=str, help="Init input values, zero vector if empty")

# tf = subparsers.add_parser("tf", help="Transfer function (not supported)")
# tf.add_argument("-n", default="1,0", type=str, help="Numerator")
# tf.add_argument("-d", default="1", type=str, help="Denominator")


args = parser.parse_args()

if args.dir is None:
    args.dir = os.getcwd()

if os.path.isdir(args.dir):
    tmpdir = os.path.join(args.dir, "tmp")
    if os.path.isdir(tmppath):
        os.removedirs(tmppath)
    os.mkdir(tmppath)
else:
    logging.error("Target fmupath does not exist.")
    
if args.subcmd == "ss":
    try:
        m = Lti(StateSpace(args.A, args.B, args.C, args.D, args.x0, args.u0), identifier=args.name)
        
        
        m.render_c()

    except ValueError as ex:
        sys.exit(ex)
else:
    sys.exit('My error message')
