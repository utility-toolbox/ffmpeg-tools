# -*- coding=utf-8 -*-
r"""

"""
import shlex
import logging
import tempfile
import typing as t
import subprocess as sp
from pathlib import Path
from .. import core


def __cmd__(input_videos: t.List[str], output: str) -> None:
    input_videos: t.List[Path] = [
        Path(input_file).absolute()
        for input_file in input_videos
    ]
    logging.debug(f"Input-Videos: {', '.join(map(str, input_videos))}")
    missing = [i for i in input_videos if not i.is_file()]
    if missing:
        raise FileNotFoundError(', '.join(map(str, missing)))

    output: Path = Path(output).absolute()

    video_infos = [
        core.ffprobe.ffprobe(file=input_file)
        for input_file in input_videos
    ]

    with tempfile.NamedTemporaryFile(mode='w+', suffix=".txt") as input_spec, \
            tempfile.NamedTemporaryFile(mode='w+', suffix=".txt", delete=False) as metadata:

        logging.info("Generating playlist and chapter-meta")
        metadata.write(f";FFMETADATA1\n")
        current_position = 0
        for i, (input_file, video_info) in enumerate(zip(input_videos, video_infos)):
            input_file: Path
            video_info: core.ffprobe.FFProbe
            safe_path = str(input_file).replace(r"'", r"\'")
            input_spec.write(f"file '{safe_path}'\n")

            main_stream = video_info.main_stream
            start: int = current_position
            end: int = start + round(video_info.format.duration / main_stream.time_base)
            metadata.write(f"\n")
            metadata.write(f"[CHAPTER]\n")
            metadata.write(f"TIMEBASE={main_stream.time_base}\n")
            metadata.write(f"START={start}\n")
            metadata.write(f"END={end}\n")
            metadata.write(f"title=Chapter {i+1}\n")
            current_position = end

        input_spec.flush()
        metadata.flush()

        args = [
            core.executables.ffmpeg_executable(), '-hide_banner',
            '-loglevel', "warning",
            '-y',
            '-safe', "0",
            '-f', "concat",
            '-i', f"file:{input_spec.name}",
            '-i', f"file:{metadata.name}",
            '-map', "0",
            '-map_metadata', "0",
            '-c', "copy",
            f"file:{output}",
        ]
        logging.info(shlex.join(args))
        sp.run(args, check=True, capture_output=True, text=True)
