#!/usr/bin/env python3
"""Tests for audio metadata extraction."""

from pathlib import Path

from rename_n_sort.plugins.audio_plugin import AudioPlugin


def test_audio_plugin_extracts_basic_metadata(tmp_path: Path) -> None:
	path = tmp_path / "sample.mp3"
	path.write_bytes(b"ID3")
	plugin = AudioPlugin()
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == "audio"
	assert meta.extra.get("extension") == "mp3"
	assert meta.summary == "Audio file mp3"
