---
name: code-audit
description: Run a structured audit of code quality, dead code, and architectural drift across the repo or a given directory. Use for periodic health checks, not for every commit.
context: fork
allowed-tools: [Read, Grep, Glob]
argument-hint: "[directory, default: whole repo]"
---

# Code Audit

This skill runs in an isolated sub-agent context (`context: fork`) because a full audit reads and greps across many files — output that would otherwise flood the main conversation. Only the final summary below comes back to the calling session.

`allowed-tools` is restricted to `[Read, Grep, Glob]` — this skill only inspects the codebase; it cannot edit or delete files, run shell commands, or otherwise take destructive action, even if the audit's own findings tempt it to "just fix this while I'm here."

## Steps

1. Scope the audit to `$1` if provided, otherwise the whole repo.
2. Grep for `TODO`, `FIXME`, and `HACK` markers; group by file and note how long each has existed (`git blame` the line).
3. Glob for source files over 500 lines that have no corresponding `*.test.ts(x)` file.
4. Identify dead exports: symbols exported from a module but never imported anywhere else in the repo.
5. Flag any file that imports from both `packages/api` and `packages/web` directly (a likely layering violation — shared code belongs in `packages/shared`).

## Output

Return one summary table: `finding | location | severity (blocking/worth-tracking/informational) | suggested owner`. Do not include full file contents or raw grep dumps in the summary — this skill exists specifically to keep that verbosity out of the main session.
