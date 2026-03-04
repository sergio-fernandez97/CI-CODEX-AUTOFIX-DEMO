Fix failing CI by making `uv run pytest -q` pass.

Rules:
- Do NOT modify files under `tests/`
- Prefer minimal diffs
- Keep existing function signatures

Steps:
1) Run tests: `uv run pytest -q`
2) Read failures and determine root cause
3) Patch only `src/` code
4) Re-run `uv run pytest -q` until green

When done:
- Summarize what changed
- List the commands you ran