# -*- coding: utf-8 -*-
"""files module"""

import threading
import json

global_lock = threading.Lock()


# https://gist.github.com/rahulrajaram/5934d2b786ed2c29dc418fafaa2830ad
def write_to_file(filename: str, content: str) -> None:
    """
    write content to file

    :param filename: the file to write content to
    :param content: the content to write to the file
    :returns: None

    """
    with global_lock:
        with open(filename, "a+", encoding="utf-8") as file:
            file.write(content)


def write_list_dict_to_file(filename: str, rows: list) -> None:
    """
    write list of dictionary to file

    :param filename: the file to write content to
    :param rows: the list of dictionary to write to the file
    :returns: None

    """
    with open(filename, "w", encoding="utf-8") as fout:
        json.dump(rows, fout, indent=4, default=str, sort_keys=False)
