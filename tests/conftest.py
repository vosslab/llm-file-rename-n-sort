"""
Pytest config to ensure local package imports work without installation.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _add_repo_root_to_path() -> None:
	"""
	Insert the repo root into sys.path for local imports.
	"""
	repo_root = Path(__file__).resolve().parent.parent
	repo_root_str = str(repo_root)
	if repo_root_str not in sys.path:
		sys.path.insert(0, repo_root_str)


_add_repo_root_to_path()

from rename_n_sort.llm import BaseClassLLM  # noqa: E402


class StubLLM(BaseClassLLM):
	"""
	Test-only stub LLM for organizer/unit tests.
	"""

	def __init__(self) -> None:
		self.model = "stub"

	def suggest_name_and_category(self, metadata: dict, current_name: str) -> tuple[str, str]:
		return ("stub_name", "Other")

	def rename_file(self, metadata: dict, current_name: str) -> str:
		return "stub_name"

	def rename_file_explain(self, metadata: dict, current_name: str) -> tuple[str, str]:
		return ("stub_name", "stub reason")

	def rename_with_keep(self, metadata: dict, current_name: str) -> tuple[str, bool]:
		return ("stub_name", False)

	def should_keep_original_explain(
		self, metadata: dict, current_name: str, new_name: str
	) -> tuple[bool, str]:
		return (False, "stub keep")

	def assign_categories(self, summaries: list[dict]) -> dict[int, str]:
		return {0: "Document"}

	def assign_categories_explain(
		self, summaries: list[dict]
	) -> tuple[dict[int, str], dict[int, str]]:
		return ({0: "Document"}, {0: "stub category"})
