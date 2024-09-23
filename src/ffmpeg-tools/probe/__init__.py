# -*- coding=utf-8 -*-
r"""

"""
import subprocess as sp
from pathlib import Path
from .. import core


def __cmd__(input_video: str):
    input_video = Path(input_video)
    args = [
        core.executables.ffprobe_executable(), '-hide_banner',
        '-show_format', '-show_streams', '-show_chapters',
        '-of', 'json',
        f"{input_video!s}",
    ]
    result = sp.run(args, check=True, capture_output=True, text=True)
    print(result.stdout)
