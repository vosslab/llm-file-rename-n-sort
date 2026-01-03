#!/usr/bin/env python3
"""
Backend-agnostic response parsers.
"""

from __future__ import annotations

# Standard Library
from dataclasses import dataclass
import html
import re

# local repo modules

#============================================


class ParseError(RuntimeError):
	"""
	Raised when a model response does not match required tags.
	"""

	def __init__(self, message: str, raw_text: str = "") -> None:
		super().__init__(message)
		self.raw_text = raw_text


@dataclass(slots=True)
class RenameResult:
	new_name: str
	reason: str
	raw_text: str


@dataclass(slots=True)
class KeepResult:
	keep_original: bool
	reason: str
	raw_text: str


@dataclass(slots=True)
class SortResult:
	assignments: dict[str, str]
	raw_text: str


_CODE_FENCE_RE = re.compile(r"```[a-zA-Z0-9_+-]*\n(.*?)```", re.DOTALL)


def _strip_code_fences(text: str) -> str:
	if not text:
		return ""
	cleaned = text.strip()
	if "```" not in cleaned:
		return cleaned
	def _unwrap(match: re.Match) -> str:
		return match.group(1)
	cleaned = _CODE_FENCE_RE.sub(_unwrap, cleaned)
	return cleaned.strip()


def _coerce_response_body(text: str) -> str:
	cleaned = _strip_code_fences(text).strip().strip('"').strip("'")
	if "&lt;" in cleaned:
		unescaped = html.unescape(cleaned)
		if unescaped:
			cleaned = unescaped
	return cleaned


def _find_tag_values(text: str, tag: str) -> list[str]:
	pattern = re.compile(
		rf"<{tag}\b[^>]*>(.*?)</{tag}>",
		flags=re.IGNORECASE | re.DOTALL,
	)
	return [match.strip() for match in pattern.findall(text)]


_PROMPT_LEAK_PHRASES = (
	"previous reply did not match",
	"do not include",
	"return only",
	"schema",
	"tags below",
)


def _contains_prompt_leak(text: str) -> bool:
	if not text:
		return False
	lower = text.lower()
	return any(phrase in lower for phrase in _PROMPT_LEAK_PHRASES)


def parse_rename_response(text: str) -> RenameResult:
	response_body = _coerce_response_body(text)
	if not response_body:
		raise ParseError("Missing required tags in rename response.", text)
	new_names = _find_tag_values(response_body, "new_name")
	if not new_names:
		raise ParseError("Missing <new_name> in rename response.", text)
	if len(new_names) > 1:
		raise ParseError("Duplicate <new_name> tags in rename response.", text)
	reasons = _find_tag_values(response_body, "reason")
	if not reasons:
		raise ParseError("Missing <reason> in rename response.", text)
	if len(reasons) > 1:
		raise ParseError("Duplicate <reason> tags in rename response.", text)
	new_name = new_names[0]
	reason = reasons[0]
	if _contains_prompt_leak(reason):
		raise ParseError("Reason appears to echo prompt instructions.", text)
	return RenameResult(new_name=new_name, reason=reason, raw_text=text)

def parse_keep_response(
	text: str, original_stem: str, *, require_stem_reason: bool = False
) -> KeepResult:
	response_body = _coerce_response_body(text)
	if not response_body:
		raise ParseError("Missing required tags in keep response.", text)
	keep_values = _find_tag_values(response_body, "keep_original")
	if not keep_values:
		raise ParseError("Missing <keep_original> in keep response.", text)
	if len(keep_values) > 1:
		raise ParseError("Duplicate <keep_original> tags in keep response.", text)
	reason_values = _find_tag_values(response_body, "reason")
	if not reason_values:
		raise ParseError("Missing <reason> in keep response.", text)
	if len(reason_values) > 1:
		raise ParseError("Duplicate <reason> tags in keep response.", text)
	keep_text = keep_values[0].strip().lower()
	reason = reason_values[0]
	keep = keep_text.startswith("t") or keep_text == "1" or keep_text == "yes"
	reason = reason.replace('\\"', '"').replace("\\'", "'")
	if reason and _contains_prompt_leak(reason):
		raise ParseError("Reason appears to echo prompt instructions.", text)
	return KeepResult(keep_original=keep, reason=reason, raw_text=text)


def parse_sort_response(text: str, expected_paths: list[str]) -> SortResult:
	response_body = _coerce_response_body(text)
	if not response_body:
		raise ParseError("Missing required tags in sort response.", text)
	if len(expected_paths) != 1:
		raise ParseError("Sort responses only support a single file.", text)
	categories = _find_tag_values(response_body, "category")
	if not categories:
		raise ParseError("Missing <category> in sort response.", text)
	if len(categories) > 1:
		raise ParseError("Duplicate <category> tags in sort response.", text)
	category = categories[0].strip()
	return SortResult(assignments={expected_paths[0]: category}, raw_text=text)
