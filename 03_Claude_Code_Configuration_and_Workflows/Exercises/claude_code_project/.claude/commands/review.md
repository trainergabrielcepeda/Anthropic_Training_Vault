---
description: Run the team's standard code review checklist against the current diff.
argument-hint: "[base-branch]"
---

# /review

Review the diff between the current branch and `$1` (default `main`) against this project's review checklist. This command lives in `.claude/commands/` (project-scoped, version-controlled) so it is available to every developer the moment they clone or pull — contrast with a personal shortcut in `~/.claude/commands/`, which would exist only on one developer's machine.

## Checklist

1. **Correctness** — does the diff do what the PR description claims? Trace at least one full request path if routes changed.
2. **Validation** — does every new/changed route validate input via the shared `zod` schemas (see `.claude/rules/api-conventions.md`)?
3. **Error handling** — are errors thrown as typed errors, not bare `Error`?
4. **Tests** — does test coverage match `.claude/rules/testing.md`? Flag missing failure-path cases specifically.
5. **Docs** — if a route was added or changed, is `docs/api-reference.md` updated in the same diff?
6. **Scope** — is anything in the diff unrelated to the stated purpose of the PR? Flag it rather than silently accepting scope creep.

Report findings as a short list grouped by severity (blocking / suggestion / nit). Do not modify any files — this command only reports.
