---
name: fix-ci-failure
description: Fix failing CI tests by diagnosing pytest errors and applying the smallest safe production-code patch so `uv run pytest` passes. Use when a repository has red CI due to failing tests, when a user provides `pytest.log`, when the prompt says "fix failing CI tests", "minimal diff", or "don't modify tests", or when the request is to autofix CI without modifying tests.
---

# Fix CI Failure

Resolve failing test suites quickly while keeping changes minimal and reviewable.

## Inputs

- `pytest.log` (if provided)
- Repository source code and tests
- Existing CI context or failure message

## Required Output

Return:
- A patch that changes only production code unless explicitly allowed otherwise
- A short summary with root cause and why the fix is minimal

## Hard Constraints

- Do not modify tests.
- Keep the diff minimal and focused on the failing behavior.
- Preserve existing public behavior outside the failing path when possible.
- Stop once `uv run pytest` passes unless the user asks for follow-up cleanup.

## Workflow

1. Reproduce failures.
Run `uv run pytest` (or target the failing subset first if `pytest.log` points to specific tests).

2. Isolate root cause.
Read traceback and failing assertions, then identify the smallest code path that can explain the failure.

If CI is failing but local tests are green:
- Read `pytest.log` if available.
- Infer the most likely hidden-test or environment edge case from implementation/test mismatch.
- Apply one minimal, production-only defensive fix tied to that likely edge case.
- Re-run `uv run pytest` and stop if green.

3. Implement minimal fix.
Patch production files only. Avoid refactors, style-only changes, or broad rewrites unless they are necessary for correctness.

4. Verify.
Run `uv run pytest` and confirm all tests pass.

5. Summarize.
Report:
- Root cause
- Files changed
- Why the diff is minimal
- Final test result from `uv run pytest`

## Heuristics For Minimal Diffs

- Prefer local conditional guards over architectural rewrites.
- Match existing project conventions; do not introduce new frameworks or patterns.
- Limit scope to symbols exercised by failing tests.
- Avoid touching unrelated files.

## Failure Handling

If tests still fail:
- Re-check whether the first fix addressed symptom instead of cause.
- Inspect the next failing traceback and iterate with another minimal production-code patch.
- Call out blockers explicitly (missing dependency, environment mismatch, unclear CI-only behavior).

## Response Template

Use this compact format:

```text
Patch:
<diff or summary of applied patch>

Summary:
- Root cause: ...
- Files changed: ...
- Why minimal: ...
- Verification: `uv run pytest` -> <result>
```
