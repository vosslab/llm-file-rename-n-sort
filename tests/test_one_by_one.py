#!/usr/bin/env python3
"""
Tests for one-by-one organizer mode.
"""

from pathlib import Path

from rename_n_sort.config import AppConfig
from rename_n_sort.organizer import Organizer
from conftest import StubLLM


def test_one_by_one_assigns_category_and_target(tmp_path: Path):
	source = tmp_path / "example.txt"
	source.write_text("hello world")
	target_root = tmp_path / "out"

	cfg = AppConfig(roots=[], target_root=target_root, dry_run=True)
	org = Organizer(cfg, llm=StubLLM())

	plans = org.process_one_by_one([source])
	assert len(plans) == 1
	assert plans[0].category == "Document"
	assert str(plans[0].target).startswith(str(target_root))
