---
tags: [theory, agents, hooks, enforcement, decomposition, sessions]
topic: "01 - Agentic Architecture & Orchestration"
---

# Workflow Control & Session Management

> [!important] Maps to Tasks 1.4, 1.5, 1.6, and 1.7
> **1.4 — Implement multi-step workflows with enforcement and handoff patterns.** **1.5 — Apply Agent SDK hooks for tool call interception and data normalization.** **1.6 — Design task decomposition strategies for complex workflows.** **1.7 — Manage session state, resumption, and forking.** These four task statements share a theme: making an otherwise probabilistic agent loop behave *deterministically* where it must, and structuring long-running or multi-part work so it stays reliable.

---

## Task 1.4 — Enforcement and Handoff Patterns

### Programmatic enforcement vs. prompt-based guidance

A system prompt instruction ("always verify identity before processing a refund") is **guidance**, not a guarantee. Prompt instructions have a non-zero failure rate — the model can skip a step under ambiguous phrasing, a long context, or an unusual input, and nothing in the architecture prevents it. For anything requiring **deterministic compliance** — identity verification before a financial operation is the canonical example — the fix is a **programmatic gate**, not a better-worded prompt.

> [!warning] The exam's most repeated pattern
> Whenever a question describes a reliability failure with real-world consequences (misidentified accounts, incorrect refunds, unauthorized actions) and offers "improve the system prompt" / "add few-shot examples" as an option alongside "add a programmatic prerequisite," the programmatic option is the answer. Prompt-based fixes reduce the failure rate; they do not eliminate it. See [[../../00_Exam_Guide/Official_Sample_Questions|Official Sample Questions]] Q1 for the exact shape of this question.

### Programmatic prerequisite gates

A prerequisite gate blocks a downstream tool call from executing at all until an upstream tool has returned a qualifying result — regardless of what the model *intends* to do next.

```python
# Illustrative prerequisite gate in a manual agentic loop
verified_customer_id = None

def execute_tool(name: str, tool_input: dict) -> str:
    global verified_customer_id

    if name == "get_customer":
        result = backend.get_customer(tool_input["identifier"])
        if result.get("verified"):
            verified_customer_id = result["customer_id"]
        return result

    if name in ("process_refund", "lookup_order"):
        if verified_customer_id is None:
            # Blocked programmatically — the model's request is refused
            # before it ever reaches the backend, no matter what it argued.
            return {
                "is_error": True,
                "content": "Blocked: call get_customer and obtain a verified "
                            "customer_id before process_refund or lookup_order.",
            }
        return backend.dispatch(name, tool_input, customer_id=verified_customer_id)

    return backend.dispatch(name, tool_input)
```

This is the same idea the Claude Agent SDK implements as a `PreToolUse` hook (see Task 1.5, below) — the gate lives in code your harness runs *before* the tool executes, not in text the model is asked to obey.

### Multi-concern requests: decompose, investigate in parallel, synthesize

When a single user request bundles multiple distinct concerns (e.g., a support ticket that raises a billing question *and* a shipping problem *and* a feature complaint), the reliable pattern is:

1. **Decompose** the request into distinct, independently-resolvable items.
2. **Investigate each in parallel**, with shared context (each investigation should know about the others, so the final resolution reads as one coherent response rather than three disconnected answers).
3. **Synthesize** a single unified resolution rather than returning three separate answers stapled together.

### Structured handoff summaries for human escalation

When an agent escalates to a human, that human usually has **no access to the full transcript** — they need a compact, structured summary, not a request to "go read the conversation." A well-formed handoff includes:

- **Customer/context details** — who, what account, what's already been verified
- **Root-cause analysis** — what the agent determined is actually wrong, not just the symptom the user reported
- **Recommended action(s)** — what the agent believes should happen next, and why it couldn't do it directly (policy gap, needs judgment, exceeds autonomous authority)

> [!example] Bad vs. good handoff
> Bad: *"Customer is upset, please help."*
> Good: *"Customer #A1029 (verified via get_customer). Order #58213 arrived damaged (photo evidence attached, ticket #9931). Standard replacement policy doesn't cover this SKU because it's marked final-sale — this is a policy gap, not a customer error. Recommend a one-time exception replacement; I don't have authority to override the final-sale flag."*

