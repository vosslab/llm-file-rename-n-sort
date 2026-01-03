#!/usr/bin/env python3
"""Tests for video metadata extraction."""

from pathlib import Path

from rename_n_sort.plugins.video_plugin import VideoPlugin


def test_video_plugin_extracts_basic_metadata(tmp_path: Path) -> None:
	path = tmp_path / "sample.mp4"
	path.write_bytes(b"\x00\x00\x00\x18ftyp")
	plugin = VideoPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "video"
	assert meta.extra.get("extension") == "mp4"
	assert meta.summary == "Video file mp4"
