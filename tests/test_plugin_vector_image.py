#!/usr/bin/env python3
"""Tests for vector image metadata extraction."""

from pathlib import Path

from rename_n_sort.plugins.vector_image_plugin import VectorImagePlugin


def test_vector_image_plugin_reads_svg_text(tmp_path: Path) -> None:
	path = tmp_path / "sample.svg"
	path.write_text(
		"<svg xmlns=\"http://www.w3.org/2000/svg\"><text>SAMPLE</text></svg>",
		encoding="utf-8",
	)
	plugin = VectorImagePlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "vector_image"
	assert meta.extra.get("extension") == "svg"
	assert meta.summary and "Vector image" in meta.summary
