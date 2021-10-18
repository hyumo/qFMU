

import argparse

parser = argparse.ArgumentParser(description="Quick FMU")

subparsers = parser.add_subparsers(title="subcommands", dest="sys")

ss = subparsers.add_parser("ss", help="State space model, A, B, C, D", description="Define ABCD matrices using string. The string is interpreted as a matrix with commas or spaces separating columns, and semicolons separating rows (see `numpy.matrix`). e.g. '1 2; 3 4' -> 2x2 matrix")
ss.add_argument("-a", default="", type=str, help="A matrix")
ss.add_argument("-b", default="", type=str, help="B matrix")
ss.add_argument("-c", default="", type=str, help="C matrix")
ss.add_argument("-d", default="", type=str, help="D matrix")

tf = subparsers.add_parser("tf", help="Transfer function")
tf.add_argument("-n", default="1,0", type=str, help="Numerator")
tf.add_argument("-d", default="1", type=str, help="Denominator")


# parser.parse_args(['--help'])

# print(parser.parse_args(['ss', '-h']))
args = parser.parse_args(['ss', '-a', '1,2;3,4'])
print(args)
