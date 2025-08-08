# -*- coding: utf-8 -*-
"""json_file module"""

import json
from typing import Any


def update(json_file: str, key: str, value: Any) -> None:
    """
    update the json file based on the key and value specified

    :param json_file: the json file where the key and value should be written to
    :param key: the key to write into the json_file
    :param value: the value that belong to the key to write into the json_file
    :returns: None

    """
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(json_file, "w", encoding="utf-8") as f:
        data[key] = value
        json.dump(data, f, indent=3, sort_keys=True)
        f.write("\n")


def get_all(json_file: str) -> str:
    """
    return the content of the json file

    :param json_file: the json file where the key and value present
    :returns: the content of the json file

    """
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.dumps(json.load(f), indent=4)
    return data


def get_value(json_file: str, key: str) -> Any:
    """
    return the value associated with the key in the specified json file

    :param json_file: the json file where the key and value present
    :param key: the key where the value is associated with
    :returns: 0 if there is not key found in the json_file. else return the
              value associated with the key

    """
    count = 0
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

        if key not in data:
            return count
        count = data[key]
    return count


def create_json_file(json_file: str, template: str) -> None:
    """
    create json file based on the template

    :param json_file: the json file about to be create
    :param template: the template use to create json_file.
    :returns: None

    """
    with open(template, "r", encoding="utf-8") as f:
        data = json.load(f)

        with open(json_file, "w", encoding="utf-8") as sf:
            json.dump(data, sf, indent=3, sort_keys=True)
            sf.write("\n")
