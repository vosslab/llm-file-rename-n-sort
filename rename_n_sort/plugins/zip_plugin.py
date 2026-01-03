#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import zipfile

from .base import FileMetadata, FileMetadataPlugin
from .mdls_utils import mdls_field


class ZipPlugin(FileMetadataPlugin):
	"""
	Plugin for ZIP archives (metadata only).
	"""

	name = "zip"
	filetype_hint = "ZIP archive"
	supported_suffixes: set[str] = {"zip"}

	#============================================
	def supports(self, path: Path) -> bool:
		return path.suffix.lower().lstrip(".") in self.supported_suffixes

	#============================================
	def extract_metadata(self, path: Path) -> FileMetadata:
		meta = FileMetadata(path=path, plugin_name=self.name)
		meta.extra["size_bytes"] = path.stat().st_size
		meta.extra["extension"] = path.suffix.lstrip(".")
		title = mdls_field(path, "kMDItemTitle")
		if title:
			meta.title = title
		file_count, top_level = self._read_zip_index(path)
		if file_count is not None:
			meta.extra["archive_file_count"] = file_count
		if top_level:
			meta.extra["archive_top_level"] = top_level
		meta.summary = self._build_summary(file_count, top_level)
		return meta

	#============================================
	def _read_zip_index(self, path: Path) -> tuple[int | None, list[str]]:
		try:
			with zipfile.ZipFile(path, "r") as archive:
				file_count = 0
				top_level: set[str] = set()
				for info in archive.infolist():
					name = info.filename
					if not name:
						continue
					parts = [part for part in name.split("/") if part]
					if parts:
						top_level.add(parts[0])
					if not name.endswith("/"):
						file_count += 1
				return file_count, sorted(top_level)
		except Exception:
			return None, []

	#============================================
	def _build_summary(self, file_count: int | None, top_level: list[str]) -> str:
		count_text = "ZIP archive"
		if file_count is not None:
			count_text = f"ZIP archive with {file_count} files"
		if not top_level:
			return count_text
		shown = ", ".join(top_level[:10])
		if len(top_level) > 10:
			shown = f"{shown}, ..."
		return f"{count_text}. Top-level: {shown}."
