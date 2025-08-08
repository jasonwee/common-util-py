# -*- coding: utf-8 -*-
"""
Unit tests for httpclient/__init__.py
"""
import pytest
from httpclient import get_param_from_url, get_param_from_query_string

def test_get_param_from_url_single():
    url = "https://example.com/page?foo=bar&baz=qux"
    assert get_param_from_url(url, "foo") == ["bar"]
    assert get_param_from_url(url, "baz") == ["qux"]


def test_get_param_from_url_multiple():
    url = "https://example.com/page?foo=bar&foo=baz"
    assert get_param_from_url(url, "foo") == ["bar", "baz"]


def test_get_param_from_query_string_single():
    qs = "a=1&b=2"
    assert get_param_from_query_string(qs, "a") == ["1"]
    assert get_param_from_query_string(qs, "b") == ["2"]


def test_get_param_from_query_string_multiple():
    qs = "foo=bar&foo=baz"
    assert get_param_from_query_string(qs, "foo") == ["bar", "baz"]


def test_key_error_for_missing_param_url():
    url = "https://example.com/page?a=1"
    with pytest.raises(KeyError):
        get_param_from_url(url, "notfound")


def test_key_error_for_missing_param_query_string():
    qs = "a=1"
    with pytest.raises(KeyError):
        get_param_from_query_string(qs, "notfound")
