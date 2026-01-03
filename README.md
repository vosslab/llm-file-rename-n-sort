# macos-llm-file-cleanup

Local-first macOS tool that scans Downloads, Desktop, and Documents, extracts metadata with pluggable extractors, and uses a local Ollama LLM (with deterministic fallback) to rename and optionally sort files into category folders. Designed for Apple Silicon with no cloud calls.

## Capabilities
- Recursively scan messy folders with extension filters and file limits.
- Extract metadata via dedicated plugins per file type; fall back to a generic mdls/stat reader.
- Ask a chat-based Ollama model (persistent history) for a new file name and category, or use a deterministic Dummy heuristic when Ollama is unavailable.
- Apply safe renames/moves with collision avoidance; dry run by default.

## Supported file types (v1)
- Documents: pdf, doc, docx, odt, rtf, pages, txt, md
- Presentations: ppt, pptx, odp
- Spreadsheets/data: xls, xlsx, ods, csv, tsv (csv/tsv handled by a dedicated plugin)
- Images: jpg, jpeg, png, gif, heic, tif, tiff, bmp (bitmap) and svg/svgz (vector via dedicated plugin)
- Images can optionally use Moondream2 (if `ai_image_caption/moondream2.py` deps are installed) to auto-caption; install Pillow + pillow-heif (see `image` extra) for HEIC support.
- Audio: mp3, wav, flac, aiff, ogg
- Video: mp4, mov, mkv, webm, avi
- Code/scripts (as text): py, m, cpp, js, sh, pl, rb, php
- Generic fallback for anything else

## Architecture overview
- `cli.py`: argparse interface, builds config, selects LLM, runs organizer.
- `config.py`: runtime settings, extension parsing, optional YAML/JSON overrides.
- `scanner.py`: iterates files respecting recursion, limits, and hidden/extension rules.
- `plugins/`: per-type metadata extractors returning `FileMetadata` objects.
	- Documents: `pdf.py`, `document_plugin.py`, `docx_plugin.py`, `odt_plugin.py`
	- Presentations: `presentation_plugin.py`
	- Spreadsheets/data: `spreadsheet_plugin.py`
	- Media: `image_plugin.py`, `audio_plugin.py`, `video_plugin.py`
	- Code/scripts: `code_plugin.py`
	- Text: `text.py`
	- Fallback: `generic.py`
- `llm.py`: LocalLLM interface, `OllamaChatLLM` (chat history, /api/chat), `DummyLLM`, filename/category helpers, VRAM/RAM-based model chooser.
- `organizer.py`: orchestrates metadata -> LLM suggestion -> target path -> apply (with collision handling).
- `renamer.py`: safe move/rename with deduping.
- `tests/`: pytest coverage for heuristics, plugin selection, model selection, and collision handling.

## LLM integration
- Interface: `suggest_name_and_category(metadata: dict, current_name: str) -> tuple[str, str]`
- Ollama: `OllamaChatLLM` keeps in-memory chat messages and posts to `http://localhost:11434/api/chat` with `stream: false`.
- Dummy fallback: deterministic naming from title/keywords/summary and extension-based categories.
- Availability check: if Ollama is unreachable at startup, the tool logs a warning and uses DummyLLM.
- Prompt format expects lines:
	- `new_name: <file name without path>`
	- `category: <short category or empty>`
- Model selection: VRAM/unified memory heuristic
	- >30 GB → `gpt-oss:20b`
	- >14 GB → `phi4:14b-q4_K_M`
	- >4 GB → `llama3.2:3b-instruct-q5_K_M`
	- else `llama3.2:1b-instruct-q4_K_M`
	- Override with `--model`.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
# install all dependencies (LLM, captions, docs, etc.)
pip install -r requirements.txt
```

## Quick start
```bash
python -m rename_n_sort --paths /path/to/folder --max-files 20          # dry run
python -m rename_n_sort --paths /path/to/folder --apply --max-files 10  # apply moves
python -m rename_n_sort --paths /path/to/folder --apply --model "llama3.2:3b-instruct-q5_K_M"
```

## CLI reference
- `-p/--paths PATH [PATH ...]` required scan roots
- `-d/--dry-run` dry run
- `-a/--apply` perform renames and moves
- `-m/--max-files N` limit processed files
- `-c/--config FILE` optional JSON or YAML overrides
- `-e/--ext EXT` repeatable extension filter
- `-g/--category CAT` limit to a category (docs, data, images, audio, video, code)
- `-t/--target PATH` target root (default `~/Organized`)
- `-r/--recursive` enable recursion; `-s/--stop-recursive` disable recursion
- `-o/--model MODEL` override Ollama model
- `-v/--verbose` verbose logging
- `-x/--context "text"` optional user/folder context to keep naming on-theme
- `-z/--randomize` shuffle processing order (useful for testing)

## Configuration file (JSON/YAML)
Supported keys:
- `target_root`: string path
- `include_extensions`: list of extensions
- `roots`: list of scan roots

## Naming and moves
- Target path: `<target_root>/cleaned/<category>/<new_name><ext>`
- Collisions: deduped with numeric suffixes.
- Hidden files skipped by default.
- Dry run prints planned moves; apply performs renames/moves.

## Testing
```bash
python -m pytest
```

## Notes and limitations
- macOS-only; uses `mdls` when available for fast metadata.
- Ollama must be running locally for chat mode; otherwise the Dummy heuristic is used.
- Plugins aim for lightweight metadata (size, extension, optional title/preview); heavy parsing is out-of-scope for v1.
