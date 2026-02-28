# -*- coding: utf-8 -*-
"""
cli module
"""

import subprocess
from . import timeout


def run(command: list[str]) -> tuple[bytes, bytes | None]:
    """
    Run a command and return the output and error.
    """
    # bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"
    with subprocess.Popen(command, stdout=subprocess.PIPE) as process:
        output, error = process.communicate()
    return (output, error)


__all__ = [
    "timeout",
]
