#!/usr/bin/env python3
"""Tests for CSV metadata extraction."""

from pathlib import Path

from rename_n_sort.plugins.csv_plugin import CSVPlugin


def test_csv_plugin_extracts_preview(tmp_path: Path) -> None:
	path = tmp_path / "data.csv"
	path.write_text("col1,col2\n1,2\n3,4\n", encoding="utf-8")
	plugin = CSVPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "csv"
	assert meta.extra.get("extension") == "csv"
	assert meta.summary and "col1" in meta.summary
