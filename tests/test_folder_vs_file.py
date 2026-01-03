#!/usr/bin/env python3
"""Ensure folders are skipped and files are processed."""

from pathlib import Path

from rename_n_sort.config import AppConfig
from rename_n_sort.organizer import Organizer
from rename_n_sort.scanner import iter_files
from conftest import StubLLM


def test_scanner_skips_directories(tmp_path: Path) -> None:
	file_path = tmp_path / "sample.txt"
	dir_path = tmp_path / "Folder"
	dir_path.mkdir()
	file_path.write_text("hello", encoding="utf-8")
	config = AppConfig(roots=[tmp_path], randomize=False)
	paths = iter_files(config)
	assert dir_path not in paths
	assert file_path in paths


def test_organizer_skips_directory_in_input(tmp_path: Path) -> None:
	file_path = tmp_path / "sample.txt"
	dir_path = tmp_path / "Folder"
	dir_path.mkdir()
	file_path.write_text("hello", encoding="utf-8")
	config = AppConfig(roots=[tmp_path], randomize=False)
	org = Organizer(config, llm=StubLLM())
	plans = org.plan(files=[dir_path, file_path])
	assert len(plans) == 1
	assert plans[0].source == file_path
