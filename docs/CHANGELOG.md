# Changelog

## 2026-01-03
- Update module references to `rename_n_sort` across code, tests, CLI entrypoint, and docs.
- Add pytest `conftest.py` to ensure local package imports resolve without installation.
- Make Apple Foundation Models the primary macOS backend with Ollama fallback; remove DummyLLM fallback behavior.
- Process files one-by-one by default and simplify CLI flags accordingly.
- Rename console prefixes to `[SCAN]`, `[FILE]`, `[WHY]`, `[RENAME]`, and `[DEST]`, plus add per-file separators and shorter path display.
- Require Moondream2 captioning and OCR (pytesseract) for image metadata; include OCR text in summaries.
- Add `Brewfile`, clean and sort `pip_requirements.txt`, and add sample file generator + dependency availability tests.
- Remove `source_me_for_testing.sh`.
- Rename the distribution/CLI entrypoint to `llm-file-rename-n-sort`.
- Bundle Moondream2 captioning helpers directly in the repo to remove `OTHER_REPOS` dependencies.
- Rename `MacOSLocalLLM` to `AppleLLM`, rename the base class to `BaseClassLLM`, and add `--max-depth` (default 1).
- Add mutually-exclusive `--apply` and `--dry-run` flags (dry-run default) for safer CLI behavior.
- Default target root now uses `<search_root>/Organized` to keep files on the same drive unless `--target` is set.
- Clarify `--context` to indicate it is injected into LLM prompts with examples.

## 2026-01-02
- Bump version to `26.01` and add root `VERSION` file synced with `pyproject.toml`.
- Lazy-import `ai_image_caption.moondream2` so optional caption dependencies load only when needed.
- Add `--one-by-one` mode to process each file through PLAN1/PLAN2 (and DRY RUN/APPLY) before starting the next file.
- Add `--llm-backend {macos,ollama}` to choose between the default macOS-local backend and Ollama.
- Print rename/keep/category decision details by default.
- Fix Ollama sorting-mode parsing to fill missing categories using the actual file indices in the batch (not `0..N-1`).
- Add tests for VERSION sync and keep-original heuristics, plus a CLI smoke script at `tests/run_smoke_cli.sh`.
- Fix pyflakes warnings (unused imports and duplicate dictionary keys).
- Update Ollama prompts/parsing to use an XML `<response>...</response>` block for robust extraction from chatty model outputs.
- Add repo-root runner script `run_file_cleanup.py`.
- Switch PDF parsing dependency from PyPDF2 to pypdf.
