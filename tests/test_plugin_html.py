#!/usr/bin/env python3
"""Tests for HTML metadata extraction."""

from pathlib import Path

from rename_n_sort.plugins import html_plugin
from rename_n_sort.plugins.html_plugin import HtmlPlugin


def test_html_plugin_extracts_text_and_title(tmp_path: Path) -> None:
	path = tmp_path / "sample.html"
	path.write_text(
		"<html><head><title>Sample</title></head><body>Hello World</body></html>",
		encoding="utf-8",
	)
	plugin = HtmlPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "html"
	assert meta.extra.get("extension") == "html"
	if html_plugin.BeautifulSoup:
		assert meta.summary and "Hello" in meta.summary
		assert meta.title == "Sample"
