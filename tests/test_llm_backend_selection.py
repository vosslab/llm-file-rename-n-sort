#!/usr/bin/env python3
"""
Tests for CLI LLM backend selection.
"""

from rename_n_sort.cli import build_llm
from rename_n_sort.config import AppConfig
from rename_n_sort.llm import AppleLLM, OllamaChatLLM


def test_backend_macos_default(monkeypatch):
	cfg = AppConfig(roots=[])
	cfg.llm_backend = "macos"
	import rename_n_sort.cli as cli
	monkeypatch.setattr(cli, "apple_models_available", lambda: True)
	llm = build_llm(cfg)
	assert isinstance(llm, AppleLLM)


def test_backend_macos_falls_back_to_ollama(monkeypatch):
	import rename_n_sort.cli as cli
	monkeypatch.setattr(cli, "apple_models_available", lambda: False)
	monkeypatch.setattr(cli, "_ollama_available", lambda _url: True)
	cfg = AppConfig(roots=[])
	cfg.llm_backend = "macos"
	llm = build_llm(cfg)
	assert isinstance(llm, OllamaChatLLM)


def test_backend_ollama_available_uses_ollama(monkeypatch):
	import rename_n_sort.cli as cli

	monkeypatch.setattr(cli, "apple_models_available", lambda: True)
	monkeypatch.setattr(cli, "_ollama_available", lambda _url: True)
	cfg = AppConfig(roots=[])
	cfg.llm_backend = "ollama"
	llm = build_llm(cfg)
	assert isinstance(llm, OllamaChatLLM)


def test_backend_ollama_unavailable_raises(monkeypatch):
	import pytest
	import rename_n_sort.cli as cli

	monkeypatch.setattr(cli, "_ollama_available", lambda _url: False)
	cfg = AppConfig(roots=[])
	cfg.llm_backend = "ollama"
	with pytest.raises(RuntimeError):
		build_llm(cfg)
