# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from shell_complete import ShellCompleteAction, types
from . import __version__


parser = ap.ArgumentParser(prog='ffmpeg-tools', description=__doc__, formatter_class=ap.ArgumentDefaultsHelpFormatter)
parser.set_defaults(__cmd__=parser.print_help)
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('--shell-completion', action=ShellCompleteAction,
                    help="Generates an auto-complete shell script. Use with `eval \"$(img --shell-completion)\"`")
subparsers = parser.add_subparsers()


def main(argv=None):
    args = vars(parser.parse_args(args=argv))
    cmd = args.pop('__cmd__')
    return cmd(**args)


if __name__ == '__main__':
    main()
