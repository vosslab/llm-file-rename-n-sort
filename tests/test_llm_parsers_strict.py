#!/usr/bin/env python3
"""
Strict parsing error cases for LLM outputs.
"""

import pytest

from rename_n_sort.llm_parsers import ParseError, parse_keep_response, parse_rename_response, parse_sort_response


def test_parse_rename_missing_response_raises():
	with pytest.raises(ParseError):
		parse_rename_response("no tags here")


def test_parse_rename_missing_name_raises():
	with pytest.raises(ParseError):
		parse_rename_response("<reason>why</reason>")


def test_parse_keep_missing_reason_raises():
	with pytest.raises(ParseError):
		parse_keep_response(
			"<keep_original>true</keep_original>",
			"abc",
		)


def test_parse_keep_duplicate_reason_raises():
	with pytest.raises(ParseError):
		parse_keep_response(
			"<keep_original>true</keep_original>"
			"<reason>one</reason><reason>two</reason>",
			"abc",
		)


@pytest.mark.parametrize(
	"keep_value, expected",
	[
		("true", True),
		("TRUE", True),
		("1", True),
		("yes", True),
		("false", False),
		("FALSE", False),
		("0", False),
		("no", False),
	],
)
def test_parse_keep_boolean_variants(keep_value, expected):
	result = parse_keep_response(
		f"<keep_original>{keep_value}</keep_original>"
		"<reason>stem looks numeric</reason>",
		"abc",
	)
	assert result.keep_original is expected


def test_parse_keep_duplicate_keep_original_raises():
	with pytest.raises(ParseError):
		parse_keep_response(
			"<keep_original>true</keep_original>"
			"<keep_original>false</keep_original>"
			"<reason>two values</reason>",
			"abc",
		)


def test_parse_sort_duplicate_category_raises():
	with pytest.raises(ParseError):
		parse_sort_response(
			"<category>Document</category><category>Image</category>",
			["/tmp/a.pdf"],
		)


def test_parse_sort_missing_category_raises():
	with pytest.raises(ParseError):
		parse_sort_response(
			"no category tag here",
			["/tmp/a.pdf"],
		)
