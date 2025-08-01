# -*- coding: utf-8 -*-
"""
Unit tests for timeout.py
"""

from unittest import mock
import sys
import subprocess
import signal

import pytest

from cli import timeout


def test_timeout_exception():
    """Test that TimeoutException is raised by the handler."""
    with pytest.raises(timeout.TimeoutException):
        timeout.timeout_handler(signal.SIGALRM, None)


def test_cuda_exception():
    """Test CUDAException can be raised and caught."""
    with pytest.raises(timeout.CUDAException):
        raise timeout.CUDAException("CUDA error detected")


def test_env_timeout(monkeypatch):
    """Test TIMEOUT_NO_ACTIVITY_SECONDS env var parsing."""
    monkeypatch.setenv("TIMEOUT_NO_ACTIVITY_SECONDS", "123")
    import importlib
    from cli import timeout as t_reload

    importlib.reload(t_reload)
    assert t_reload.TIMEOUT_NO_ACTIVITY_SECONDS == 123


def test_execute_keyboard_interrupt(monkeypatch):
    """Test execute handles KeyboardInterrupt and exits loop."""

    class DummyProc:
        """Patch subprocess.Popen to simulate a process"""

        def __init__(self):
            self.stdout = mock.Mock()
            self.stdout.readline = mock.Mock(side_effect=KeyboardInterrupt)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

        def send_signal(self, sig):
            """Send signal to process"""

        def wait(self, timeout=None):
            """Wait for process to finish"""

    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: DummyProc())
    # Patch signal.signal and signal.alarm to do nothing
    monkeypatch.setattr(signal, "signal", lambda *a, **k: None)
    monkeypatch.setattr(signal, "alarm", lambda *a, **k: None)
    # Should exit cleanly
    timeout.execute([sys.executable, "-c", "print('ok')"])


'''
def test_execute_timeout(monkeypatch):
    """Test execute handles TimeoutException and restarts once."""
    class DummyProc:
        def __init__(self):
            self.stdout = mock.Mock()
            self.stdout.readline = mock.Mock(side_effect=["line", "", TimeoutError])
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): return False
        def send_signal(self, sig): pass
        def wait(self, timeout=None): pass

    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: DummyProc())
    monkeypatch.setattr(signal, "signal", lambda *a, **k: None)
    monkeypatch.setattr(signal, "alarm", lambda *a, **k: None)

    # Add a counter to break the loop after one restart
    call_count = {"count": 0}
    orig_execute = timeout.execute

    def limited_execute(cmd):
        if call_count["count"] > 0:
            return  # Exit after first restart
        call_count["count"] += 1
        return orig_execute(cmd)

    with mock.patch("cli.timeout.logging") as mock_log:
        monkeypatch.setattr(timeout, "execute", limited_execute)
        timeout.execute([sys.executable, "-c", "print('ok')"])
        assert mock_log.error.called
'''
