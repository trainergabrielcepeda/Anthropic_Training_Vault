---
tags: [topic, agents, orchestration, agentic]
topic: "01 - Agentic Architecture & Orchestration"
---

# Domain 1 — Agentic Architecture & Orchestration

**Domain 1 · 27% of the exam** — the largest domain on the CCAR-F blueprint. It covers building an agentic loop from first principles, coordinating multiple agents in a hub-and-spoke architecture, enforcing deterministic behavior inside a probabilistic loop, choosing a task decomposition strategy, and managing session state across a long-running or multi-part piece of work.

See [[../00_Exam_Guide/_Index|Exam Guide]] for exam-wide format, scoring, and the official scenario bank this domain's questions are anchored to (primarily [[../00_Exam_Guide/Exam_Scenarios|Scenario 1 — Customer Support Resolution Agent]] and [[../00_Exam_Guide/Exam_Scenarios|Scenario 3 — Multi-Agent Research System]]).

---

## Task Statements

1. **1.1 — Design and implement agentic loops for autonomous task execution.** The `send request → inspect stop_reason → execute tools → return results` lifecycle; `tool_use` vs `end_turn`; avoiding text-parsing and iteration-cap-as-primary-stop anti-patterns.
2. **1.2 — Orchestrate multi-agent systems with coordinator-subagent patterns.** Hub-and-spoke architecture; the coordinator's decomposition/delegation/aggregation role; the narrow-decomposition risk.
3. **1.3 — Configure subagent invocation, context passing, and spawning.** The `Task` tool and `allowedTools`; explicit context passing (no automatic inheritance); `AgentDefinition`; parallel spawning; `fork_session`.
4. **1.4 — Implement multi-step workflows with enforcement and handoff patterns.** Programmatic prerequisite gates vs. prompt-based guidance; multi-concern decomposition; structured handoff summaries for human escalation.
5. **1.5 — Apply Agent SDK hooks for tool call interception and data normalization.** `PostToolUse` result normalization; `PreToolUse`-style outgoing call interception; hooks (deterministic) vs. prompts (probabilistic).
6. **1.6 — Design task decomposition strategies for complex workflows.** Fixed sequential pipelines (prompt chaining) vs. dynamic adaptive decomposition; per-file + cross-file review passes; mapping structure before planning open-ended work.
7. **1.7 — Manage session state, resumption, and forking.** Named `--resume`; `fork_session` for divergent exploration from a shared baseline; informing a resumed session about file changes; resuming vs. a fresh session with an injected summary.

---

## Theory Notes

1. [[Theory/01_Agentic_Loops_and_Tool_Execution|01 — Agentic Loops & Tool Execution]] — Task 1.1: the loop lifecycle, `stop_reason`, and the three anti-patterns the exam rejects.
2. [[Theory/02_Multi_Agent_Orchestration|02 — Multi-Agent Orchestration]] — Tasks 1.2 & 1.3: hub-and-spoke, isolated subagent context, the `Task` tool, `AgentDefinition`, and parallel spawning.
3. [[Theory/03_Workflow_Control_and_Session_Management|03 — Workflow Control & Session Management]] — Tasks 1.4–1.7: enforcement and handoffs, Agent SDK hooks, decomposition strategy selection, and session resumption/forking.

---

## Exercises

[[Exercises/Setup|Setup instructions]]

| Language | File | What it covers |
| -------- | ---- | -------------- |
| Python | `Exercises/python/01_agentic_loop.py` | Agentic loop keyed off `stop_reason`, with a safety-net (not primary) iteration cap |
| Python | `Exercises/python/02_coordinator_subagents.py` | Coordinator dispatching to parallel, context-isolated subagents; synthesis + gap re-delegation |
| Python | `Exercises/python/03_hook_interception.py` | `PreToolUse`-style blocking + `PostToolUse`-style result normalization |
| JavaScript | `Exercises/javascript/01_agentic_loop.js` · `02_coordinator_subagents.js` · `03_hook_interception.js` | Same three exercises in Node.js |
| TypeScript | `Exercises/typescript/01_agentic_loop.ts` · `02_coordinator_subagents.ts` · `03_hook_interception.ts` | Same three exercises, strongly typed |

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 18 questions covering all 7 task statements, framed through the Customer Support Resolution Agent, Multi-Agent Research System, and Developer Productivity scenarios.

---

## Key Concepts Checklist

- [ ] State the four-step agentic loop lifecycle and identify `stop_reason` as the only valid control-flow signal
- [ ] Name the three loop anti-patterns the exam rejects: text-parsing for completion, iteration-cap-as-primary-stop, and text-content-as-completion-indicator
- [ ] Explain hub-and-spoke coordination and why all subagent communication routes through the coordinator
- [ ] Explain why subagents don't automatically inherit the coordinator's context, and how explicit context passing fixes that
- [ ] Describe the `Task` tool / `allowedTools` / `AgentDefinition` mechanism for spawning and configuring subagents
- [ ] Explain how to spawn subagents in true parallel (multiple `Task` calls in one coordinator turn) vs. accidentally serializing them
- [ ] Distinguish programmatic enforcement (hooks, prerequisite gates) from prompt-based guidance, and know when each is appropriate
- [ ] Explain `PostToolUse` normalization vs. `PreToolUse`-style interception, and why hooks give deterministic guarantees prompts cannot
- [ ] Choose between prompt chaining and dynamic adaptive decomposition for a given task shape
- [ ] Explain `--resume`, `fork_session`, and when a fresh session with an injected summary beats resuming a stale one

---

[[../00_Exam_Guide/_Index|← Exam Guide]] · [[../Home|Home]]
