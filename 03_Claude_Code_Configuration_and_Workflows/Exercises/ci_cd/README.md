# Exercise — Claude Code in a CI/CD Review Pipeline

Bash is the right language for this exercise — Task 3.6 is a CLI/pipeline integration concern (how you invoke the `claude` binary from a shell step in CI), not an SDK-language concern. There's no Python/JS/TS split here because none of this goes through the Messages API SDKs; it goes through the `claude` CLI directly.

## Files

| File | Demonstrates |
| ---- | ------------- |
| `run_review.sh` | A CI pipeline step: `claude -p "..." --output-format json --json-schema schema.json`, prior-findings de-duplication, and failing the build on new blocking findings |
| `schema.json` | The JSON Schema passed to `--json-schema` — defines exactly what a "finding" looks like, including the `is_new` field used to suppress duplicate PR comments across re-runs |

## What each piece maps to (Theory/03_Iterative_Refinement_and_CICD.md)

- **`-p` / `--print`** — non-interactive mode. Without it, `claude "..."` in a CI job hangs waiting for input instead of completing or failing cleanly.
- **`--output-format json` + `--json-schema schema.json`** — structured, machine-parseable output. This is what lets a downstream step turn findings into individual inline PR comments instead of a single unstructured text blob.
- **Prior-findings de-duplication** — the script reads `prior_findings.json` (if a previous run left one) and asks Claude to mark already-reported, still-unaddressed issues with `is_new: false`, so re-running the review after a new commit doesn't repost every old comment.
- **CLAUDE.md as context** — the prompt explicitly defers to "the review criteria and fixture conventions documented in this repository's CLAUDE.md and .claude/rules/ files" rather than inventing criteria inline. See [[../claude_code_project/CLAUDE.md]] for what that looks like in practice.
- **Session isolation** — this script is meant to run as its **own** invocation, separate from whatever session generated the code being reviewed (e.g. a separate CI job step, not a continuation of the PR author's local Claude Code session). See the "session isolation for self-review" warning in the theory note for why that separation matters.

## How to try this safely

This script calls a real `claude` CLI with a real API key/session if you run it as-is. To exercise it without needing a live pipeline:

1. Read `run_review.sh` top to bottom first — it's short and every line is commented with *why*, not just *what*.
2. In a real repo with `claude` installed and authenticated, copy this script and `schema.json` into a `.github/workflows/scripts/` (or equivalent) directory.
3. Run it manually once against a local diff: `./run_review.sh main` from inside a git repo with uncommitted or branched changes against `main`.
4. Inspect `review_findings.json` — confirm it validates against `schema.json` and that each finding has a `file`, `severity`, `category`, `message`, and `is_new`.
5. Make a second, unrelated commit and re-run the script — confirm `prior_findings.json` (written by the first run) causes previously-reported, still-open findings to come back with `is_new: false` instead of being re-flagged as new.
6. Wire the exit code (`exit 1` on new blocking findings) into your actual CI job so a blocking finding fails the build.

No exercise here requires you to actually wire this into a live GitHub Actions/GitLab CI config — the point is understanding the flags and the JSON contract, which you can verify locally with any git repo.
