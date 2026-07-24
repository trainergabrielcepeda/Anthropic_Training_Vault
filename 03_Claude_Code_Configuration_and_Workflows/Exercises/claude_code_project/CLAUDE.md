# Project Standards — Orderflow API

This file is the project-level memory Claude Code loads for every session in this repo (committed, shared with the whole team — contrast with `~/.claude/CLAUDE.md`, which is personal and never committed).

## What this project is

A Node/TypeScript order-management API (`packages/api`) with a React frontend (`packages/web`). Both packages share a `packages/shared` types package.

## Universal standards (always apply, everywhere in this repo)

- Package manager is `pnpm`, not `npm` or `yarn`. Never generate `package-lock.json`.
- Commit messages: Conventional Commits (`feat:`, `fix:`, `chore:`, ...).
- Never commit `.env` files or anything under `secrets/`.
- All new backend endpoints require an entry in `docs/api-reference.md`.

## Modular standards — imported, not inlined

Keep this file a thin index. Package-specific and topic-specific conventions live in their own files and are pulled in with `@import` so each session only reasons about the standards relevant to what it's actually touching.

@import .claude/standards/git-conventions.md
@import packages/api/CONVENTIONS.md

## Path-scoped conventions

Testing conventions and API conventions are **not** confined to one directory (test files sit next to the code they test, scattered across `packages/api` and `packages/web`), so they live in glob-scoped `.claude/rules/` files instead of being duplicated into every directory's own `CLAUDE.md`:

- `.claude/rules/testing.md` — applies to `**/*.test.ts` and `**/*.test.tsx` wherever they are.
- `.claude/rules/api-conventions.md` — applies to everything under `packages/api/src/routes/**`.

See [[../Theory/01_CLAUDE_md_and_Configuration|CLAUDE.md & Path-Specific Rules]] for why glob-scoped rules are the right tool here instead of a `CLAUDE.md` per directory.

## If you're new here

Run `/memory` in a Claude Code session to see exactly which of these files loaded for your current task — the fastest way to confirm your session actually has the context you expect, and to catch cases where you assumed something was project-level but it was actually only ever in someone's personal `~/.claude/CLAUDE.md`.
