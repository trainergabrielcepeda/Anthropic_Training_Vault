---
tags: [theory, claude-code, commands, skills, plan-mode]
topic: "03 - Claude Code Configuration & Workflows"
---

# Commands, Skills & Plan Mode

## Custom Slash Commands

A slash command is a saved prompt template, invoked as `/command-name`, optionally taking arguments.

| Location | Scope | Shared with team? |
| -------- | ----- | ------------------ |
| `.claude/commands/` | Project | **Yes** — version-controlled, available to every developer on clone/pull |
| `~/.claude/commands/` | User (personal) | **No** — exists only on your machine |

> [!example] A team-wide `/review` command
> `.claude/commands/review.md` containing your team's review checklist, committed to the repo. The moment a teammate clones the project, `/review` exists for them too — no setup step, no "did you get the email with the checklist" problem. This is the correct home for anything the *team* should share; `~/.claude/commands/` is for personal shortcuts that shouldn't leak into anyone else's session.

Commands are the right tool for **on-demand, task-specific** prompts — invoked when you need them, not loaded into every turn the way CLAUDE.md is. See the CLAUDE.md-vs-skills-vs-commands decision guide at the bottom of this note.

---

## Skills

A skill is a packaged capability under `.claude/skills/<name>/SKILL.md`. Where a slash command is a short prompt template, a skill can bundle instructions, scripts, and reference material, and carries richer frontmatter controlling how it runs.

```markdown
---
name: code-audit
description: Run a structured audit of code quality, dead code, and architectural drift across the repo. Use for periodic health checks, not for every commit.
context: fork
allowed-tools: [Read, Grep, Glob]
argument-hint: "[directory]"
---

# Code Audit

1. Grep for TODO/FIXME/HACK markers and count by age (git blame).
2. Identify files exceeding 500 lines with no corresponding test file.
3. Report dead exports (defined, never imported).

Produce a single summary table. Do not modify any files.
```

### Frontmatter fields worth knowing

| Field | Purpose |
| ----- | ------- |
| `context: fork` | Runs the skill in an **isolated sub-agent context** rather than the main conversation. The skill can explore, grep, and reason at length without any of that intermediate output polluting your main session — only the final result comes back. |
| `allowed-tools` | Restricts which tools the skill may use during execution — e.g. limiting a documentation-generation skill to file-write tools only, so it structurally cannot run arbitrary shell commands or delete files. |
| `argument-hint` | Shown to the user/Claude as a hint for what argument the skill expects (e.g. `[directory]`, `[pr-number]`), prompting for required parameters instead of guessing. |

> [!tip] Why `context: fork` matters
> Skills that produce verbose output — full codebase analysis, open-ended brainstorming, exhaustive dependency traversal — are exactly the ones that will flood your main conversation's context if run inline. `context: fork` routes that verbosity into a sub-agent, which returns only a distilled summary. Without it, a single "analyze the whole codebase" skill invocation can consume most of your remaining context budget.

> [!tip] Why `allowed-tools` matters
> A skill meant only to *propose* changes (write a report, draft a migration plan) shouldn't have `Bash` access — restricting `allowed-tools` to `[Read, Write, Grep, Glob]` makes destructive actions structurally impossible, not just discouraged by prose instructions.

### Personal skill customization

Like commands, skills can be personal: `~/.claude/skills/<name>/SKILL.md` under a **different name** from any project skill lets you customize your own workflow without changing what teammates get from the project-scoped version. Reusing the same name in your user-level directory to *override* a project skill is possible but affects only your own sessions — it never touches the shared, committed one.

---

## Skills vs. CLAUDE.md

| | CLAUDE.md | Skills |
| - | --------- | ------ |
| Loaded | Always, every session | On-demand, when invoked |
| Best for | Universal standards true on every task (build commands, forbidden patterns, architecture) | Task-specific procedures used occasionally (an audit, a migration helper, a report generator) |
| Context cost | Paid on every turn | Paid only when used (and can be isolated via `context: fork`) |

If you find yourself writing an elaborate "how to do X" procedure into CLAUDE.md that only applies to one occasional task, it's usually a skill, not a memory file.

---

## Plan Mode vs. Direct Execution

### Direct execution

Just do the change. Right for well-scoped, well-understood work: a single-file bug fix with a clear stack trace, adding one validation check to one function, a one-line config change. There's one obviously correct approach and no ambiguity worth pausing to resolve.

### Plan mode

Explore and design a plan **before** touching any files, then get it reviewed/approved before execution begins. Right for:

- Large-scale, multi-file changes (a library migration touching 45+ files)
- Multiple valid approaches that trade off differently (which integration pattern, which infra requirements)
- Architectural decisions (service boundaries in a monolith-to-microservices split)

Plan mode exists to let you catch a wrong direction **before** it's been implemented across dozens of files — the cost of discovering a bad approach during planning is a rewritten plan; the cost of discovering it after implementation is a rewritten codebase.

> [!example] Same underlying task, different mode
> "Add a null check to `parseOrderId`" → direct execution. "Migrate the whole codebase off the deprecated `parseOrderId` in favor of the new validated `OrderId` type" → plan mode, because it touches many call sites, may reveal call sites with different validation needs, and the migration strategy itself (big-bang vs. incremental with a compatibility shim) is a real architectural choice.

### Combining the two

A common pattern: use plan mode for the **investigation** phase of a task, then drop to direct execution for implementation once the plan is settled and approved. Plan mode isn't an all-or-nothing mode for the whole session — it's a phase you enter for the parts of a task that carry real design risk.

---

## The Explore Subagent

Discovery work — "where is X defined," "how does this legacy module handle Y," "which files reference this deprecated function" — tends to generate a lot of intermediate output: file listings, grep hits, partial reads. Doing this directly in the main conversation burns context on exploration that the user (and the eventual implementation step) doesn't need to see in full.

The Explore subagent runs this discovery work in an isolated context and returns a **summary** — not the raw transcript of every file it opened. This is the same "isolate the noisy part" principle behind `context: fork` for skills, applied to ad hoc codebase exploration rather than a packaged skill.

> [!warning] Context exhaustion in long exploration sessions
> A single long session that reads dozens of files directly, in-line, degrades — earlier context gets crowded out or effectively ignored. Delegating verbose discovery to the Explore subagent (or to a forked skill) keeps the main conversation focused on decisions and results, not raw search output.

---

## Related Notes

- [[01_CLAUDE_md_and_Configuration|CLAUDE.md & Path-Specific Rules]]
- [[03_Iterative_Refinement_and_CICD|Iterative Refinement & CI/CD]]
- [[../Exercises/claude_code_project/README|Exercise: `.claude/commands/review.md` and `.claude/skills/code-audit/SKILL.md`]]

---

[[../_Index|← Back to Claude Code Configuration & Workflows Index]]
