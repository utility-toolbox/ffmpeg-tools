# -*- coding=utf-8 -*-
r"""

"""
import shlex
import logging
import subprocess as sp
from pathlib import Path

from .. import core


def __cmd__(input_video: str, output: str) -> None:
    input_video = Path(input_video).absolute()
    logging.debug(f"Input-Video: {input_video!s}")
    if not input_video.is_file():
        raise FileNotFoundError(input_video)

    output = Path(output).absolute()
    if "%d" not in output.name:
        output = output / ("%d" + input_video.suffix)
    logging.debug(f"Output-Path: {output!s}")

    logging.debug(f"Ensuring output directory: {output.parent!s}")
    output.parent.mkdir(exist_ok=True)

    video_info = core.ffprobe.ffprobe(file=input_video)
    logging.info(f"Found {len(video_info.chapters)} found")

    for i, chapter in enumerate(video_info.chapters):
        logging.info(f"Extracting chapter {chapter.tags.get('title', i+1)!r}")
        current_output = output.with_name(output.name % (i + 1)).absolute()
        args = [
            core.executables.ffmpeg_executable(), '-hide_banner',
            '-loglevel', "warning",
            '-y',  # overwrite if existing output
            '-i', f"file:{input_video}",  # input file
            '-ss', f"{chapter.start_time}",  # start-time
            '-to', f"{chapter.end_time}",  # end-time
            '-map', "0",  # keep all streams
            '-c', "copy",  # copy (don't re-encode)
            f"file:{current_output}",  # output
        ]
        logging.info(shlex.join(args))
        sp.run(args, check=True)
    else:
        logging.info("Chapter-splitting completed")
