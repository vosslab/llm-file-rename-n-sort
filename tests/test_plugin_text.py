#!/usr/bin/env python3
"""Tests for text document metadata extraction."""

from pathlib import Path

import pytest

from rename_n_sort.plugins.text import TextDocumentPlugin


def test_text_plugin_reads_sample_txt() -> None:
	path = Path("tests/test_files/sample.txt")
	if not path.exists():
		pytest.skip("sample.txt not available")
	plugin = TextDocumentPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "text"
	assert meta.extra.get("extension") == "txt"
	assert meta.summary
