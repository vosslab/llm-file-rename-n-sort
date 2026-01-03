#!/usr/bin/env python3
"""
Tests for EPUB metadata extraction.
"""

from pathlib import Path

from rename_n_sort.plugins import build_registry


def test_epub_metadata_extraction():
	path = Path("tests/test_files/sample.epub")
	if not path.exists():
		return
	registry = build_registry()
	plugin = registry.for_path(path)
	meta = plugin.extract_metadata(path)
	assert plugin.name == "epub"
	assert meta.summary
	assert meta.title
