#!/usr/bin/env python3
"""Tests for legacy document metadata extraction."""

from pathlib import Path

import pytest

from rename_n_sort.plugins.document_plugin import DocumentPlugin


@pytest.mark.parametrize(
	"filename",
	[
		"sample.doc",
		"sample.docx",
		"sample.odt",
	],
)
def test_document_plugin_handles_samples(filename: str) -> None:
	path = Path("tests/test_files") / filename
	if not path.exists():
		pytest.skip(f"{filename} not available")
	plugin = DocumentPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "document"
	assert meta.extra.get("extension") == path.suffix.lstrip(".")
