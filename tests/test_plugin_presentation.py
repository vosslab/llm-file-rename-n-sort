#!/usr/bin/env python3
"""Tests for presentation metadata extraction."""

from pathlib import Path

import pytest

from rename_n_sort.plugins.presentation_plugin import PresentationPlugin


@pytest.mark.parametrize(
	"filename",
	[
		"sample.ppt",
		"sample.pptx",
		"sample.odp",
	],
)
def test_presentation_plugin_handles_samples(filename: str) -> None:
	path = Path("tests/test_files") / filename
	if not path.exists():
		pytest.skip(f"{filename} not available")
	plugin = PresentationPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "presentation"
	assert meta.extra.get("extension") == path.suffix.lstrip(".")
	assert meta.summary
