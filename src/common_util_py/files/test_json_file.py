# -*- coding: utf-8 -*-
"""
Unit tests for json_file.py
"""

import os
import json
import tempfile
import pytest
from files import json_file


def test_update_and_get_value():
    """
    test update and get value
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "data.json")
        # Start with empty dict
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f)
        json_file.update(path, "foo", 123)
        assert json_file.get_value(path, "foo") == 123
        # Update value
        json_file.update(path, "foo", 456)
        assert json_file.get_value(path, "foo") == 456


def test_get_value_missing_key():
    """
    test get value missing key
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "data.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"a": 1}, f)
        assert json_file.get_value(path, "notfound") == 0


def test_get_all():
    """
    test get all
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "data.json")
        data = {"x": 1, "y": 2}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        out = json_file.get_all(path)
        # Should be a JSON string with both keys
        assert '"x": 1' in out and '"y": 2' in out
        assert out.strip().startswith("{")


def test_create_json_file():
    """
    test create json file
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        template = os.path.join(tmpdir, "template.json")
        target = os.path.join(tmpdir, "result.json")
        data = {"a": 10, "b": 20}
        with open(template, "w", encoding="utf-8") as f:
            json.dump(data, f)
        json_file.create_json_file(target, template)
        with open(target, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded == data


def test_update_invalid_json():
    """
    test update invalid json
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "broken.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write("not a json")
        with pytest.raises(json.JSONDecodeError):
            json_file.update(path, "foo", 1)


def test_get_all_invalid_json():
    """
    test get all invalid json
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "broken.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write("not a json")
        with pytest.raises(json.JSONDecodeError):
            json_file.get_all(path)


def test_get_value_invalid_json():
    """
    test get value invalid json
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "broken.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write("not a json")
        with pytest.raises(json.JSONDecodeError):
            json_file.get_value(path, "foo")


def test_create_json_file_invalid_template():
    """
    test create json file invalid template
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        template = os.path.join(tmpdir, "broken.json")
        target = os.path.join(tmpdir, "result.json")
        with open(template, "w", encoding="utf-8") as f:
            f.write("not a json")
        with pytest.raises(json.JSONDecodeError):
            json_file.create_json_file(target, template)
