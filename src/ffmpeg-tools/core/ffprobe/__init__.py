# -*- coding=utf-8 -*-
r"""

"""
import json
import shlex
import subprocess as sp
from pathlib import Path
from ..executables import ffprobe_executable
from .model import FFProbe


def ffprobe(file: Path) -> FFProbe:
    args = [
        ffprobe_executable(), '-hide_banner',
        '-show_format', '-show_streams', '-show_chapters',
        '-of', 'json',
        f"{file}",
    ]
    print(shlex.join(args))
    completed_process = sp.run(args, check=True, capture_output=True, text=True)
    result = json.loads(completed_process.stdout)
    return FFProbe.model_validate(result)
