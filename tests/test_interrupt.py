from BB_auto_framework.plugins.recon.recon_utils import prompt_user_on_interrupt
import builtins
import pytest  # noqa: F401 - used for fixtures (monkeypatch)

def test_prompt_continue(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "C")
    assert prompt_user_on_interrupt() == "C"

def test_prompt_skip(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "S")
    assert prompt_user_on_interrupt() == "S"

def test_prompt_exit(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "E")
    assert prompt_user_on_interrupt() == "E"
