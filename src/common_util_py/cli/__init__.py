# -*- coding: utf-8 -*-
#
#   Copyright WeeTech Developer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
