# -*- coding=utf-8 -*-
r"""

"""
import shlex
import logging
import typing as t
import subprocess as sp
from .executables import ffmpeg_executable


__all__ = ['ffmpeg']


def ffmpeg(args: t.List[str]) -> sp.CompletedProcess:
    args = [
        ffmpeg_executable(),
        '-hide_banner',
        '-loglevel', "warning",
        '-y',  # overwrite if existing output
    ] + args
    logging.info(shlex.join(args))
    return sp.run(args, check=True, capture_output=True, text=True)
