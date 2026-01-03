#!/usr/bin/env python3
"""
Tests for CLI LLM backend selection.
"""

from rename_n_sort.cli import build_llm
from rename_n_sort.config import AppConfig
from rename_n_sort.llm import MacOSLocalLLM, OllamaChatLLM


def test_backend_macos_default():
	cfg = AppConfig(roots=[])
	cfg.llm_backend = "macos"
	llm = build_llm(cfg)
	assert isinstance(llm, MacOSLocalLLM)


def test_backend_ollama_unavailable_falls_back(monkeypatch):
	import rename_n_sort.cli as cli

	monkeypatch.setattr(cli, "_ollama_available", lambda _url: False)
	cfg = AppConfig(roots=[])
	cfg.llm_backend = "ollama"
	llm = build_llm(cfg)
	assert isinstance(llm, MacOSLocalLLM)


def test_backend_ollama_available_uses_ollama(monkeypatch):
	import rename_n_sort.cli as cli

	monkeypatch.setattr(cli, "_ollama_available", lambda _url: True)
	cfg = AppConfig(roots=[])
	cfg.llm_backend = "ollama"
	llm = build_llm(cfg)
	assert isinstance(llm, OllamaChatLLM)
