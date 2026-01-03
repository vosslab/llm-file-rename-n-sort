#!/usr/bin/env python3
"""
Extraction checks for repo test files.
"""

from pathlib import Path

import pytest

from rename_n_sort.plugins import build_registry


ROOT = Path("tests/test_files")
SAMPLE_EXT_PATHS: dict[str, Path] = {}
if ROOT.exists():
	for path in sorted(ROOT.iterdir()):
		if not path.is_file():
			continue
		ext = path.suffix.lstrip(".").lower()
		if ext and ext not in SAMPLE_EXT_PATHS:
			SAMPLE_EXT_PATHS[ext] = path


@pytest.mark.parametrize(
	"ext,path",
	sorted(SAMPLE_EXT_PATHS.items()),
)
def test_extract_test_files_metadata(ext: str, path: Path):
	registry = build_registry()
	plugin = registry.for_path(path)
	if plugin.name == "image":
		plugin._extract_ocr_text = lambda _path: None
		plugin._try_caption = lambda _path: None
	meta = plugin.extract_metadata(path)
	assert meta.plugin_name == plugin.name
	assert meta.extra.get("extension") == ext


EXPECTED_PLUGINS = {
	"doc": "document",
	"docx": "docx",
	"epub": "epub",
	"odt": "odt",
	"odp": "presentation",
	"ppt": "presentation",
	"pptx": "presentation",
	"png": "image",
	"jpg": "image",
	"gif": "image",
	"bmp": "image",
	"tiff": "image",
	"txt": "document",
}
REQUIRED_SUMMARY_EXTS = {"docx", "epub", "odt", "pptx", "odp", "txt"}
CONTENT_PARAMS = [
	(ext, SAMPLE_EXT_PATHS[ext])
	for ext in EXPECTED_PLUGINS
	if ext in SAMPLE_EXT_PATHS
]


@pytest.mark.parametrize("ext,path", CONTENT_PARAMS)
def test_extract_test_files_content_expectations(ext: str, path: Path):
	registry = build_registry()
	plugin = registry.for_path(path)
	if plugin.name == "image":
		plugin._extract_ocr_text = lambda _path: None
		plugin._try_caption = lambda _path: None
	meta = plugin.extract_metadata(path)
	assert plugin.name == EXPECTED_PLUGINS[ext]
	if ext in REQUIRED_SUMMARY_EXTS:
		assert meta.summary
