---
tags: [exam-guide, official, scenarios]
topic: "00 - Exam Guide"
source: "Claude Certified Architect – Foundations, Exam Guide v1.0, effective July 2026"
---

# The 6 Official Exam Scenarios

Every question on the real exam is anchored to one of these six scenarios. On exam day, **4 of the 6** are presented (picked at random), each seeding a cluster of questions that span 2–3 domains. Study these verbatim — they are the lens the exam guide itself uses to frame sample questions (see [[Official_Sample_Questions]]).

## Scenario 1 — Customer Support Resolution Agent

> You are building a customer support resolution agent using the Claude Agent SDK. The agent handles high-ambiguity requests like returns, billing disputes, and account issues. It has access to your backend systems through custom MCP tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`). Your target is 80%+ first-contact resolution while knowing when to escalate.

**Primary domains:** Agentic Architecture & Orchestration · Tool Design & MCP Integration · Context Management & Reliability

**What to have ready:** enforcement via hooks vs. prompt instructions for identity-verification-before-refund; tool description quality when two tools look alike; escalation calibration (explicit criteria + few-shot, not confidence scores or sentiment).

## Scenario 2 — Code Generation with Claude Code

> You are using Claude Code to accelerate software development — code generation, refactoring, debugging, documentation. You need custom slash commands, CLAUDE.md configuration, and to know when to use plan mode vs. direct execution.

**Primary domains:** Claude Code Configuration & Workflows · Context Management & Reliability

**What to have ready:** `.claude/commands/` (project) vs `~/.claude/commands/` (personal); `.claude/rules/` glob-scoped conventions vs. per-directory CLAUDE.md; plan mode for architectural/multi-file work vs. direct execution for well-scoped single-file changes.

## Scenario 3 — Multi-Agent Research System

> A coordinator agent delegates to specialized subagents — one searches the web, one analyzes documents, one synthesizes findings, one generates reports — to research topics and produce comprehensive, cited reports.

**Primary domains:** Agentic Architecture & Orchestration · Tool Design & MCP Integration · Context Management & Reliability

**What to have ready:** task decomposition breadth (narrow decomposition silently drops sub-topics); context passed explicitly to subagents (no automatic inheritance); claim-source mappings surviving synthesis; structured error propagation on subagent timeout.

## Scenario 4 — Developer Productivity with Claude

> An agent built on the Claude Agent SDK helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) plus MCP servers.

**Primary domains:** Tool Design & MCP Integration · Claude Code Configuration & Workflows · Agentic Architecture & Orchestration

**What to have ready:** Grep vs Glob vs Read/Write/Edit selection; incremental codebase understanding (Grep entry points → Read to trace); scratchpad files and subagent delegation to survive context degradation in long exploration sessions.

## Scenario 5 — Claude Code for Continuous Integration

> Claude Code is integrated into CI/CD: automated code review, test generation, and pull-request feedback. Prompts must give actionable feedback and minimize false positives.

**Primary domains:** Claude Code Configuration & Workflows · Prompt Engineering & Structured Output

**What to have ready:** `-p`/`--print` for non-interactive runs; `--output-format json` + `--json-schema` for machine-parseable PR comments; explicit review criteria over vague "be conservative" instructions; independent review instance vs. self-review of generated code.

## Scenario 6 — Structured Data Extraction

> Claude extracts information from unstructured documents, validates output against JSON schemas, maintains high accuracy, handles edge cases gracefully, and integrates with downstream systems.

**Primary domains:** Prompt Engineering & Structured Output · Context Management & Reliability

**What to have ready:** `tool_use` + JSON schema over free-text JSON; nullable/optional fields to stop fabrication; validation-retry-with-error-feedback vs. retries that can't work (info simply isn't in the source); Message Batches API tradeoffs (50% cheaper, ≤24h, no mid-request tool calls); confidence-calibrated human review routing.

---

[[Exam_Overview|← Exam Overview]] · [[Official_Sample_Questions|Official Sample Questions →]]
