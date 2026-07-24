---
tags: [theory, claude-code, configuration, claude-md]
topic: "03 - Claude Code Configuration & Workflows"
---

# CLAUDE.md & Path-Specific Rules

## What CLAUDE.md Is For

`CLAUDE.md` is memory that Claude Code loads automatically into context at the start of every session in a given directory tree. It is the mechanism for "always-loaded universal standards" — things Claude should know on every single task in this project, without you having to repeat them: build commands, architectural conventions, review standards, forbidden patterns.

It is **not** for task-specific, on-demand instructions — that's what [[02_Commands_Skills_and_Plan_Mode|commands and skills]] are for. Loading everything into CLAUDE.md wastes context on turns that don't need it.

---

## The CLAUDE.md Hierarchy

Claude Code merges memory from three levels, in this order:

| Level | Location | Scope | Shared with team? |
| ----- | -------- | ----- | ------------------ |
| User | `~/.claude/CLAUDE.md` | Every project you work on, on your machine | **No** — lives outside any repo, never committed |
| Project | `.claude/CLAUDE.md` or root `CLAUDE.md` | Everyone who clones the repo | **Yes** — version-controlled |
| Directory | `<subdir>/CLAUDE.md` | Only sessions working inside that subdirectory | Yes, if committed with the repo |

> [!warning] The most common hierarchy mistake
> A new teammate clones the repo, runs Claude Code, and doesn't get instructions you "know" it follows. The instructions are almost always sitting in **your** `~/.claude/CLAUDE.md` — a user-level file that was never in version control and therefore never reached them. If a convention matters for the whole team, it belongs in the project-level `CLAUDE.md` (or `.claude/rules/`), not your personal user-level file.

Directory-level `CLAUDE.md` files let a monorepo give different instructions per package — e.g. `packages/api/CLAUDE.md` documents REST conventions while `packages/frontend/CLAUDE.md` documents component conventions, and both inherit the root project file.

---

## Keeping CLAUDE.md Modular

A single giant `CLAUDE.md` becomes unmanageable as a project grows. Two mechanisms keep it modular:

### `@import` Syntax

`@import` references an external file so CLAUDE.md itself stays a thin index rather than a monolith:

```markdown
# Project Standards

@import .claude/standards/testing.md
@import .claude/standards/git-conventions.md
@import packages/api/CONVENTIONS.md
```

This is especially useful in monorepos, where each package can `@import` only the standards files relevant to it — the API package imports API conventions, not frontend styling rules — instead of every session loading every standard regardless of relevance.

### `.claude/rules/` Directory

As an alternative to one monolithic file, `.claude/rules/` lets you split standards into focused, topic-specific files that Claude Code loads alongside CLAUDE.md:

```
.claude/
  rules/
    testing.md
    api-conventions.md
    deployment.md
```

Each file owns one concern. This scales better than headers-within-one-file because it's easier to find, edit, and reason about in isolation — and, as covered below, rule files can be scoped to load **only** when relevant.

> [!tip] Modular index vs. one giant file
> If every rule always applies everywhere, plain `.claude/rules/*.md` files (always loaded) are enough. If conventions only apply to certain files or directories, add YAML frontmatter path scoping — see below.

---

## Path-Specific Rules (Glob-Scoped Loading)

`.claude/rules/` files can carry YAML frontmatter with a `paths` field containing glob patterns. When present, Claude Code loads that rule file **only** when the current task touches a matching file — not on every turn.

```markdown
---
paths: ["terraform/**/*"]
---

# Terraform Conventions

- All resources must have an `environment` tag.
- Use `for_each`, not `count`, for anything keyed by name.
- Run `terraform fmt` before every commit.
```

### Why glob rules beat directory-level CLAUDE.md for scattered conventions

Directory-level `CLAUDE.md` is bound to a directory tree — it works when a convention maps cleanly onto "everything under `packages/api/`." It breaks down when the convention instead maps onto a **file type that's scattered across the whole codebase** — e.g. every `*.test.tsx` file, regardless of which feature directory it lives in.

| Situation | Best mechanism |
| --------- | --------------- |
| Convention applies to everything under one directory tree | Directory-level `CLAUDE.md` |
| Convention applies to a file type/pattern scattered across many directories | `.claude/rules/*.md` with `paths` glob frontmatter |
| Convention always applies, everywhere, regardless of file | Project-level `CLAUDE.md` (or an always-loaded rule file) |

```markdown
---
paths: ["**/*.test.tsx", "**/*.test.ts"]
---

# Test File Conventions

- Use `describe`/`it`, not `test()`.
- Mock network calls with the shared `mockFetch` helper — never `jest.mock('node-fetch')` directly.
- Every test file must cover at least one failure-path case.
```

Because this rule is keyed on the glob `**/*.test.tsx`, it activates the moment Claude touches a matching file anywhere in the repo — `src/components/Button.test.tsx`, `src/routes/checkout/Checkout.test.tsx`, etc. — without needing a `CLAUDE.md` duplicated into every directory that happens to contain tests. It also keeps token usage down: a session editing `terraform/*` never loads the React test conventions, and vice versa.

---

## Diagnosing Memory Issues with `/memory`

When Claude Code behaves as if it never saw an instruction you're sure you wrote down, don't guess — run `/memory` to see exactly which memory files were loaded for the current session, in hierarchy order. This tells you immediately whether:

- the instruction is sitting in a user-level file that isn't shared with the team,
- a path-scoped rule simply didn't match the current file (glob typo, wrong directory),
- or the instruction was never actually written down anywhere.

> [!example] Diagnostic flow
> Teammate reports "Claude keeps using `fetch` instead of our `apiClient` wrapper." You run `/memory`. The project `CLAUDE.md` loaded fine, but the rule enforcing `apiClient` was in a file with `paths: ["src/api/**/*"]` — and the teammate was editing `src/routes/checkout.tsx`, outside that glob. Fix: either broaden the glob or move the instruction to project-level `CLAUDE.md` if it should really apply everywhere.

---

## Related Notes

- [[02_Commands_Skills_and_Plan_Mode|Commands, Skills & Plan Mode]]
- [[03_Iterative_Refinement_and_CICD|Iterative Refinement & CI/CD]]
- [[../Exercises/claude_code_project/README|Exercise: a sample project with CLAUDE.md + rules]]

---

[[../_Index|← Back to Claude Code Configuration & Workflows Index]]
