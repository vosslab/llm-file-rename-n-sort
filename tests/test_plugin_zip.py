#!/usr/bin/env python3
"""Tests for ZIP archive metadata extraction."""

from pathlib import Path
from zipfile import ZipFile

from rename_n_sort.plugins.zip_plugin import ZipPlugin


def test_zip_plugin_top_level_entries(tmp_path: Path) -> None:
	zip_path = tmp_path / "sample.zip"
	with ZipFile(zip_path, "w") as archive:
		archive.writestr("README.txt", "hello")
		archive.writestr("src/main.py", "print('hi')")
		archive.writestr("src/utils/helpers.py", "")
		archive.writestr("docs/guide.md", "# guide")
		archive.writestr("nested/dir/thing.txt", "x")
	plugin = ZipPlugin()
	meta = plugin.extract_metadata(zip_path)
	top_level = meta.extra.get("archive_top_level")
	assert set(top_level) == {"README.txt", "src", "docs", "nested"}
	assert meta.extra.get("archive_file_count") == 5
	assert meta.summary and "Top-level" in meta.summary
