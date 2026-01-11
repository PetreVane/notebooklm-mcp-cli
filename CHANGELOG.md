# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.9] - 2026-01-11

### Added
- **Automatic re-authentication** - Server now survives token expirations without restart
  - Three-layer recovery: CSRF refresh → disk reload → headless Chrome auth
  - Works with long-running MCP sessions (e.g., MCP Super Assistant proxy)
- `refresh_auth` MCP tool for explicit token reload
- `run_headless_auth()` function for background authentication (if Chrome profile has saved login)
- `has_chrome_profile()` helper to check if profile exists

### Changed
- `launch_chrome()` now returns `subprocess.Popen` handle instead of `bool` for cleanup control
- `_call_rpc()` enhanced with `_deep_retry` parameter for multi-layer auth recovery

## [0.1.8] - 2026-01-10

### Added
- `constants.py` module as single source of truth for all API code-name mappings
- `CodeMapper` class with bidirectional lookup (name→code, code→name)
- Dynamic error messages now show valid options from `CodeMapper`

### Changed
- **BREAKING:** `quiz_create` now accepts `difficulty: str` ("easy"|"medium"|"hard") instead of `int` (1|2|3)
- All MCP tools now use `constants.CodeMapper` for input validation
- All API client output now uses `constants.CodeMapper` for human-readable names
- Removed ~10 static `_get_*_name` helper methods from `api_client.py`
- Removed duplicate `*_codes` dictionaries from `server.py` tool functions

### Fixed
- Removed duplicate code block in research status parsing

## [0.1.7] - 2026-01-10

### Fixed
- Fixed URL source retrieval by implementing correct metadata parsing in `get_notebook_sources_with_types`
- Added fallback for finding source type name in `get_notebook_sources_with_types`

## [0.1.6] - 2026-01-10

### Added
- `studio_status` now includes mind maps alongside audio/video/slides
- `delete_mind_map()` method with two-step RPC deletion
- `RPC_DELETE_MIND_MAP` constant for mind map deletion
- Unit tests for authentication retry logic

### Fixed
- Mind map deletion now works via `studio_delete` (fixes #7)
- `notebook_query` now accepts `source_ids` as JSON string for compatibility with some AI clients (fixes #5)
- Deleted/tombstone mind maps are now filtered from `list_mind_maps` responses
- Token expiration handling with auto-retry on RPC Error 16 and HTTP 401/403

### Changed
- Updated `bl` version to `boq_labs-tailwind-frontend_20260108.06_p0`
- `delete_studio_artifact` now accepts optional `notebook_id` for mind map fallback

## [0.1.5] - 2026-01-09

### Fixed
- Improved LLM guidance for authentication errors

## [0.1.4] - 2026-01-09

### Added
- `source_get_content` tool for raw text extraction from sources

## [0.1.3] - 2026-01-08

### Fixed
- Chrome detection on Linux distros

## [0.1.2] - 2026-01-07

### Fixed
- YouTube URL handling - use correct array position

## [0.1.1] - 2026-01-06

### Changed
- Improved research tool descriptions for better AI selection

## [0.1.0] - 2026-01-05

### Added
- Initial release
- Full NotebookLM API client with 31 MCP tools
- Authentication via Chrome DevTools or manual cookie extraction
- Notebook, source, query, and studio management
- Research (web/Drive) with source import
- Audio/Video overview generation
- Report, flashcard, quiz, infographic, slide deck creation
- Mind map generation
