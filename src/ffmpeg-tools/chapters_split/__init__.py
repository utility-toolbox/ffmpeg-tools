# -*- coding=utf-8 -*-
r"""

"""
import logging
from pathlib import Path
from .. import core


def __cmd__(input_video: str, output: str) -> None:
    input_video = Path(input_video).absolute()
    logging.debug(f"Input-Video: {input_video!s}")
    if not input_video.is_file():
        raise FileNotFoundError(input_video)

    output = Path(output).absolute()
    if not contains_valid_interpolation_pattern(output.name):
        output = output / ("%s" + input_video.suffix)
    logging.debug(f"Output-Path: {output!s}")

    logging.debug(f"Ensuring output directory: {output.parent!s}")
    output.parent.mkdir(exist_ok=True)

    video_info = core.ffprobe.ffprobe(file=input_video)
    logging.info(f"Found {len(video_info.chapters)} found")

    for i, chapter in enumerate(video_info.chapters):
        logging.info(f"Extracting chapter {chapter.tags.get('title', i+1)!r}")
        new_name = format_name(output.name, title=chapter.tags.get('title', None), chapter=i+1)
        current_output = output.with_name(new_name).absolute()
        args = [
            '-i', f"file:{input_video!s}",  # input file
            '-ss', f"{chapter.start_time}",  # start-time
            '-to', f"{chapter.end_time}",  # end-time
            '-map', "0",  # keep all streams
            '-c', "copy",  # copy (don't re-encode)
            f"file:{current_output!s}",  # output
        ]
        core.ffmpeg.ffmpeg(args)
    else:
        logging.info("Chapter-splitting completed")


def contains_valid_interpolation_pattern(name: str) -> bool:
    return (name.count("%d") + name.count("%s")) == 1


def format_name(name: str, title: str, chapter: int):
    if "%s" in name:
        return (name % title) if title else (name % f"Chapter {chapter}")
    return name % chapter
