---
tags: [hub, claude-code, configuration, domain-3]
topic: "03 - Claude Code Configuration & Workflows"
---

# Domain 3 · Claude Code Configuration & Workflows — 20% of the exam

Domain 3 tests how you configure a **repository** — not the Claude API — for Claude Code: the CLAUDE.md hierarchy, modular rule files, custom commands and skills, plan mode vs. direct execution, iterative refinement technique, and CI/CD integration. See [[../00_Exam_Guide/_Index|Exam Guide]] for how this domain's weight and scenarios fit the overall exam, and [[../Home|Home]] for vault-wide navigation.

This domain is the primary lens for [[../00_Exam_Guide/Exam_Scenarios|Scenario 2 — Code Generation with Claude Code]] and [[../00_Exam_Guide/Exam_Scenarios|Scenario 5 — Claude Code for Continuous Integration]], and contributes to Scenario 4 — Developer Productivity with Claude.

---

## Task Statements

1. **3.1 — Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization.** User-level vs. project-level vs. directory-level CLAUDE.md; `@import` for modular standards; `/memory` for diagnosing what's actually loaded.
2. **3.2 — Create and configure custom slash commands and skills.** `.claude/commands/` (project, shared) vs. `~/.claude/commands/` (personal); `.claude/skills/` with `SKILL.md` frontmatter (`context: fork`, `allowed-tools`, `argument-hint`); when to reach for a skill vs. CLAUDE.md.
3. **3.3 — Apply path-specific rules for conditional convention loading.** `.claude/rules/` files with YAML frontmatter `paths` glob patterns; loading conventions only when relevant files are touched; glob rules vs. directory-level CLAUDE.md for conventions scattered across many directories.
4. **3.4 — Determine when to use plan mode vs. direct execution.** Plan mode for architecturally-implicated, multi-file, ambiguous work; direct execution for well-scoped single-file changes; the Explore subagent for isolating verbose discovery.
5. **3.5 — Apply iterative refinement techniques for progressive improvement.** Concrete input/output examples; test-driven iteration; the interview pattern; batching interacting issues vs. fixing independent ones sequentially.
6. **3.6 — Integrate Claude Code into CI/CD pipelines.** `-p`/`--print` for non-interactive runs; `--output-format json` + `--json-schema` for structured findings; CLAUDE.md as context for CI-invoked runs; independent review instances vs. self-review.

---

## Theory Notes

1. [[Theory/01_CLAUDE_md_and_Configuration|01 — CLAUDE.md & Path-Specific Rules]] — hierarchy, `@import`, `.claude/rules/`, glob-scoped path rules, `/memory` (Tasks 3.1, 3.3)
2. [[Theory/02_Commands_Skills_and_Plan_Mode|02 — Commands, Skills & Plan Mode]] — `.claude/commands/`, `.claude/skills/` frontmatter, plan mode vs. direct execution, the Explore subagent (Tasks 3.2, 3.4)
3. [[Theory/03_Iterative_Refinement_and_CICD|03 — Iterative Refinement & CI/CD]] — input/output examples, TDD iteration, the interview pattern, `-p`/`--output-format json`/`--json-schema`, CI review patterns (Tasks 3.5, 3.6)

---

## Exercises

[[Exercises/Setup|Setup instructions]] — read this first; this domain's exercises are repository configuration artifacts, not API scripts, so the layout differs from other domains.

| Folder | What it covers |
| ------ | --------------- |
| [[Exercises/claude_code_project/README\|Exercises/claude_code_project/]] | A sample repo: root `CLAUDE.md`, `.claude/rules/testing.md` + `api-conventions.md` (glob-scoped), `.claude/commands/review.md`, `.claude/skills/code-audit/SKILL.md`, `.mcp.json` with `${ENV_VAR}` expansion |
| [[Exercises/ci_cd/README\|Exercises/ci_cd/]] | `run_review.sh` — `claude -p "..." --output-format json --json-schema schema.json` for CI-integrated review, plus `schema.json` |

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 18 questions spanning all six task statements.

---

## Key Concepts Checklist

- [ ] Explain why a user-level `~/.claude/CLAUDE.md` convention won't reach a teammate who clones the repo
- [ ] Use `@import` to keep a CLAUDE.md modular across monorepo packages
- [ ] Split a large CLAUDE.md into focused `.claude/rules/` files
- [ ] Use `/memory` to diagnose why an expected instruction didn't apply
- [ ] Write a `.claude/rules/` file with `paths` glob frontmatter for conventions scattered across directories
- [ ] Explain when glob-scoped rules beat directory-level CLAUDE.md
- [ ] Create a project-scoped command in `.claude/commands/` vs. a personal one in `~/.claude/commands/`
- [ ] Configure a skill's `context: fork`, `allowed-tools`, and `argument-hint` frontmatter and explain what each buys you
- [ ] Choose plan mode vs. direct execution for a given task description
- [ ] Explain what the Explore subagent isolates and why
- [ ] Recognize when to provide concrete input/output examples vs. more prose
- [ ] Apply test-driven iteration and the interview pattern appropriately
- [ ] Decide whether to batch interacting issues or fix independent ones sequentially
- [ ] Run Claude Code in CI with `-p` and produce structured findings with `--output-format json` + `--json-schema`
- [ ] Explain why an independent review instance beats self-review of generated code

---

[[../00_Exam_Guide/_Index|← Exam Guide]] · [[../Home|Home]]
