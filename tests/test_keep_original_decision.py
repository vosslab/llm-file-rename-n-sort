#!/usr/bin/env python3
"""Tests for keep_original handling."""

from rename_n_sort.llm import OllamaChatLLM
from rename_n_sort.organizer import Organizer
from rename_n_sort.config import AppConfig
from rename_n_sort.llm import DummyLLM


def test_parse_rename_with_keep_true():
	llm = OllamaChatLLM(model="test")
	response = "keep_original: true"
	keep = llm._parse_keep_response(response)
	assert keep is True


def test_parse_rename_with_keep_missing_defaults_true():
	llm = OllamaChatLLM(model="test")
	response = "note: missing flag"
	keep = llm._parse_keep_response(response)
	assert keep is True


def test_keep_original_combines_original_stem():
	org = Organizer(AppConfig(roots=[]), llm=DummyLLM(model="dummy"))
	final = org._normalize_new_name("orig.txt", "orig_NewName.txt")
	assert "orig" in final.lower()
