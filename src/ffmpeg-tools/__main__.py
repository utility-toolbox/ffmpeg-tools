# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from shell_complete import ShellCompleteAction, types
from . import __version__
from . import chapters_split, concat


parser = ap.ArgumentParser(prog='ffmpeg-tools', description=__doc__, formatter_class=ap.ArgumentDefaultsHelpFormatter)
parser.set_defaults(__cmd__=parser.print_help)
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('--shell-completion', action=ShellCompleteAction,
                    help="Generates an auto-complete shell script. Use with `eval \"$(ffmpeg-tools --shell-completion)\"`")
subparsers = parser.add_subparsers()


#


chapters_split_parser = subparsers.add_parser('chapters-split')
chapters_split_parser.set_defaults(__cmd__=chapters_split.__cmd__)
chapters_split_parser.add_argument('-i', '--input', dest="input_file", type=types.file)
chapters_split_parser.add_argument('-o', '--output', dest="output", type=types.directory)


#


concat_parser = subparsers.add_parser('concat')
concat_parser.set_defaults(__cmd__=concat.__cmd__)
concat_parser.add_argument('-i', '--input', dest="input_files", type=types.file, action='extend', nargs=ap.ONE_OR_MORE)
concat_parser.add_argument('-o', '--output', dest="output", type=types.file)
concat_parser.add_argument('--no-chapters', dest='no_chapters', action='store_true')


#


def main(argv=None):
    args = vars(parser.parse_args(args=argv))
    cmd = args.pop('__cmd__')
    return cmd(**args)


if __name__ == '__main__':
    main()
