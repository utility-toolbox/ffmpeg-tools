# -*- coding=utf-8 -*-
r"""
Used to remove parts from a video

- 'stream:{index}' - removes a stream by index
- 'video' - removes all video streams
- 'video:{index}' - removes a video stream by index
- 'audio' - removes all audio streams
- 'audio:{index}' - removes an audio stream by index
- 'subtitle' - removes all subtitle streams
- 'subtitle:{index}' - removes a subtitle stream by index
- 'data' - removes all data streams
- 'data:{index}' - removes a data stream by index
- 'attachment' - removes all attachment streams
- 'attachment:{index}' - removes an attachment stream by index
- 'tag:{name}' - remove a tag from the metadata

e.g. ffmpeg-tools pop -i input.mp4 -o output.mp4 subtitle:3 data
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
        '-map', "0",  # take all streams
        '-map_metadata', "0",  # take all metadata
        '-map_chapters', "0",  # take all chapters
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
