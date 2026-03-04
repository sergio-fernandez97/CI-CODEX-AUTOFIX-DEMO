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
```
---

##  Live Session

What you’ll build
By the end of the session you will:
* Trigger a failing CI run via a PR
* Fix locally using Codex CLI via a custom command (/fix-ci)
* Run a non-interactive Codex auto-fix workflow in GitHub Actions (no TTY required)
* See the PR become green again
* Get an automated grade comment on the PR

### 0. Prerequisites
**Local tools**
1. Install uv
2. Install Codex CLI (whatever method your environment uses)
3. Authenticate Codex locally (so codex works on your machine)

#### Repo setup (in GitHub)
1. Ensure these files exist on main:
* `.github/workflows/ci.yml`
* `.github/workflows/codex-autofix.yml`
* `.github/workflows/grade.yml`

2. Add GitHub Actions secret:
* Repo → Settings → Secrets and variables → Actions
* Add New repository secret
* Name: `OPENAI_API_KEY`
* Value: your OpenAI API key

.codex/commands/fix-ci.md

### 1. Baseline: run tests locally
```bash
uv sync
uv run pytest -q
```
tests FAIL!
### 2. Show CI failing (PR flow)
1. Create a branch
```bash
# Given that we are in main live-session
git checkout -b demo/break-ci
```
2. Make CI fail + Commit + push
```bash
git add -A
git commit -m "demo: break CI"
git push -u origin demo/break-ci
```
3. Open a PR
Open PR from demo/break-ci → main
Confirm CI workflow runs and is red

### 3. Fix locally with Codex custom command
Create custom command with the following command:
```
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
```
Codex should:
* `run uv run pytest -q`
* patch `src/` code only (do not modify tests)
* re-run tests until green
* summarize the fix
Verify locally:
```bash
uv run pytest -q
```
Commit the fix:
```bash
git add -A
git commit -m "fix: make tests pass"
git push -u origin demo/break-ci
```

#### 4. Self-healing CI in GitHub Actions
Now we’ll let the pipeline auto-fix itself without local interaction.

1. Create a new failing commit (again)
Make another small breaking change in `src/string_utils.py`, then:
```bash
git add -A
git commit -m "demo: break CI again"
git push -u origin demo/break-ci
```

2. Run the Auto-fix workflow
* GitHub → Actions
* Select Codex Auto-fix
* Click Run workflow
* Set input branch to:
* demo/break-ci
* Run

Expected behavior:
* workflow checks out your branch
* runs tests and captures output
* runs Codex non-interactively
* commits a patch back to the branch
* re-runs tests (must pass)
* Go back to PR:
* you should see a new bot commit
* CI becomes green again

5. Grading (automatic) (5 min)
The Grade workflow runs automatically on every PR update and comments a score.
Typical rubric:
* Tests pass (6 pts)
* Tests folder unchanged (2 pts)
* Diff small enough (2 pts)
You should see a comment like:
* Score: 10/10
* plus details (tests exit code, changed files, line count)
