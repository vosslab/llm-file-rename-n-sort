#!/usr/bin/env python3
from __future__ import annotations

# Standard Library
from pathlib import Path

# PIP3 modules
try:
	from bs4 import BeautifulSoup
except Exception:
	BeautifulSoup = None

# local repo modules
from .base import FileMetadata, FileMetadataPlugin

#============================================


class HtmlPlugin(FileMetadataPlugin):
	"""
	Plugin for HTML documents.
	"""

	name = "html"
	supported_suffixes: set[str] = {"html", "htm"}

	#============================================
	def supports(self, path: Path) -> bool:
		return path.suffix.lower().lstrip(".") in self.supported_suffixes

	#============================================
	def extract_metadata(self, path: Path) -> FileMetadata:
		meta = FileMetadata(path=path, plugin_name=self.name)
		meta.extra["size_bytes"] = path.stat().st_size
		meta.extra["extension"] = path.suffix.lstrip(".")
		text, title = self._read_html_text(path)
		if title:
			meta.title = title
		if text:
			meta.summary = text
		return meta

	#============================================
	def _read_html_text(self, path: Path) -> tuple[str | None, str | None]:
		if not BeautifulSoup:
			return (None, None)
		try:
			raw = path.read_text(encoding="utf-8", errors="ignore")
		except Exception:
			return (None, None)
		try:
			soup = BeautifulSoup(raw, "html.parser")
		except Exception:
			return (None, None)
		for tag in soup(["script", "style", "noscript"]):
			tag.decompose()
		title = None
		if soup.title and soup.title.string:
			title = " ".join(soup.title.string.split())
		text = soup.get_text(separator=" ")
		flattened = " ".join(text.split())
		if not flattened:
			return (None, title)
		return (flattened[:800], title)
