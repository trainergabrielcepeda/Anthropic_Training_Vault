# Exercise — A Sample Claude Code Project Configuration

This is not a runnable script — it is a small, realistic slice of a repository showing the actual configuration artifacts Claude Code reads. The "exercise" is to read each file, then try dropping this structure into a real repo and exercising it with the `claude` CLI (see [[../Setup|Exercises/Setup]] for exact steps).

## Files in this folder and what each demonstrates

| File | Demonstrates | Maps to |
| ---- | ------------- | ------- |
| `CLAUDE.md` | Project-level memory: universal standards, `@import` to keep the file thin, and a note on why testing/API conventions live in `.claude/rules/` instead of here | Task 3.1 |
| `.claude/rules/testing.md` | A glob-scoped rule (`paths: ["**/*.test.ts", "**/*.test.tsx"]`) that loads only when a matching test file is being touched, regardless of which directory it's in | Task 3.3 |
| `.claude/rules/api-conventions.md` | A glob-scoped rule (`paths: ["packages/api/src/routes/**/*", ...]`) that loads only for backend route files — frontend sessions never pay for this context | Task 3.3 |
| `.claude/commands/review.md` | A project-scoped custom slash command (`/review`), version-controlled and available to every teammate on clone — contrast with a personal command in `~/.claude/commands/` | Task 3.2 |
| `.claude/skills/code-audit/SKILL.md` | A skill with `context: fork` (isolates verbose audit output into a sub-agent), `allowed-tools` (restricted to read-only tools so the skill cannot take destructive action), and `argument-hint` (`[directory, default: whole repo]`) | Task 3.2 |
| `.mcp.json` | A project-scoped MCP server entry using `${DATABASE_URL}` environment-variable expansion, so the actual secret never lives in the committed file | Task 3.2 / cross-references [[../../../02_Tool_Design_and_MCP_Integration/_Index\|Tool Design & MCP Integration]] |

## How to actually exercise this (these files aren't "run")

Unlike the Python/JS/TS exercises in other domain folders, none of these files execute on their own — they're configuration that the `claude` CLI reads when you're working inside a real repo. To get hands-on:

1. **Copy this folder's contents into a scratch git repo** (or a throwaway branch of a real one):
   ```bash
   cp -r 03_Claude_Code_Configuration_and_Workflows/Exercises/claude_code_project/. /path/to/scratch-repo/
   cd /path/to/scratch-repo && git init -q   # if not already a repo
   ```
2. **Start Claude Code in that repo** and run `/memory` — confirm you see `CLAUDE.md` and both `.claude/rules/*.md` files listed as loaded (or not-yet-active, for the path-scoped ones — see step 4).
3. **Run the command**: type `/review main` and watch it apply the checklist from `.claude/commands/review.md`.
4. **Trigger a path-scoped rule**: create or open a file matching `**/*.test.ts` (e.g. `packages/api/src/orders.test.ts`) and ask Claude a question about it — then run `/memory` again and confirm `testing.md` is now active, where it wasn't for a non-matching file.
5. **Invoke the skill**: run the `code-audit` skill against a directory and notice the detailed grep/read activity happens in a forked sub-agent — your main conversation only receives the summary table.
6. **Inspect `.mcp.json`**: set a `DATABASE_URL` env var and start Claude Code — it should show the `orderflow-db` MCP server as available, with the URL expanded from your environment rather than hardcoded in the committed file.

None of this requires an Anthropic API key script — it requires the actual `claude` CLI and a directory it can treat as a project.
