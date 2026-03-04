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

### 4. Self-healing CI in GitHub Actions
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

## Challenge — Build Your Own Self-Healing CI Repo
### Objective
Each student must create a tiny repo from scratch (any programming language) that includes:
1. source code (2–4 small functions)
2. tests (that can fail)
3. CI workflow that runs tests on PRs
4. Codex Auto-fix workflow that can fix failing tests and push a patch
5. Grading workflow that scores the PR automatically

You should experience the full GitHub Actions setup end-to-end.

### Deliverables (what you must submit)
Your repo must contain:
- `README.md` with:
  - how to run tests locally
  - how to run CI
  - how to run Auto-fix workflow
  - how grading works
- A working CI workflow: `.github/workflows/ci.yml`
- A working auto-fix workflow: `.github/workflows/codex-autofix.yml`
- A grading workflow: `.github/workflows/grade.yml`
- A Codex prompt file used by the auto-fix workflow: `.codex/prompts/fix-ci.prompt.md`

### Step-by-Step Instructions

#### 1. Create a new repo
Create a new GitHub repository (public or private).

Clone it locally:
```bash
git clone <repo-url>
cd <repo-name>
```

#### 2. Pick your language + minimal project skeleton
Choose one language and create the smallest possible structure.

Examples:
- Python: `src/`, `tests/`, `pyproject.toml` (uv recommended)
- Node/TypeScript: `src/`, `test/`, `package.json`
- Go: `*.go`, `_test.go`
- Java: Maven/Gradle minimal project
- Rust: `src/lib.rs`, `tests/`

Rule: keep it tiny. 2-4 functions only.

#### 3. Write your own functions
Create a module/library with 2-4 functions.

Good examples:
- string utilities
- math helpers
- parsing helpers
- date formatting helpers

Important: make at least one function easy to break (so tests can fail).

#### 4. Write tests
Write tests that validate your functions.

Requirements:
- tests must run in one command (e.g. `pytest`, `npm test`, `go test ./...`)
- tests should be deterministic

#### 5. Verify locally: tests pass first
Before adding CI, confirm everything is green locally.

Example commands:
- Python: `uv run pytest -q`
- Node: `npm test`
- Go: `go test ./...`

#### 6. Add CI workflow (GitHub Actions)
Create `.github/workflows/ci.yml`.

This workflow must run on:
- `pull_request`
- push to `main`

It must:
- checkout code
- setup language runtime
- install dependencies
- run tests

What you MUST modify in `ci.yml`:
- change the install + test commands to match your language

Replace these lines (example from Python):
```yaml
- run: uv sync
- run: uv run pytest -q
```

With your language equivalent, for example:

Node:
```yaml
- run: npm ci
- run: npm test
```

Go:
```yaml
- run: go test ./...
```

#### 7. Add Codex Auto-fix workflow
Create `.github/workflows/codex-autofix.yml`.

This workflow will be triggered manually with `workflow_dispatch` and takes one input:
- `branch` (the branch to fix)

It must:
- checkout that branch
- run tests (capture logs)
- run Codex non-interactively (recommended: `openai/codex-action@v1`)
- re-run tests
- commit and push changes

What you MUST modify in `codex-autofix.yml`:
- test command (twice):
  - the `Run tests (capture logs)` step
  - the `Re-run tests (must be green)` step

Example (Python):
```bash
uv run pytest -q 2>&1 | tee pytest.log
uv run pytest -q
```

Replace with your test command:

Node:
```bash
npm test 2>&1 | tee test.log
npm test
```

Go:
```bash
go test ./... 2>&1 | tee test.log
go test ./...
```

Prompt file path (if you name it differently):
```yaml
prompt-file: .codex/commands/fix-ci.md
```

#### 8. Add a Codex prompt file (required)
Create:
```text
.codex/commands/fix-ci..md
```

Update it to match your language + test command.

Template:
```text
You are fixing a CI failure in this repository.

Goal: make the test suite pass.

Rules:
- Do NOT weaken or delete tests.
- Prefer minimal diff.
- Fix the root cause in source code.
- After changes, run the tests and ensure they pass.

Test command:
<PUT YOUR TEST COMMAND HERE>

Start by running the tests and inspecting the failure output.
```

What you MUST modify here:
- the test command
- any language-specific constraints (e.g., "don't change package.json scripts")

#### 9. Add grading workflow
Create `.github/workflows/grade.yml`.

The grader must:
- run tests on PRs
- apply quality gates
- comment a score on the PR

What you MUST modify in `grade.yml`:
- test command
- optional quality gates paths
- if your tests folder is not `tests/`, adjust it
- if your source folder is not `src/`, adjust it

Example (Python):
```bash
uv run pytest -q
if echo "$CHANGED" | grep -q "tests/"; then ...
```

Replace with:
- Node: `npm test`
- Go: `go test ./...`

And update folder checks if needed.

### How to Complete the Challenge (Student Flow)

#### A. Push initial version (green)
Commit everything (code, tests, workflows):
```bash
git add -A
git commit -m "init: add code, tests, CI, autofix, grading"
git push -u origin main
```

Confirm CI is green on `main`.

#### B. Create a failing PR
Create branch:
```bash
git checkout -b challenge/break-ci
```

Break one function (source code only).

Commit + push:
```bash
git add -A
git commit -m "break: introduce failing tests"
git push -u origin challenge/break-ci
```

Open a PR to `main` and confirm CI fails.

#### C. Run auto-fix workflow
GitHub -> Actions -> Codex Auto-fix

Run workflow with input:
```text
branch = challenge/break-ci
```

Confirm:
- a new commit is pushed to your branch
- CI turns green

#### D. Check grade
The Grade workflow will comment a score in the PR.

### Success Criteria (Pass/Fail)
You pass if your repo demonstrates all of these:
- CI runs on PR and can fail
- Auto-fix workflow runs and pushes a patch
- CI becomes green after auto-fix
- Grade workflow comments a score
- Tests were not weakened/deleted
