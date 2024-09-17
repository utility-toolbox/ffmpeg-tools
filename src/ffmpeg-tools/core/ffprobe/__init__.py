# -*- coding=utf-8 -*-
r"""

"""
import json
import shlex
import logging
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
    logging.info(shlex.join(args))
    completed_process = sp.run(args, check=True, capture_output=True, text=True)
    logging.debug("Parsing ffprobe result to python objects")
    result = json.loads(completed_process.stdout)
    logging.debug("Converting ffprobe result to model")
    logging.debug(f"{result}")
    return FFProbe.model_validate(result)