---

## Task 1.5 — Agent SDK Hooks: Interception and Normalization

Hooks are how the Claude Agent SDK gives you **deterministic guarantees** inside an otherwise model-driven loop — the same enforcement principle as Task 1.4's prerequisite gates, formalized as a first-class SDK mechanism.

### Two hook directions

| Hook point | Intercepts | Typical use |
| --- | --- | --- |
| **Outgoing tool call** (before execution — `PreToolUse`) | The tool Claude is *about* to call, with its inputs | Enforce compliance rules: block the call, redirect to an alternative, or require confirmation |
| **`PostToolUse`** (after execution, before the model sees the result) | The tool's RESULT | Transform/normalize the data before it enters the model's context |

### `PostToolUse`: normalizing heterogeneous data

Different MCP tools — often backed by different systems — return the same *kind* of data in different *shapes*. A `PostToolUse` hook is where you normalize before the model ever has to reason about the inconsistency:

```python
# Illustrative PostToolUse-style normalization hook
from datetime import datetime, timezone

def normalize_tool_result(tool_name: str, raw_result: dict) -> dict:
    """Runs after tool execution, before the result is appended to context.
    Different MCP tools return dates and statuses in different formats —
    normalize here so the model reasons over one consistent shape."""
    result = dict(raw_result)

    # Unix timestamp -> ISO 8601
    if isinstance(result.get("timestamp"), (int, float)):
        result["timestamp"] = datetime.fromtimestamp(
            result["timestamp"], tz=timezone.utc
        ).isoformat()

    # Numeric status code -> human-readable label
    status_map = {200: "success", 404: "not_found", 409: "conflict", 500: "error"}
    if isinstance(result.get("status"), int):
        result["status"] = status_map.get(result["status"], f"unknown_status_{result['status']}")

    return result
```

Without this, the model is left to reason about `"order_date": 1732492800` from one tool and `"order_date": "2024-11-24T00:00:00Z"` from another — the same field, two encodings, more opportunity for a misread.

### Intercepting outgoing tool calls: blocking policy violations

A tool-call interception hook inspects the pending call **before** it executes and can block it outright — this is where "refunds over $500 require human approval" becomes an enforced rule instead of a suggestion:

```python
# Illustrative PreToolUse-style interception hook
def enforce_refund_policy(tool_name: str, tool_input: dict) -> dict | None:
    """Runs before the tool executes. Returning a block response prevents
    execution entirely and can redirect the model toward an alternative."""
    if tool_name == "process_refund" and tool_input.get("amount", 0) > 500:
        return {
            "blocked": True,
            "reason": (
                "Refunds over $500 require human approval. "
                "Call escalate_to_human with the refund details instead."
            ),
        }
    return None  # not blocked — proceed normally
```

### Hooks vs. prompts: choosing deterministic over probabilistic

> [!tip] The rule of thumb
> If a business rule **must** hold every single time (a compliance threshold, an identity check, a data format the downstream system requires), implement it as a hook. If it's a *preference* that improves quality but tolerates occasional misses (tone, verbosity, which tool to prefer when two are roughly equivalent), a prompt instruction is appropriate and a hook would be overkill. The exam consistently rewards recognizing which category a given requirement falls into.

---

## Task 1.6 — Task Decomposition Strategies

Two decomposition strategies solve different problems. Picking the wrong one for the situation is a recurring wrong-answer pattern.

### Fixed sequential pipelines (prompt chaining)

Prompt chaining breaks a **predictable, multi-aspect** task into a fixed sequence of steps, where each step's output feeds the next. This works well when you already know the shape of the work in advance.

> [!example] Code review: per-file pass, then cross-file integration pass
> Reviewing a 14-file pull request in a single pass causes **attention dilution** — inconsistent depth across files, and the same pattern flagged as a bug in one file but missed in another. The fix is to chain two fixed steps: (1) a **local pass per file**, analyzing each file independently for issues contained within it, then (2) a **separate cross-file integration pass** that looks specifically for consistency issues, duplicated logic, and interactions between the files. This is a fixed pipeline — you know in advance that "per-file, then integration" is the right shape for *any* multi-file review. See [[../../00_Exam_Guide/Official_Sample_Questions|Official Sample Questions]] Q12.

