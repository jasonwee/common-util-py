# -*- coding: utf-8 -*-
"""
cli module
"""

import subprocess
from . import timeout


def run(command):
    """
    Run a command and return the output and error.
    """
    # bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"
    with subprocess.Popen(command.split(), stdout=subprocess.PIPE) as process:
        output, error = process.communicate()
    return (output, error)


__all__ = [
    "timeout",
]
