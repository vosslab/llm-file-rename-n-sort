#!/usr/bin/env python3
"""
Repo-root runner for rename_n_sort.

Examples:
	python run_file_cleanup.py --paths ~/Downloads --max-files 20
	python run_file_cleanup.py --paths ~/Downloads --max-files 20 --apply
"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
	"""
	Run the CLI entrypoint with repo-root import behavior.
	"""
	repo_root = Path(__file__).resolve().parent
	if str(repo_root) not in sys.path:
		sys.path.insert(0, str(repo_root))

	from rename_n_sort.cli import main as cli_main

	cli_main()


if __name__ == "__main__":
	main()

