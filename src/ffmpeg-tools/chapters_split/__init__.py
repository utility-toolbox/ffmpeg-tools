# -*- coding=utf-8 -*-
r"""

"""
import shlex
import subprocess as sp
import sys
from pathlib import Path

from .. import core


def __cmd__(input_file: str, output: str):
    input_file = Path(input_file).absolute()
    if not input_file.is_file():
        raise FileNotFoundError(input_file)

    output = Path(output).absolute()
    if "%d" not in output.name:
        output = output / ("%d" + input_file.suffix)

    output.parent.mkdir(exist_ok=True)

    video_info = core.ffprobe.ffprobe(file=input_file)

    for i, chapter in enumerate(video_info.chapters):
        current_output = output.with_name(output.name % (i + 1)).absolute()
        args = [
            core.executables.ffmpeg_executable(), '-hide_banner',
            '-loglevel', "warning",
            '-y',  # overwrite if existing output
            '-i', f"file:{input_file}",  # input file
            '-ss', f"{chapter.start_time}",  # start-time
            '-to', f"{chapter.end_time}",  # end-time
            '-map', "0",  # keep all streams
            '-c', "copy",  # copy (don't re-encode)
            f"file:{current_output}",  # output
        ]
        print(shlex.join(args))
        try:
            sp.run(args, check=True)
        except sp.CalledProcessError as e:
            print(e.stderr, file=sys.stderr)
