#!/usr/bin/env python3
"""
Tests for shared prompt builders.
"""

from rename_n_sort.llm_prompts import KeepRequest, RenameRequest, build_keep_prompt, build_rename_prompt


def test_rename_prompt_includes_current_name():
	req = RenameRequest(metadata={"extension": "pdf"}, current_name="old.pdf")
	prompt = build_rename_prompt(req)
	assert "current_name: old.pdf" in prompt
	assert "Return only the tags shown below" in prompt


def test_keep_prompt_requires_stem_reason():
	req = KeepRequest(
		original_stem="ABC123",
		suggested_name="NewName",
		extension=None,
		features={"has_letter": True},
	)
	prompt = build_keep_prompt(req)
	assert "Reason should mention what useful info is in the stem" in prompt
	assert "<stem_action>" in prompt
	assert "<reason>" in prompt
