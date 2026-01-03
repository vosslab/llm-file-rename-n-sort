#!/usr/bin/env python3
from __future__ import annotations

from html import unescape
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

from .base import FileMetadata, FileMetadataPlugin
from .mdls_utils import mdls_field

#============================================


class EpubPlugin(FileMetadataPlugin):
	"""
	Plugin for .epub ebooks.
	"""

	name = "epub"
	filetype_hint = "Ebook"
	supported_suffixes: set[str] = {"epub"}

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
		metadata = self._read_epub_metadata(path)
		if metadata:
			epub_title, creator, subjects, description = metadata
			if epub_title and not meta.title:
				meta.title = epub_title
			if creator:
				meta.keywords.append(creator)
			if subjects:
				meta.keywords.extend(subjects)
			summary = self._build_summary(epub_title, creator, description, subjects)
			if summary:
				meta.summary = summary
		return meta

	#============================================
	def _read_epub_metadata(
		self, path: Path
	) -> tuple[str | None, str | None, list[str], str | None] | None:
		try:
			with zipfile.ZipFile(path, "r") as archive:
				container_xml = archive.read("META-INF/container.xml")
				rootfile = self._find_rootfile(container_xml)
				if not rootfile:
					return None
				opf_xml = archive.read(rootfile)
		except Exception:
			return None
		return self._parse_opf(opf_xml)

	#============================================
	def _find_rootfile(self, xml_blob: bytes) -> str | None:
		try:
			root = ET.fromstring(xml_blob)
		except Exception:
			return None
		for element in root.iter():
			if self._strip_ns(element.tag) == "rootfile":
				full_path = element.attrib.get("full-path")
				if full_path:
					return full_path
		return None

	#============================================
	def _parse_opf(
		self, xml_blob: bytes
	) -> tuple[str | None, str | None, list[str], str | None] | None:
		try:
			root = ET.fromstring(xml_blob)
		except Exception:
			return None
		metadata_node = None
		for element in root.iter():
			if self._strip_ns(element.tag) == "metadata":
				metadata_node = element
				break
		if metadata_node is None:
			metadata_node = root
		title = None
		creator = None
		description = None
		subjects: list[str] = []
		for element in metadata_node.iter():
			tag = self._strip_ns(element.tag)
			if tag == "title" and not title:
				title = self._clean_text(element.text)
			elif tag == "creator" and not creator:
				creator = self._clean_text(element.text)
			elif tag == "subject":
				subject = self._clean_text(element.text)
				if subject:
					subjects.append(subject)
			elif tag == "description" and not description:
				description = self._clean_text(element.text)
			elif tag == "meta":
				name = (element.attrib.get("name") or element.attrib.get("property") or "").lower()
				content = self._clean_text(element.attrib.get("content") or element.text)
				if not content:
					continue
				if name.endswith("title") and not title:
					title = content
				elif name.endswith("creator") and not creator:
					creator = content
				elif name.endswith("description") and not description:
					description = content
				elif name.endswith("subject"):
					subjects.append(content)
		return title, creator, subjects, description

	#============================================
	def _build_summary(
		self,
		title: str | None,
		creator: str | None,
		description: str | None,
		subjects: list[str],
	) -> str | None:
		if description:
			return description[:800]
		parts: list[str] = []
		if title:
			parts.append(title)
		if creator:
			parts.append(f"by {creator}")
		if subjects:
			shown = ", ".join(subjects[:5])
			parts.append(f"Topics: {shown}")
		if not parts:
			return "EPUB ebook"
		return f"EPUB ebook: {' '.join(parts)}"

	#============================================
	def _strip_ns(self, tag: str) -> str:
		if "}" in tag:
			return tag.split("}", 1)[1]
		return tag

	#============================================
	def _clean_text(self, text: str | None) -> str | None:
		if not text:
			return None
		flat = " ".join(unescape(text).split())
		return flat or None
