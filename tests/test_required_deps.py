#!/usr/bin/env python3
"""
Ensure required dependencies are installed and available.
"""


def test_moondream2_available():
	from rename_n_sort import moondream2_caption

	assert hasattr(moondream2_caption, "setup_ai_components")


def test_apple_foundation_models_available():
	from applefoundationmodels import apple_intelligence_available

	assert apple_intelligence_available() is True


def test_tesseract_available():
	import pytesseract

	_ = pytesseract.get_tesseract_version()
