#!/usr/bin/env python3
"""
Moondream2 captioning helpers bundled with this repo.
"""

from __future__ import annotations

import torch
from PIL import Image
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
import transformers.utils.logging as translogging


MODEL_ID = "vikhyatk/moondream2"
MODEL_REVISION = "2025-01-09"


def _get_mps_device() -> str:
	if not torch.backends.mps.is_available():
		raise RuntimeError("Moondream2 requires Apple Silicon with MPS support.")
	return "mps"


def _resize_image(image: Image.Image, max_dimension: int) -> Image.Image:
	width, height = image.size
	if max(width, height) <= max_dimension:
		return image
	if width > height:
		new_width = max_dimension
		new_height = int((max_dimension / width) * height)
	else:
		new_height = max_dimension
		new_width = int((max_dimension / height) * width)
	return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def setup_ai_components(prompt: str | None = None) -> dict:
	"""
	Setup the Moondream2 model and tokenizer.
	"""
	translogging.set_verbosity_error()
	device = _get_mps_device()
	model = AutoModelForCausalLM.from_pretrained(
		MODEL_ID,
		trust_remote_code=True,
		revision=MODEL_REVISION,
		torch_dtype=torch.float16,
		device_map={"": device},
	)
	tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
	model.to(device)
	return {
		"model": model,
		"tokenizer": tokenizer,
		"device": device,
		"prompt": prompt,
	}


def generate_caption(image_path: str, ai_components: dict) -> str:
	"""
	Generate a caption for an image using Moondream2.
	"""
	image = Image.open(image_path)
	image = _resize_image(image, 1280)
	model = ai_components["model"]
	prompt = ai_components.get("prompt")
	if prompt:
		result = model.query(image, prompt)
		caption = result.get("answer", "")
	else:
		result = model.caption(image, length="normal")
		caption = result.get("caption", "")
	if not caption:
		raise RuntimeError("Moondream2 returned an empty caption.")
	return caption
