# -*- coding: utf-8 -*-
"""
Unit tests for files/__init__.py
"""

import os
import json
import tempfile
from files import write_to_file, write_list_dict_to_file


def test_write_to_file_appends():
    """Test that write_to_file appends content to a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "testfile.txt")
        write_to_file(path, "hello\n")
        write_to_file(path, "world\n")
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        assert lines == ["hello\n", "world\n"]


def test_write_list_dict_to_file():
    """Test that write_list_dict_to_file writes a list of dicts as JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        data = [{"a": 1}, {"b": 2}]
        write_list_dict_to_file(path, data)
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded == data


def test_write_to_file_unicode():
    """Test that write_to_file handles unicode content."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "utf8.txt")
        content = "你好，世界\n"
        write_to_file(path, content)
        with open(path, "r", encoding="utf-8") as f:
            assert f.read() == content


def test_write_list_dict_to_file_empty():
    """Test writing an empty list."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "empty.json")
        write_list_dict_to_file(path, [])
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded == []
