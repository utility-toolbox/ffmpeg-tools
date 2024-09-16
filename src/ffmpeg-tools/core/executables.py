# -*- coding=utf-8 -*-
r"""

"""
import os
import shutil
import logging
from functools import cache


__all__ = ['ffprobe_executable', 'ffmpeg_executable']


@cache
def ffprobe_executable() -> str:
    raw = os.getenv('FFPROBE', "ffprobe")
    exe = shutil.which(raw)
    if exe is None:
        raise FileNotFoundError(f"ffprobe not found for {raw!r}")
    logging.debug(f"ffprobe-executable: {exe}")
    return exe


@cache
def ffmpeg_executable() -> str:
    raw = os.getenv('FFMPEG', "ffmpeg")
    exe = shutil.which(raw)
    if exe is None:
        raise FileNotFoundError(f"ffmpeg not found for {raw!r}")
    logging.debug(f"ffmpeg-executable: {exe}")
    return exe
