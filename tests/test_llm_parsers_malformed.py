#!/usr/bin/env python3
"""Malformed XML parsing scenarios that should still succeed."""

from rename_n_sort.llm_parsers import parse_keep_response, parse_rename_response, parse_sort_response


def test_parse_rename_with_chatter_and_code_fence():
	text = (
		"some chatter\n"
		"```xml\n"
		"<new_name>File.pdf</new_name><reason>title</reason>\n"
		"```\n"
		"more chatter"
	)
	result = parse_rename_response(text)
	assert result.new_name == "File.pdf"
	assert result.reason == "title"


def test_parse_rename_with_unclosed_response():
	text = "<response><new_name>File.pdf</new_name><reason>ok</reason>"
	result = parse_rename_response(text)
	assert result.new_name == "File.pdf"
	assert result.reason == "ok"


def test_parse_rename_without_response_wrapper():
	text = "<new_name>File.pdf</new_name><reason>ok</reason>"
	result = parse_rename_response(text)
	assert result.new_name == "File.pdf"
	assert result.reason == "ok"


def test_parse_rename_accepts_missing_reason():
	result = parse_rename_response("<new_name>Only.pdf</new_name>")
	assert result.new_name == "Only.pdf"
	assert result.reason == ""


def test_parse_rename_with_nested_response_string():
	text = (
		"<response>```xml\\n"
		"<response><new_name>Nested.pdf</new_name><reason>nested</reason></response>\\n"
		"```</response>"
	)
	result = parse_rename_response(text)
	assert result.new_name == "Nested.pdf"
	assert result.reason == "nested"


def test_parse_keep_with_escaped_response():
	text = "&lt;response&gt;&lt;keep_original&gt;true&lt;/keep_original&gt;" \
		"&lt;reason&gt;stem is numeric&lt;/reason&gt;&lt;/response&gt;"
	result = parse_keep_response(text, "abc")
	assert result.stem_action == "keep"
	assert "numeric" in result.reason


def test_parse_keep_with_unclosed_response_and_missing_stem_reason():
	text = (
		"<response><stem_action>drop</stem_action>"
		"<reason>too generic</reason>"
	)
	result = parse_keep_response(text, "abc")
	assert result.stem_action == "drop"
	assert result.reason == "too generic"


def test_parse_keep_accepts_prompt_echo_text():
	result = parse_keep_response(
		"<stem_action>keep</stem_action>"
		"<reason>return only the tags below</reason>",
		"abc",
	)
	assert result.stem_action == "keep"
	assert "tags" in result.reason


def test_parse_sort_with_unclosed_response():
	text = (
		"<response><category>Document</category>"
	)
	result = parse_sort_response(text, ["/tmp/a.pdf"])
	assert result.assignments["/tmp/a.pdf"] == "Document"


def test_parse_sort_without_response_wrapper():
	text = "<category>Image</category>"
	result = parse_sort_response(text, ["/tmp/a.pdf"])
	assert result.assignments["/tmp/a.pdf"] == "Image"
