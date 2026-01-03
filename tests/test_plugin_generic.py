#!/usr/bin/env python3
"""Tests for generic metadata extraction."""

from pathlib import Path

from rename_n_sort.plugins.generic import GenericPlugin


def test_generic_plugin_extracts_basic_metadata(tmp_path: Path) -> None:
	path = tmp_path / "sample.unknown"
	path.write_text("hello", encoding="utf-8")
	plugin = GenericPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "generic"
	assert meta.extra.get("extension") == "unknown"
