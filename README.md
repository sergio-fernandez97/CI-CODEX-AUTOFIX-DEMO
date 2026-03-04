# CI Codex Autofix Demo (uv + pytest)

This tiny repo is designed for a 1-hour live session on:
- GitHub Actions CI
- Codex CLI custom commands
- “Skills” as reusable workflow specs
- Self-healing pipelines (auto-fix)

## Prerequisites
- Python 3.11+
- uv installed locally
- Codex CLI installed locally
- For GitHub Actions auto-fix: set repo secret `OPENAI_API_KEY`

---

## 1) Setup (local)
From repo root:

```bash
uv sync
uv run pytest -q