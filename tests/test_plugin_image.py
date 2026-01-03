#!/usr/bin/env python3
"""Tests for image metadata extraction."""

from pathlib import Path

import pytest

from rename_n_sort.plugins.image_plugin import ImagePlugin


@pytest.mark.parametrize(
	"filename",
	[
		"sample_image.jpg",
		"sample_image.png",
		"sample_image.gif",
		"sample_image.bmp",
		"sample_image.tiff",
		"sample_ocr.png",
	],
)
def test_image_plugin_extracts_basic_metadata(filename: str) -> None:
	path = Path("tests/test_files") / filename
	if not path.exists():
		pytest.skip(f"{filename} not available")
	plugin = ImagePlugin()
	plugin._extract_ocr_text = lambda _path: None
	plugin._try_caption = lambda _path: None
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "image"
	ext = path.suffix.lstrip(".")
	assert meta.extra.get("extension") == ext
	assert meta.summary == f"Image file {ext}"
