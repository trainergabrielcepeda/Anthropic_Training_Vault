---
tags: [theory, tools, mcp, errors, multi-agent]
topic: "02 - Tool Design & MCP Integration"
task: "2.2, 2.3"
---

# Error Handling & Tool Distribution

> [!important] Exam Tasks 2.2 & 2.3
> 2.2 — Implement structured error responses for MCP tools.
> 2.3 — Distribute tools appropriately across agents and configure tool choice.

These two tasks are grouped because they share a theme: giving an agent (or the agent evaluating a tool's result) enough **structured information** to make a good decision, instead of forcing it to guess from an undifferentiated signal — a flat error string in 2.2, an overloaded tool list in 2.3.

---

## Part 1 — Structured MCP Error Responses

### The Problem With Uniform Failure Messages

A tool that returns `"Operation failed"` for every kind of failure gives the calling agent nothing to act on. A timeout, a malformed argument, and a denied permission are three completely different situations requiring three different responses — retry, correct-and-retry, and escalate-without-retrying, respectively. Collapsing them into one string forces the agent to either guess or always take the same (usually wrong) action.

### The `isError` Pattern

MCP tools communicate failure via an `isError` flag on the result, alongside structured metadata describing *what kind* of failure occurred:

```json
{
  "isError": true,
  "errorCategory": "transient",
  "isRetryable": true,
  "message": "Payment service timed out after 10s. Safe to retry."
}
```

| `errorCategory` | Meaning | Typically `isRetryable`? |
| --------------- | ------- | ------------------------- |
| `transient` | Timeout, service unavailable, rate limit | Usually `true` |
| `validation` | Invalid input (bad format, missing field, out-of-range value) | `false` — retrying with the *same* input never helps; the caller must supply different input |
| `business` | A policy or business rule blocked the action (e.g. refund exceeds approval limit) | `false` — no input change fixes this; it needs escalation or a different action |
| `permission` | The caller isn't authorized for this action on this resource | `false` — needs escalation, not retry |

> [!warning] Don't conflate "no results" with "the call failed"
> A successful query that legitimately finds nothing (e.g. `lookup_order` on an order ID that doesn't exist) is **not** an error — it's a valid, empty result. Marking it `isError: true` forces unnecessary retry logic on the caller; marking a real access failure as a *plain success with an empty payload* hides a problem the caller needed to know about. Keep these two states clearly distinct in what you return.

### Why `isRetryable` Matters

Without an explicit retryable/non-retryable signal, the calling agent (or your own orchestration code) has to infer retry-worthiness from the error category alone, which is error-prone for edge cases. Returning `isRetryable` explicitly:

- Lets an agent retry a `transient` failure immediately, without burning a turn asking "should I retry?"
- Prevents **wasted retries** against a `business` or `validation` failure that will never succeed no matter how many times it's attempted
- Gives orchestration code a single boolean to branch on, independent of which specific category caused the failure

```json
{
  "isError": true,
  "errorCategory": "business",
  "isRetryable": false,
  "message": "Refunds over $500 require manager approval and cannot be processed automatically. Escalate to a human agent."
}
```

Note the `message` here is written for a human/customer-facing context, not a stack trace — for `business` errors especially, the message often needs to be presentable as-is to the end user or a human reviewer.

### Local Recovery vs. Propagation

In a multi-agent system, a subagent that hits a **transient** failure should generally attempt local recovery — retry once or twice with backoff — *inside its own execution*, without bothering the coordinator. Only an error that the subagent cannot resolve locally should propagate upward, and when it does, it should carry:

- **What kind of failure occurred** (the error category)
- **What was already attempted** (e.g. "retried twice with backoff")
- **Any partial results already gathered**, if the task was partway done

```json
{
  "isError": true,
  "errorCategory": "transient",
  "isRetryable": false,
  "message": "Search API unreachable after 2 retries.",
  "attempted": ["query: 'AI creative industries 2026'", "retry 1", "retry 2"],
  "partialResults": ["3 articles found before failure"]
}
```

> [!example] Why structured propagation beats the alternatives
> Silently returning an empty result marked "successful" hides the failure entirely. Propagating every raw exception straight to a top-level handler that kills the whole workflow is an overreaction when partial results could still be salvaged. Structured context lets the coordinator make an *intelligent* recovery decision — retry elsewhere, proceed with partial results, or escalate — instead of guessing.

---

## Part 2 — Distributing Tools Across Agents

### Too Many Tools Degrades Selection Reliability

Giving one agent 18 tools "so it can handle anything" does not make it more capable — it makes tool selection harder. Every additional tool in the list is another option Claude has to correctly rule out on every single turn. Empirically, tool-selection reliability degrades noticeably once an agent's tool count grows well past what its role actually needs; a subagent that only ever needs 4-5 tools for its job should not be handed 18.

### Tools Outside a Role Get Misused

A subagent given tools **outside its specialization** doesn't just have unused capability sitting idle — it tends to actually use it, in ways that undermine the system's design. A synthesis subagent whose job is to combine already-gathered findings into a report, if given general web-search access "just in case," will sometimes run its own speculative searches mid-synthesis — introducing unverified content that never went through the research pipeline's normal sourcing/citation path.

> [!warning] Scope tools to role, not to "what might be useful"
> The fix for the synthesis-agent-searching-the-web problem is not a system-prompt instruction asking it not to ("don't use web search unless necessary") — prompt-level discouragement is probabilistic, not a guarantee. The fix is not giving it that tool in the first place.

### Scoped Cross-Role Tools for High-Frequency Needs

Least-privilege doesn't mean zero cross-role access ever. If a synthesis agent frequently (say, 85% of the time) needs to verify a simple fact — a date, a name, a number — while combining findings, round-tripping every single verification through the coordinator to a dedicated search agent and back adds latency for no real benefit on the easy cases.

The scoped fix: give the synthesis agent a narrow, purpose-built tool for exactly that high-frequency need (e.g. `verify_fact(claim)` — a lightweight lookup, not general web search), and keep routing the harder 15% of cases (deep, multi-source investigation) through the coordinator as before.

| Approach | Outcome |
| -------- | ------- |
| Full web-search access for synthesis | Over-provisioned; breaks separation of concerns; introduces unsourced content |
| Everything through the coordinator | Correct but slow — blocking round trips even for trivial lookups |
| Scoped `verify_fact` tool + coordinator for complex cases | Fast path for the common case, correct escalation path for the rare case |

### `tool_choice` Modes

| Value | Behavior | Use case |
| ----- | -------- | -------- |
| `{"type": "auto"}` | Claude decides whether and which tool to call (default) | Normal conversational/agentic turns |
| `{"type": "any"}` | Claude must call *some* tool, but chooses which one | Guarantee a tool call happens rather than a conversational text reply, without dictating which of several tools applies |
| `{"type": "tool", "name": "..."}` | Claude must call this exact tool | Force a specific step to run — e.g. guarantee `extract_metadata` runs before any enrichment tool, regardless of what Claude might otherwise pick |

**Forced tool_choice for pipeline ordering:** if a workflow requires `extract_metadata` to run before `translate_text` or `classify_topic` can meaningfully operate on a document, force it explicitly on the first turn:

```python
response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=300,
    tools=tools,
    tool_choice={"type": "tool", "name": "extract_metadata"},
    messages=messages,
)
```

Once the forced tool's result is back in the conversation, switch subsequent turns to `{"type": "auto"}` so Claude can freely choose the next appropriate step from the remaining tools.

**`"any"` for guaranteed-but-unspecified tool calls:** useful when you need *a* structured action to come back — any one of several valid tools — rather than risk a plain-text response that your pipeline can't parse.

---

## Related Notes

- [[01_Tool_Interface_Design|Tool Interface Design]]
- [[03_MCP_Servers_and_Builtin_Tools|MCP Servers & Built-in Tools]]
- [[../../01_Agentic_Architecture_and_Orchestration/Theory/02_Multi_Agent_Orchestration|Multi-Agent Orchestration — least privilege and trust boundaries]]
- [[../../00_Exam_Guide/Official_Sample_Questions|Official Sample Questions — Q8 and Q9 walk through these exact scenarios]]

---

[[../_Index|← Back to Domain 2 Index]]
