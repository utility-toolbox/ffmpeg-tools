# -*- coding=utf-8 -*-
r"""

"""
import logging
import argparse as ap
from shell_complete import ShellCompleteAction, types
from . import __version__
from . import chapters_split as cmd_chapters_split, concat as cmd_concat, stack as cmd_stack


parser = ap.ArgumentParser(prog='ffmpeg-tools', description=__doc__, formatter_class=ap.ArgumentDefaultsHelpFormatter)
parser.set_defaults(__cmd__=parser.print_help)
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('--debug', action='store_true',
                    help="Print additional information on failure")
parser.add_argument('--shell-completion', action=ShellCompleteAction,
                    help="Generates an auto-complete shell script. Use with `eval \"$(ffmpeg-tools --shell-completion)\"`")
subparsers = parser.add_subparsers()


#


chapters_split_parser = subparsers.add_parser('chapters-split')
chapters_split_parser.set_defaults(__cmd__=cmd_chapters_split.__cmd__)
chapters_split_parser.add_argument('-i', '--input', dest="input_video", type=types.file)
chapters_split_parser.add_argument('-o', '--output', dest="output", type=types.directory)


#


concat_parser = subparsers.add_parser('concat')
concat_parser.set_defaults(__cmd__=cmd_concat.__cmd__)
concat_parser.add_argument('-i', '--input', dest="input_videos", type=types.file, action='extend', nargs=ap.ONE_OR_MORE)
concat_parser.add_argument('-o', '--output', dest="output", type=types.file)


#


concat_parser = subparsers.add_parser('stack')
concat_parser.set_defaults(__cmd__=cmd_stack.__cmd__)
concat_parser.add_argument('-d', '--direction', dest="direction", type=cmd_stack.Direction,
                           choices=[d.value.lower() for d in cmd_stack.Direction], default=cmd_stack.Direction.LTR)
concat_parser.add_argument('-i', '--input', dest="input_videos", type=types.file, action='extend', nargs=ap.ONE_OR_MORE)
concat_parser.add_argument('-o', '--output', dest="output", type=types.file)


#


def configure_logging():
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="{levelname:.3} | {message}",
        style="{",
        handlers=[logging.StreamHandler()]
    )


def main(argv=None, reraise: bool = False):
    args = vars(parser.parse_args(args=argv))
    cmd = args.pop('__cmd__')
    debug = args.pop('debug')
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.debug(f"Running ffmpeg-tools command: {cmd.__module__} with {args}")
    try:
        return cmd(**args)
    except Exception as error:
        logging.error(f"{type(error).__name__}: {error}", exc_info=error if debug else False)
        if reraise:
            raise error


if __name__ == '__main__':
    configure_logging()
    main()
