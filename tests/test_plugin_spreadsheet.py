#!/usr/bin/env python3
"""Tests for spreadsheet metadata extraction."""

from pathlib import Path

import pytest

from rename_n_sort.plugins.spreadsheet_plugin import SpreadsheetPlugin


@pytest.mark.parametrize(
	"filename,delimiter",
	[
		("sheet.csv", ","),
		("sheet.tsv", "\t"),
	],
)
def test_spreadsheet_plugin_reads_delimited_preview(
	tmp_path: Path, filename: str, delimiter: str
) -> None:
	path = tmp_path / filename
	path.write_text(f"A{delimiter}B\n1{delimiter}2\n3{delimiter}4\n", encoding="utf-8")
	plugin = SpreadsheetPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "spreadsheet"
	assert meta.extra.get("extension") == path.suffix.lstrip(".")
	assert meta.summary and "A" in meta.summary
