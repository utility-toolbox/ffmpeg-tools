# -*- coding=utf-8 -*-
r"""

"""
import os
import shutil


__all__ = ['ffprobe_executable', 'ffmpeg_executable']


def ffprobe_executable() -> str:
    raw = os.getenv('FFPROBE', "ffprobe")
    exe = shutil.which(raw)
    if exe is None:
        raise FileNotFoundError(f"ffprobe not found for {raw!r}")
    return exe


def ffmpeg_executable() -> str:
    raw = os.getenv('FFMPEG', "ffmpeg")
    exe = shutil.which(raw)
    if exe is None:
        raise FileNotFoundError(f"ffmpeg not found for {raw!r}")
    return exe
