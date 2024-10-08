# -*- coding=utf-8 -*-
r"""
collection of wrapper-commands for ffmpeg
"""
import logging
import argparse as ap
from shell_complete import ShellCompleteAction, types
from . import __version__
from . import (
    autocrop as cmd_autocrop,
    chapters_split as cmd_chapters_split,
    concat as cmd_concat,
    pop as cmd_pop,
    probe as cmd_probe,
    stack as cmd_stack,
)

class CustomFormatter(ap.ArgumentDefaultsHelpFormatter, ap.RawDescriptionHelpFormatter):
    pass


parser = ap.ArgumentParser(prog='ffmpeg-tools', description=__doc__.strip(), formatter_class=CustomFormatter)
parser.set_defaults(__cmd__=parser.print_help)
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('--debug', action='store_true',
                    help="Print additional information on failure")
parser.add_argument('--shell-completion', action=ShellCompleteAction,
                    help="Generates an auto-complete shell script. Use with `eval \"$(ffmpeg-tools --shell-completion)\"`")
subparsers = parser.add_subparsers()


def _doc(docstring: str):
    docstring = docstring.strip()
    return dict(help=docstring.split('\n', 1)[0], description=docstring, formatter_class=CustomFormatter)


#


autocrop_parser = subparsers.add_parser('autocrop', **_doc(cmd_autocrop.__doc__))
autocrop_parser.set_defaults(__cmd__=cmd_autocrop.__cmd__)
autocrop_parser.add_argument('-i', '--input', dest="input_video", type=types.file)
autocrop_parser.add_argument('-o', '--output', dest="output", type=types.file)


#


chapters_split_parser = subparsers.add_parser('chapters-split', **_doc(cmd_chapters_split.__doc__))
chapters_split_parser.set_defaults(__cmd__=cmd_chapters_split.__cmd__)
chapters_split_parser.add_argument('-i', '--input', dest="input_video", type=types.file)
chapters_split_parser.add_argument('-o', '--output', dest="output", type=types.directory, default="./")


#


concat_parser = subparsers.add_parser('concat', **_doc(cmd_concat.__doc__))
concat_parser.set_defaults(__cmd__=cmd_concat.__cmd__)
concat_parser.add_argument('-i', '--input', dest="input_videos", type=types.file, action='extend', nargs=ap.ONE_OR_MORE)
concat_parser.add_argument('-o', '--output', dest="output", type=types.file)


#


pop_parser = subparsers.add_parser('pop', **_doc(cmd_pop.__doc__))
pop_parser.set_defaults(__cmd__=cmd_pop.__cmd__)
pop_parser.add_argument('-i', '--input', dest="input_video", type=types.file)
pop_parser.add_argument('-o', '--output', dest="output", type=types.file)
pop_parser.add_argument('identifiers', nargs=ap.ONE_OR_MORE)


#


probe_parser = subparsers.add_parser('probe', **_doc(cmd_probe.__doc__))
probe_parser.set_defaults(__cmd__=cmd_probe.__cmd__)
probe_parser.add_argument('input_video', type=types.file)


#


concat_parser = subparsers.add_parser('stack', **_doc(cmd_stack.__doc__))
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
