#!/usr/bin/env python3
"""
Tests for max-depth scanning.
"""

from pathlib import Path

from rename_n_sort.config import AppConfig
from rename_n_sort.scanner import iter_files


def test_max_depth_limits(tmp_path: Path) -> None:
	root = tmp_path
	(root / "a.txt").write_text("root file", encoding="utf-8")
	sub = root / "sub"
	sub.mkdir()
	(sub / "b.txt").write_text("sub file", encoding="utf-8")
	nested = sub / "nested"
	nested.mkdir()
	(nested / "c.txt").write_text("deep file", encoding="utf-8")

	cfg = AppConfig(roots=[root], max_depth=1)
	files = iter_files(cfg)
	names = {path.name for path in files}

	assert "a.txt" in names
	assert "b.txt" in names
	assert "c.txt" not in names
