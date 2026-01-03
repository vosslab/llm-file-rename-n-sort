#!/usr/bin/env python3
"""Filename normalization and sanitization tests."""

from rename_n_sort.config import AppConfig
from rename_n_sort.llm_utils import MAX_FILENAME_CHARS, sanitize_filename
from rename_n_sort.organizer import Organizer
from conftest import StubLLM


def test_sanitize_filename_replaces_invalid_chars():
	assert sanitize_filename("My File 2025.pdf") == "My-File-2025.pdf"
	assert sanitize_filename("bad/evil:name?.txt") == "bad-evil-name-.txt"


def test_sanitize_filename_keeps_safe_names():
	assert sanitize_filename("Report_2025-01-03.pdf") == "Report_2025-01-03.pdf"


def test_sanitize_filename_fallback_to_file():
	assert sanitize_filename("___") == "file"


def test_sanitize_filename_truncates_long_names():
	long_name = "a" * 200
	result = sanitize_filename(long_name)
	assert len(result) == MAX_FILENAME_CHARS


def test_normalize_new_name_dedupes_extension():
	org = Organizer(AppConfig(roots=[]), llm=StubLLM())
	assert org._normalize_new_name("report.pdf", "report.pdf.pdf") == "report.pdf"


def test_normalize_new_name_removes_current_name_token():
	org = Organizer(AppConfig(roots=[]), llm=StubLLM())
	assert org._normalize_new_name("report.pdf", "report-current_name.pdf") == "report"
