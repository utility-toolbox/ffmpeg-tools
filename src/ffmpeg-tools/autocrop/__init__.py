# -*- coding=utf-8 -*-
r"""

"""
import re
import logging
from pathlib import Path
from .. import core


def __cmd__(input_video: str, output: str) -> None:
    input_video = Path(input_video).absolute()
    logging.debug(f"Input-Video: {input_video!s}")
    if not input_video.is_file():
        raise FileNotFoundError(input_video)

    output: Path = Path(output).absolute()
    logging.debug(f"Output: {output!s}")

    pattern = re.compile(r'(?<=\s)crop=\d+:\d+:\d+:\d+(?=\s)')

    args = [
        '-i', f"{input_video!s}",
        '-vf', "cropdetect=24:16:0",
        '-t', "60",  # only detect based on the first minute (is faster)
        '-f', "null",
        '-',
    ]
    result = core.ffmpeg.ffmpeg(args)
    matches = pattern.findall(result.stderr)
    if not matches:
        raise RuntimeError(f"Could not find crop info in {input_video!s}")
    crop_dimensions = matches[-1]
    logging.info(f"Crop dimensions: {crop_dimensions!r}")

    if output.name == "-":
        return  # we only detect this time

    args = [
        '-i', f"{input_video!s}",  # input
        '-map', "0",  # keep all streams
        '-vf', f"{crop_dimensions}",  # crop
        '-c:a', "copy",  # avoid re-encoding of audio for teeny tiny performance boost
        '-c:s', "copy",  # avoid re-encoding of subtitles for teeny tiny performance boost
        '-c:d', "copy",  # avoid re-encoding of data for teeny tiny performance boost
        '-c:t', "copy",  # avoid re-encoding of attachments for teeny tiny performance boost
        f"{output!s}",  # output
    ]
    core.ffmpeg.ffmpeg(args)
