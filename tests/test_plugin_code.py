#!/usr/bin/env python3
"""Tests for code metadata extraction."""

from pathlib import Path

from rename_n_sort.plugins.code_plugin import CodePlugin


def test_code_plugin_extracts_preview(tmp_path: Path) -> None:
	path = tmp_path / "script.py"
	path.write_text("print('hi')\n# comment\n", encoding="utf-8")
	plugin = CodePlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "code"
	assert meta.extra.get("extension") == "py"
	assert meta.summary and "print" in meta.summary
