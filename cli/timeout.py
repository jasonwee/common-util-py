# -*- coding: utf-8 -*-
"""
Timeout script for CUDA applications

Only work for linux since it use singal.SIGALRM
"""

import logging
import os
import signal
import subprocess
import sys


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

try:
    TIMEOUT_NO_ACTIVITY_SECONDS = int(os.getenv("TIMEOUT_NO_ACTIVITY_SECONDS", "60"))
except (ValueError, TypeError):
    TIMEOUT_NO_ACTIVITY_SECONDS = 60


class CUDAException(Exception):
    """CUDA error exception"""


class TimeoutException(Exception):
    """Time out exception"""


def timeout_handler(signum, frame):
    """Timeout handler"""
    raise TimeoutException(
        f"No activity from app for {TIMEOUT_NO_ACTIVITY_SECONDS} seconds"
    )


def execute(cmd):
    """
    Execute a command, restarting on CUDA errors or inactivity.
    Args:
        cmd (list): The command and arguments to run as a subprocess.
    """
    signal.signal(signal.SIGALRM, timeout_handler)

    shutdown = False
    while not shutdown:
        with subprocess.Popen(
            cmd,
            bufsize=0,  # unbuffered so immediately print out
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        ) as proc:
            try:
                signal.alarm(TIMEOUT_NO_ACTIVITY_SECONDS)
                for line in iter(proc.stdout.readline, ""):
                    line = line.strip()
                    logging.info(line)
                    if line.startswith("CUDA error"):
                        raise CUDAException("****** Restarting due to CUDA error")
                    signal.alarm(TIMEOUT_NO_ACTIVITY_SECONDS)
            except (CUDAException, TimeoutException) as e:
                logging.error(str(e))
            except KeyboardInterrupt:
                shutdown = True

        signal.alarm(0)

        proc.send_signal(signal.SIGINT)

        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            logging.error("app didn't shutdown within 5 seconds")
            proc.kill()


if __name__ == "__main__":
    execute(sys.argv[1:])
