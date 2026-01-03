#!/usr/bin/env python3
"""
Backend-agnostic prompt builders.
"""

from __future__ import annotations

# Standard Library
from dataclasses import dataclass

# local repo modules
from .llm_utils import (
	ALLOWED_CATEGORIES,
	PROMPT_FILENAME_CHARS,
	_sanitize_prompt_list,
	_sanitize_prompt_text,
	_prompt_excerpt,
)

#============================================


@dataclass(slots=True)
class RenameRequest:
	metadata: dict
	current_name: str
	context: str | None = None


@dataclass(slots=True)
class KeepRequest:
	original_stem: str
	suggested_name: str
	extension: str | None
	features: dict[str, object]


@dataclass(slots=True)
class SortItem:
	path: str
	name: str
	ext: str
	description: str


@dataclass(slots=True)
class SortRequest:
	files: list[SortItem]
	context: str | None = None


RENAME_EXAMPLE_OUTPUT = (
	"<new_name>Invoice_20240115_Acorn_Supply.pdf</new_name>\n"
	"<reason>invoice with vendor and date</reason>"
)
KEEP_EXAMPLE_OUTPUT = (
	"<stem_action>normalize</stem_action>\n"
	"<reason>date and topic in stem are useful</reason>"
)
SORT_EXAMPLE_OUTPUT = "<category>Document</category>"


def build_rename_prompt(req: RenameRequest) -> str:
	lines: list[str] = []
	if req.context:
		lines.append(f"Context: {req.context}")
	lines.append(
		f"Rename this file concisely (max {PROMPT_FILENAME_CHARS} chars)."
	)
	title = _sanitize_prompt_text(req.metadata.get("title"), max_chars=200)
	keywords = _sanitize_prompt_list(req.metadata.get("keywords"))
	description = _sanitize_prompt_text(
		req.metadata.get("summary") or req.metadata.get("description"),
		max_chars=1200,
	)
	caption = _sanitize_prompt_text(req.metadata.get("caption"), max_chars=800)
	ocr_text = _sanitize_prompt_text(req.metadata.get("ocr_text"), max_chars=800)
	caption_note = _sanitize_prompt_text(req.metadata.get("caption_note"))
	filetype_hint = _sanitize_prompt_text(req.metadata.get("filetype_hint"))
	lines.append(f"current_name: {req.current_name}")
	if filetype_hint:
		lines.append(f"filetype: {filetype_hint}")
	if title:
		lines.append(f"title: {title}")
	if keywords:
		lines.append(f"keywords: {keywords}")
	if description:
		lines.append(f"description: {description}")
	if caption:
		lines.append(f"caption: {caption}")
	if ocr_text:
		lines.append(f"ocr_text: {ocr_text}")
	if caption_note:
		lines.append(f"caption_note: {caption_note}")
	lines.append(f"extension: {req.metadata.get('extension')}")
	lines.append("Return only the tags shown below.")
	lines.append("Example output:")
	lines.append(RENAME_EXAMPLE_OUTPUT)
	return "\n".join(lines)


def build_rename_prompt_minimal(req: RenameRequest) -> str:
	lines: list[str] = []
	if req.context:
		lines.append(f"Context: {req.context}")
	lines.append(
		f"Rename this file concisely (max {PROMPT_FILENAME_CHARS} chars)."
	)
	title = _sanitize_prompt_text(req.metadata.get("title"), max_chars=200)
	excerpt = _prompt_excerpt(req.metadata)
	filetype_hint = _sanitize_prompt_text(req.metadata.get("filetype_hint"))
	lines.append(f"current_name: {req.current_name}")
	if filetype_hint:
		lines.append(f"filetype: {filetype_hint}")
	if title:
		lines.append(f"title: {title}")
	if excerpt:
		lines.append(f"excerpt: {excerpt}")
	lines.append(f"extension: {req.metadata.get('extension')}")
	lines.append("Return only the tags shown below.")
	lines.append("Example output:")
	lines.append(RENAME_EXAMPLE_OUTPUT)
	return "\n".join(lines)


def build_keep_prompt(req: KeepRequest) -> str:
	lines: list[str] = []
	lines.append("Choose stem_action: drop | normalize | keep.")
	lines.append("Reason should mention what useful info is in the stem.")
	lines.append(f"original_stem: {req.original_stem}")
	lines.append(f"suggested_name: {req.suggested_name}")
	if req.extension:
		lines.append(f"extension: {req.extension}")
	lines.append("features:")
	for key, value in req.features.items():
		lines.append(f"- {key}: {value}")
	lines.append("Return only the tags shown below.")
	lines.append("Example output:")
	lines.append(KEEP_EXAMPLE_OUTPUT)
	return "\n".join(lines)


def build_sort_prompt(req: SortRequest) -> str:
	lines: list[str] = []
	if req.context:
		lines.append(f"Context: {req.context}")
	lines.append("Assign one allowed category to the file below.")
	lines.append("Allowed categories:")
	for cat in ALLOWED_CATEGORIES:
		lines.append(f"- {cat}")
	lines.append("File:")
	item = req.files[0]
	lines.append(
		f"path={item.path} | name={item.name} | ext={item.ext} | desc={item.description}"
	)
	lines.append("Return only the tags shown below.")
	lines.append("Example output:")
	lines.append(SORT_EXAMPLE_OUTPUT)
	return "\n".join(lines)


def build_format_fix_prompt(original_prompt: str, example_output: str) -> str:
	lines = [
		"Reply with tags only.",
		example_output,
	]
	return "\n".join(lines)
