#!/usr/bin/env python3
"""
Command line interface for llm-file-rename-n-sort.
"""

# Standard Library
import argparse
import logging
from pathlib import Path
import urllib.request
from collections import Counter
import sys

# local repo modules
from .config import AppConfig, load_user_config, parse_exts
from .llm import AppleLLM, OllamaLLM, apple_models_available, choose_model
from .organizer import Organizer
from .scanner import iter_files

#============================================


def parse_args() -> argparse.Namespace:
	"""
	Parse CLI arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Rename and sort macOS files using a local LLM."
	)
	parser.add_argument(
		"-p",
		"--paths",
		dest="paths",
		nargs="+",
		required=True,
		help="Paths to scan (required).",
	)
	mode_group = parser.add_mutually_exclusive_group()
	mode_group.add_argument(
		"-a",
		"--apply",
		dest="apply",
		action="store_true",
		help="Perform renames and moves.",
	)
	mode_group.add_argument(
		"-d",
		"--dry-run",
		dest="dry_run",
		action="store_true",
		help="Only print planned actions (default).",
	)
	parser.add_argument(
		"-m",
		"--max-files",
		dest="max_files",
		type=int,
		help="Maximum files to process.",
	)
	parser.add_argument(
		"--max-depth",
		dest="max_depth",
		type=int,
		default=1,
		help="Maximum directory depth to scan (default 1).",
	)
	parser.add_argument(
		"-c",
		"--config",
		dest="config_path",
		help="Optional JSON or YAML config file.",
	)
	parser.add_argument(
		"-v",
		"--verbose",
		dest="verbose",
		action="store_true",
		help="Verbose logging.",
	)
	parser.add_argument(
		"-e",
		"--ext",
		dest="extensions",
		action="append",
		help="Include only files with these extensions (repeatable).",
	)
	parser.add_argument(
		"-t",
		"--target",
		dest="target_root",
		help="Target root for organized files (default ~/Organized).",
	)
	parser.add_argument(
		"-o",
		"--model",
		dest="model",
		help="Override Ollama model name.",
	)
	parser.add_argument(
		"--llm-backend",
		dest="llm_backend",
		choices=["macos", "ollama"],
		default="macos",
		help="Choose LLM backend: macos (default) or ollama.",
	)
	parser.add_argument(
		"-x",
		"--context",
		dest="context",
		help="Optional context string added to LLM prompts to keep naming on-theme (e.g., 'Biology class', 'Client ACME').",
	)
	parser.set_defaults(apply=False, dry_run=True)
	return parser.parse_args()


#============================================


def build_config(args: argparse.Namespace) -> AppConfig:
	"""
	Build runtime config from args and file.
	"""
	config = AppConfig()
	config.roots = [Path(p).expanduser() for p in args.paths]
	if args.target_root:
		config.target_root = Path(args.target_root).expanduser()
	if args.max_files:
		config.max_files = args.max_files
	if args.max_depth is not None:
		config.max_depth = args.max_depth
	exts = parse_exts(args.extensions) if args.extensions else None
	if exts:
		config.include_extensions = exts
	config.dry_run = True
	if args.apply:
		config.dry_run = False
	elif args.dry_run:
		config.dry_run = True
	if args.config_path:
		config.config_path = Path(args.config_path)
		user_cfg = load_user_config(config.config_path)
		if user_cfg.get("target_root"):
			config.target_root = Path(user_cfg["target_root"]).expanduser()
		if user_cfg.get("include_extensions"):
			config.include_extensions = parse_exts(user_cfg["include_extensions"])
		if user_cfg.get("context"):
			config.context = str(user_cfg.get("context"))
		if user_cfg.get("max_depth") is not None:
			config.max_depth = int(user_cfg.get("max_depth"))
		if user_cfg.get("llm_backend"):
			config.llm_backend = str(user_cfg.get("llm_backend"))
	if args.model:
		config.model_override = args.model
	if args.llm_backend:
		config.llm_backend = args.llm_backend
	if args.context:
		config.context = args.context
	config.verbose = args.verbose
	return config


#============================================


def build_llm(config: AppConfig):
	"""
	Instantiate LLM client with model selection.

	Args:
		config: Application configuration.

	Returns:
		OllamaLLM or AppleLLM instance.
	"""
	model = choose_model(config.model_override)
	system_prompt = ""
	if config.context:
		system_prompt = (
			"Keep names and categories aligned to this user/folder context: "
			+ config.context
		)
	base_url = "http://localhost:11434"
	if config.llm_backend == "ollama":
		if not _ollama_available(base_url):
			raise RuntimeError("Ollama backend selected but service is not reachable.")
		return OllamaLLM(model=model, system_message=system_prompt, base_url=base_url)
	if not apple_models_available():
		if _ollama_available(base_url):
			logging.warning("Apple Foundation Models unavailable; using Ollama backup.")
			return OllamaLLM(model=model, system_message=system_prompt, base_url=base_url)
		raise RuntimeError("No available LLM backend (Apple Foundation Models or Ollama).")
	return AppleLLM(model=model, system_message=system_prompt)


#============================================


def _color(text: str, code: str) -> str:
	if sys.stdout.isatty():
		return f"\033[{code}m{text}\033[0m"
	return text


#============================================


def _ollama_available(base_url: str) -> bool:
	"""
	Check if Ollama service is up.
	"""
	try:
		request = urllib.request.Request(f"{base_url}/api/tags", method="GET")
		with urllib.request.urlopen(request, timeout=2) as response:
			return response.status < 400
	except Exception:
		return False


#============================================


def main() -> None:
	"""
	Entry point for the CLI.
	"""
	args = parse_args()
	config = build_config(args)
	if config.verbose:
		logging.basicConfig(level=logging.INFO)
	else:
		logging.basicConfig(level=logging.WARNING)
	llm = build_llm(config)
	organizer = Organizer(config=config, llm=llm)
	files = iter_files(config)
	print(f"{_color('[SCAN]', '34')} Found {len(files)} files to consider.")
	if files:
		ext_counter = Counter(p.suffix.lower().lstrip(".") for p in files)
		top_exts = ext_counter.most_common(8)
		summary = ", ".join(f"{ext}:{count}" for ext, count in top_exts if ext)
		if summary:
			print(f"{_color('[SCAN]', '34')} Top extensions: {summary}")
	limited_files = files
	if config.max_files:
		limited_files = limited_files[: config.max_files]
	organizer.process_one_by_one(limited_files)


#============================================


if __name__ == "__main__":
	main()
