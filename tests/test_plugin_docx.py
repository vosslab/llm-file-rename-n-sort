#!/usr/bin/env python3
"""Tests for DOCX metadata extraction."""

from pathlib import Path

import pytest

from rename_n_sort.plugins import docx_plugin
from rename_n_sort.plugins.docx_plugin import DocxPlugin


def test_docx_plugin_extracts_summary() -> None:
	path = Path("tests/test_files/sample.docx")
	if not path.exists():
		pytest.skip("sample.docx not available")
	plugin = DocxPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "docx"
	assert meta.extra.get("extension") == "docx"
	if docx_plugin.docx:
		assert meta.summary
