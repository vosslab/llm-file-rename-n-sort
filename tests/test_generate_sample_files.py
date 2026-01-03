#!/usr/bin/env python3
"""
Tests for sample file generator.
"""

from pathlib import Path
import subprocess
import sys


def test_generate_sample_files(tmp_path: Path):
	script = Path("tests/generate_sample_files.py")
	output_dir = tmp_path / "samples"
	subprocess.run(
		[sys.executable, str(script), "--output", str(output_dir)],
		check=True,
	)
	assert (output_dir).exists()
	assert any(output_dir.iterdir())
	extensions = {path.suffix for path in output_dir.iterdir()}
	assert ".docx" in extensions
	assert ".pdf" in extensions
