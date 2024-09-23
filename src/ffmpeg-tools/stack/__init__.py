# -*- coding=utf-8 -*-
r"""

"""
import enum
import logging
import typing as t
from pathlib import Path
from .. import core


def __cmd__(input_videos: t.List[str], output: str, direction: 'Direction') -> None:
    input_videos: t.List[Path] = [
        Path(input_file).absolute()
        for input_file in input_videos
    ]
    logging.debug(f"Input-Videos: {', '.join(map(str, input_videos))}")
    missing = [i for i in input_videos if not i.is_file()]
    if missing:
        raise FileNotFoundError(', '.join(map(str, missing)))

    if direction in {Direction.RTL, Direction.BTT}:
        input_videos.reverse()

    output: Path = Path(output).absolute()
    logging.debug(f"Output: {output!s}")

    stack_mode = "hstack" if direction in {Direction.LTR, Direction.RTL} else "vstack"

    args = [
        *(_ for input_video in input_videos for _ in ['-i', f"file:{input_video!s}"]),
        '-filter_complex', f"{stack_mode}=inputs={len(input_videos)}",  # stacking
        '-an',  # no audio
        '-sn',  # no subtitles
        f"file:{output!s}",  # output
    ]
    core.ffmpeg.ffmpeg(args)


class Direction(enum.Enum):
    LTR = "ltr"
    RTL = "rtl"
    TTB = "ttb"
    BTT = "bbt"
