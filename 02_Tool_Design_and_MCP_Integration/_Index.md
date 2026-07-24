---
tags: [hub, tools, mcp]
topic: "02 - Tool Design & MCP Integration"
---

# Domain 2 — Tool Design & MCP Integration

**18% of the exam.** Tests whether you can design tool interfaces Claude selects reliably, implement structured MCP error responses that let agents recover intelligently, distribute tools across multi-agent systems without degrading selection accuracy, wire MCP servers into Claude Code correctly, and choose the right built-in tool for a given job.

See [[../00_Exam_Guide/_Index|Exam Guide]] for the full official blueprint and [[../Home|Home]] for vault-wide navigation.

---

## Official Task Statements

1. **2.1 — Design effective tool interfaces with clear descriptions and boundaries.** Tool descriptions are the primary mechanism Claude uses for tool selection; vague or overlapping descriptions cause misrouting between similar tools.
2. **2.2 — Implement structured error responses for MCP tools.** The `isError` pattern: distinguishing transient, validation, business, and permission errors so agents can retry, correct, or escalate appropriately instead of treating every failure identically.
3. **2.3 — Distribute tools appropriately across agents and configure tool choice.** Too many tools (or tools outside an agent's specialization) degrade selection reliability; `tool_choice` (`auto` / `any` / forced) controls whether and how a tool call happens.
4. **2.4 — Integrate MCP servers into Claude Code and agent workflows.** Project-scoped `.mcp.json` vs. user-scoped `~/.claude.json`, environment variable expansion for credentials, and MCP resources for exposing content catalogs.
5. **2.5 — Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively.** Content search vs. path matching, targeted edits vs. full-file rewrites, and building codebase understanding incrementally.

---

## Theory Notes

1. [[Theory/01_Tool_Interface_Design|01 — Tool Interface Design]] — Task 2.1: description quality, splitting generic tools into purpose-specific ones, keyword-sensitivity pitfalls. Includes a quick recap of core `tool_use`/`tool_result` mechanics.
2. [[Theory/02_Error_Handling_and_Tool_Distribution|02 — Error Handling & Tool Distribution]] — Tasks 2.2 & 2.3: structured MCP error responses, local vs. propagated recovery, tool distribution across agents, `tool_choice` modes.
3. [[Theory/03_MCP_Servers_and_Builtin_Tools|03 — MCP Servers & Built-in Tools]] — Tasks 2.4 & 2.5: `.mcp.json` scoping, env var expansion, MCP resources, and Grep/Glob/Read/Write/Edit selection.

---

## Exercises

[[Exercises/Setup|Setup instructions]]

| # | File | Task | What it covers |
| - | ---- | ---- | --------------- |
| 1 | `01_tool_description_design.*` | 2.1 | Ambiguous vs. differentiated tool descriptions — before/after routing |
| 2 | `02_structured_errors.*` | 2.2 | MCP `isError` pattern, `errorCategory`/`isRetryable`, client-side recovery |
| 3 | `03_tool_choice_modes.*` | 2.3 | `tool_choice` forced / `auto` / `any` |

Available in Python, JavaScript, and TypeScript under `Exercises/`.

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 16 original scenario-based questions covering all five task statements.

---

## Key Concepts Checklist

- [ ] Explain why tool descriptions are the primary selection signal, and diagnose a misrouting bug caused by vague/overlapping descriptions
- [ ] Split a generic multi-mode tool into purpose-specific tools with clear input/output contracts
- [ ] Identify when a system prompt's keyword-triggered instruction — not the tool description — is the actual root cause of misrouting
- [ ] Write a structured MCP error response with `isError`, `errorCategory`, `isRetryable`, and a human-readable `message`
- [ ] Distinguish transient, validation, business, and permission errors, and match each to the correct recovery action
- [ ] Explain why local recovery for transient failures beats always propagating to the coordinator, and what a propagated error should carry
- [ ] Explain why giving a subagent too many tools, or tools outside its role, degrades reliability — and how a scoped cross-role tool (e.g. `verify_fact`) fixes the high-frequency case without over-provisioning
- [ ] Choose the correct `tool_choice` value (`auto`, `any`, forced) for a given requirement
- [ ] Configure a shared MCP server in project-level `.mcp.json` with `${VAR}` environment variable expansion, vs. a personal server in `~/.claude.json`
- [ ] Explain when an MCP resource (content catalog) is the right tool to reduce exploratory calls, instead of another tool
- [ ] Choose Grep vs. Glob vs. Read/Write vs. Edit for a given task, and know the Read+Write fallback when Edit's anchor isn't unique

---

[[../Home|Home]]
