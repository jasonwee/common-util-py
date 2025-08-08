# -*- coding: UTF-8 -*-
#
#   Copyright Jason Wee
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
import re


# Regular expression to match a valid hex color code
hex_color_pattern = re.compile(r'^[a-fA-F0-9]{6}$')

def is_valid_hex_color(color: str) -> bool:
    return bool(hex_color_pattern.match(color))

def bold(msg: str) -> str:
    return f"<b>{msg}</b>"

def color_text(msg: str, color: str) -> str:
    return f'<font color="#{color}">{msg}</font>'

def console2texthtml(line: str, colors: dict) -> tuple[str, str]:
    """
    Receive formatted line from console and return a tuple of two strings.
    The first return string is the text string.
    The second return string is the formatted string.
    """
    if not line:
        return ("", "")
    # split at reset delimiter
    parts = line.split("\x1b[0m")
    parts = [p for p in parts if p]
    newparts = []
    newparts_txt = []
    for p in parts:
        subparts = p.split("\x1b[")
        subparts = [sp for sp in subparts if sp]
        newsubparts = []
        newsubparts_txt = []
        for sp in subparts:
            if "m" in sp:
                code, text = sp.split('m', 1)
                code = code.split(";") if ";" in code else [code]

                # https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
                color = None
                if "30" in code:      # black
                    color = colors.get("black")
                elif "31" in code:    # red
                    color = colors.get("red")
                elif "32" in code:    # green
                    color = colors.get("green")
                elif "33" in code:    # yellow
                    color = colors.get("yellow")
                elif "34" in code:    # blue
                    color = colors.get("blue")
                elif "35" in code:    # magenta
                    color = colors.get("magenta")
                elif "36" in code:    # cyan
                    color = colors.get("cyan")

                txt = text
                text = bold(color_text(text, color=color)) if color else sp
            else:
                text = txt = sp
            newsubparts.append(text)
            newsubparts_txt.append(txt)
        newparts.append("".join(newsubparts))
        newparts_txt.append("".join(newsubparts_txt))
    newline = "".join(newparts)
    newline_txt = "".join(newparts_txt)
    return (newline_txt, newline)