### Dynamic, adaptive decomposition

Adaptive decomposition generates subtasks **based on what's discovered at each step** — appropriate for open-ended investigation where you don't know the shape of the work until you're partway into it.

> [!example] "Add comprehensive tests to a legacy codebase"
> You cannot write a fixed pipeline for this in advance — you don't yet know what the codebase looks like. The adaptive approach: (1) **map the structure first** (what modules exist, what's already tested), (2) **identify high-impact areas** from that map (untested code on critical paths, historically bug-prone modules), (3) **build an adaptive, prioritized plan** from those findings — and revise the plan as testing surfaces more information (e.g., discovering an untested module has its own undocumented dependencies).

### Choosing between them

| Signal | Use |
| --- | --- |
| You can fully specify the steps before starting | Prompt chaining (fixed sequential pipeline) |
| The task is predictable but touches many similar units (files, records, tickets) | Prompt chaining — one pass per unit, then an integration pass |
| The right next step depends on what the previous step found | Dynamic/adaptive decomposition |
| The task is open-ended ("investigate X," "improve Y") | Dynamic/adaptive decomposition |

---

## Task 1.7 — Session State, Resumption, and Forking

### Named session resumption

Claude Code (and Agent SDK sessions built the same way) support resuming a prior session by name: `--resume <session-name>`. This restores the prior conversation history so work can continue across separate CLI invocations or work sessions, without re-explaining everything from scratch.

### `fork_session`: independent branches from a shared baseline

`fork_session` starts an **independent branch** from an existing session's state — subsequent work in the fork does not affect the original session, and vice versa. This is the right tool for **parallel exploration**: e.g., comparing two different refactoring approaches, both starting from the same already-completed codebase analysis, without one approach's changes contaminating the other's starting point.

```
Shared baseline session (codebase analyzed)
        │
        ├── fork_session → Branch A: refactor using the Strategy pattern
        └── fork_session → Branch B: refactor using composition + hooks
```

### Resuming after code changes: tell the agent what changed

If files have changed since a session was created — whether by you, another engineer, or a previous agent run — **inform the resumed session about the specific changes** rather than assuming it will notice. A resumed session's tool-result history reflects the file state *at the time those tools ran*, not the current state. Telling it exactly what changed (which files, roughly what changed) lets it do **targeted re-analysis** of just the affected area, instead of either working from stale assumptions or being forced into a full, expensive re-exploration of the whole codebase.

### Resuming vs. starting fresh with an injected summary

> [!warning] When resuming is the wrong call
> Resuming a stale session replays old tool results as if they were still current — if a lot has changed, or the session's tool-call history is large and mostly irrelevant now, resuming can actively mislead the agent by anchoring it to outdated context. In that situation, **starting a new session with a structured summary of what's relevant now** is often more reliable than resuming: you control exactly what context enters the new session, instead of inheriting an entire prior transcript's worth of assumptions.

| Situation | Prefer |
| --- | --- |
| Prior context is still mostly valid; picking up where you left off | `--resume <session-name>` |
| Comparing divergent approaches from one shared starting point | `fork_session` |
| Prior tool results are stale (files changed significantly, a lot of time has passed) | New session + injected structured summary |
| Resuming, but specific files changed since last run | `--resume`, plus explicitly tell the agent which files changed |

## Related Notes

- [[01_Agentic_Loops_and_Tool_Execution|Agentic Loops & Tool Execution]] — the loop-level mechanics these controls sit on top of
- [[02_Multi_Agent_Orchestration|Multi-Agent Orchestration]] — coordinator-subagent patterns that also rely on structured handoffs and explicit context
- [[../../03_Claude_Code_Configuration_and_Workflows/_Index|Claude Code Configuration & Workflows]] — CLI-level session flags and configuration
- [[../../05_Context_Management_and_Reliability/_Index|Context Management & Reliability]] — deeper treatment of escalation criteria and error propagation
- [[../../00_Exam_Guide/Exam_Scenarios|Exam Scenarios]] — Scenario 1 (Customer Support) for 1.4/1.5, Scenario 4 (Developer Productivity) for 1.6/1.7

---

[[../_Index|← Back to Domain 1 Index]]
