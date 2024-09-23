# -*- coding=utf-8 -*-
r"""
ffmpeg-tools pop -i input.mp4 -o output.mp4 subtitle:3 data
"""
import logging
import typing as t
from pathlib import Path
from .. import core


def __cmd__(input_video: str, output: str, identifiers: t.List[str]) -> None:
    input_video = Path(input_video).absolute()
    logging.debug(f"Input-Video: {input_video!s}")
    if not input_video.is_file():
        raise FileNotFoundError(input_video)

    output: Path = Path(output).absolute()
    logging.debug(f"Output: {output!s}")

    args = [
        '-i', f"{input_video!s}",
        '-map', "0",  # take all
        '-map_metadata', "0",
        '-map_chapters', "0",
    ]
    for identifier in identifiers:
        head, _, detail = identifier.partition(":")
        if head == "stream":
            args.extend(['-map', f"-0:{detail}"])
        elif head == "video":
            if detail:
                assert detail.isdigit()
                args.extend(['-map', f"-0:v:{detail}"])
            else:
                args.extend(['-map', f"-0:v"])
        elif head == "audio":
            if detail:
                assert detail.isdigit()
                args.extend(['-map', f"-0:a:{detail}"])
            else:
                args.extend(['-map', f"-0:a"])
        elif head == "subtitle":
            if detail:
                assert detail.isdigit()
                args.extend(['-map', f"-0:s:{detail}"])
            else:
                args.extend(['-map', f"-0:s"])
        elif head == "data":
            if detail:
                assert detail.isdigit()
                args.extend(['-map', f"-0:d:{detail}"])
            else:
                args.extend(['-map', f"-0:d"])
        elif head == "attachment":
            if detail:
                assert detail.isdigit()
                args.extend(['-map', f"-0:t:{detail}"])
            else:
                args.extend(['-map', f"-0:t"])
        elif head == "tag":
            args.extend(['-metadata', f"{detail}="])
        else:
            raise KeyError(f"unknown head: {head!r}")

    args += [
        '-c', "copy",
        f"{output!s}",
    ]
    core.ffmpeg.ffmpeg(args)
