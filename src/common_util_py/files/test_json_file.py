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
    Test update() and get_value() integration.

    Verifies that update() can add and modify key-value pairs,
    and get_value() correctly retrieves the updated values.
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
    Test that get_value returns 0 when the specified key is not found in the JSON file.

    This test creates a JSON file with a known key-value pair and verifies that
    get_value() returns 0 when attempting to retrieve a non-existent key,
    demonstrating the default behavior for missing keys.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "data.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"a": 1}, f)
        assert json_file.get_value(path, "notfound") == 0


def test_get_all():
    """
    Test that get_all returns the complete JSON content as a formatted string.

    This test creates a JSON file with multiple key-value pairs and verifies that
    get_all() returns a JSON string containing all the data, properly formatted
    with indentation as specified in the implementation.
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
    Test that create_json_file copies the template content to the target file.

    This test creates a template JSON file with sample data and verifies that
    create_json_file() successfully creates a new file with identical content,
    ensuring the template copying functionality works correctly.
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
    Test that get_all raises ValueError when the JSON file contains invalid JSON.

    This test creates a file with invalid JSON content and verifies that
    get_all() raises a ValueError instead of attempting to parse the malformed data.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "broken.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write("not a json")
        with pytest.raises(ValueError):
            json_file.get_all(path)


def test_get_value_invalid_json():
    """
    Test that get_value raises JSONDecodeError when given a file with invalid JSON.

    This test creates a file with invalid JSON content and verifies that
    get_value() raises a JSONDecodeError instead of attempting to parse
    the malformed data.
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
