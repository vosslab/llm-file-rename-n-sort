#!/usr/bin/env python3
"""Tests for PDF metadata extraction."""

from pathlib import Path

from rename_n_sort.plugins.pdf import PDFPlugin


def test_pdf_plugin_extracts_basic_metadata(tmp_path: Path) -> None:
	path = tmp_path / "sample.pdf"
	path.write_bytes(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
	plugin = PDFPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "pdf"
	assert meta.extra.get("extension") == "pdf"
