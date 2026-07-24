---
tags: [setup, exercises, claude-code]
topic: "03 - Claude Code Configuration & Workflows"
---

# Exercises Setup — Claude Code Configuration & Workflows

## Why this folder looks different from the other domains

Domains 1, 2, 4, and 5 test how you write code *against* the Claude API — so their exercises are Python/JavaScript/TypeScript scripts you run with an `ANTHROPIC_API_KEY`. Domain 3 tests how you **configure a repository** for the Claude Code CLI — CLAUDE.md hierarchy, `.claude/rules/`, commands, skills, plan mode, and CI integration. None of that is a Messages-API scripting concern, so there's no meaningful python/javascript/typescript split here. Instead:

- [[claude_code_project/README|Exercises/claude_code_project/]] — a small sample repository containing the actual configuration files Claude Code reads: `CLAUDE.md`, `.claude/rules/*.md`, `.claude/commands/review.md`, `.claude/skills/code-audit/SKILL.md`, and `.mcp.json`.
- [[ci_cd/README|Exercises/ci_cd/]] — a bash script (`run_review.sh`) plus a `schema.json`, demonstrating `claude -p "..." --output-format json --json-schema schema.json` for CI/CD review pipelines. Bash, not Python/JS/TS, because this is a CLI/pipeline concern.

The previously-empty `Exercises/python/`, `Exercises/javascript/`, and `Exercises/typescript/` placeholder directories have been removed — they would have stayed empty and misleading, since this domain has no per-language exercise content to put in them.

## Prerequisites

- The [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated (`claude --version` to check).
- A local git repository to experiment in — either a scratch repo or a disposable branch of a real one. **Do not** experiment directly on a shared team repo's `main` branch.

## How to exercise `claude_code_project/`

These files are not "run" like a script — they're configuration the `claude` CLI reads automatically when you start it inside a matching directory. Full walkthrough (drop into a scratch repo, run `/memory`, trigger `/review`, edit a file matching a rule's glob to see it activate, invoke the `code-audit` skill, inspect `.mcp.json` env expansion) is in [[claude_code_project/README|claude_code_project/README.md]] — read it there rather than duplicating the steps here.

Quick start:

```bash
mkdir -p /tmp/scratch-repo && cd /tmp/scratch-repo && git init -q
cp -r "<vault>/03_Claude_Code_Configuration_and_Workflows/Exercises/claude_code_project/." .
claude
# then, inside the Claude Code session:
#   /memory
#   /review main
```

## How to exercise `ci_cd/`

`run_review.sh` and `schema.json` demonstrate the CI-facing flags (`-p`, `--output-format json`, `--json-schema`). Read [[ci_cd/README|ci_cd/README.md]] first — it's short and explains exactly what each flag buys you and how to run the script safely against a real local diff before ever wiring it into an actual pipeline.

Quick start:

```bash
cd "<vault>/03_Claude_Code_Configuration_and_Workflows/Exercises/ci_cd"
chmod +x run_review.sh
./run_review.sh main   # run from inside a git repo with a diff against main
cat review_findings.json
```

---

[[../_Index|← Back to Claude Code Configuration & Workflows Index]]
