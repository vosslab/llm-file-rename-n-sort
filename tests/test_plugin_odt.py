#!/usr/bin/env python3
"""Tests for ODT metadata extraction."""

from pathlib import Path

import pytest

from rename_n_sort.plugins import odt_plugin
from rename_n_sort.plugins.odt_plugin import OdtPlugin


def test_odt_plugin_extracts_summary() -> None:
	path = Path("tests/test_files/sample.odt")
	if not path.exists():
		pytest.skip("sample.odt not available")
	plugin = OdtPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "odt"
	assert meta.extra.get("extension") == "odt"
	if odt_plugin.load and odt_plugin.text and odt_plugin.teletype:
		assert meta.summary
