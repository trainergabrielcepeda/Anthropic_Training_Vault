---
tags: [theory, error-handling, multi-agent, codebase-exploration, reliability]
topic: "05 - Context Management & Reliability"
---

# Error Propagation & Codebase Context

Two reliability problems share a root cause: information that exists at the point of failure gets thrown away before it reaches whoever could act on it. In multi-agent systems, that's a subagent's error detail disappearing before it reaches the coordinator. In long codebase-exploration sessions, that's earlier findings degrading or vanishing as context fills up. Both are solved the same way — by deliberately persisting and structuring information instead of trusting it to survive by default.

---

## Structured Error Context Enables Intelligent Recovery

When a subagent's tool call or sub-task fails, what it returns to the coordinator determines whether the coordinator can make a good decision. A generic status string throws away everything the coordinator would need.

> [!warning] "Search unavailable" tells the coordinator nothing
> Was it a timeout that a retry might fix? Was the query malformed? Did the source genuinely have no matching data? A generic error status collapses all of these into one undifferentiated failure, forcing the coordinator to either blindly retry, blindly give up, or blindly proceed as if nothing happened — none of which is a real decision.

Instead, a failing subagent should return **structured error context**:

```json
{
  "status": "error",
  "failure_type": "timeout",
  "attempted_query": "AI adoption in film production, 2024-2026",
  "partial_results": [
    {"source": "trade-press-article-1", "excerpt": "..."}
  ],
  "alternative_approaches": [
    "retry with a narrower date range",
    "fall back to a cached index if available"
  ]
}
```

With this, the coordinator can make an *informed* recovery choice: retry (transient timeout), proceed with partial results annotated as incomplete, or try the suggested alternative — instead of guessing.

### Access Failures vs. Valid Empty Results

These are different events and must be reported differently:

| Situation | What happened | Correct signal |
| --- | --- | --- |
| Access failure | Timeout, auth error, source unreachable | Error with failure type — retry may help |
| Valid empty result | Query executed successfully; genuinely no matches | Success, with an empty result set |

Collapsing these into the same "no results" signal is a common bug: a coordinator that can't tell "the search failed" from "the search succeeded and found nothing" will either retry a query that was never going to return anything (waste) or accept a failed search as a confirmed negative (a wrong conclusion baked into the final output).

### Two Anti-Patterns to Avoid

> [!warning] Anti-pattern 1: Silently suppressing errors
> Catching a failure and returning an empty result marked as success hides the failure from the coordinator entirely. The final synthesis will look complete and confident about a topic area that was, in fact, never actually researched.

> [!warning] Anti-pattern 2: Terminating the whole workflow on one failure
> Propagating an unhandled exception up to a top-level handler that kills the entire run overreacts to a single subagent's failure. If eight of nine subagents succeeded, killing the workflow throws away eight successful results to protect against one recoverable failure.

The correct middle path: subagents attempt **local recovery** for transient failures (retry with backoff inside the subagent, for example), and only propagate errors upward when they're genuinely unresolvable at that level — attaching what was attempted and any partial results, so the coordinator isn't starting from zero.

### Coverage Annotations in Synthesis

When a final report is assembled from multiple subagents where some failed or partially failed, the synthesis step should explicitly annotate **coverage** — which findings are well-supported by multiple sources, and which topic areas have gaps because a source was unavailable — rather than presenting a uniformly confident report that quietly omits what it couldn't get.

```text
## Coverage Notes
- Music and film industry impact: LOW coverage — web search subagent
  timed out on this sub-topic after 2 retries; findings below are from
  cached sources only.
- Visual arts impact: HIGH coverage — 6 independent sources agree.
```

---

## Context Degradation in Extended Codebase Exploration

Long, single-session codebase exploration degrades in a specific, recognizable way: as context fills with file contents, grep output, and prior reasoning, the model starts giving less consistent answers — referencing "typical patterns" or "the usual approach" instead of naming the specific class or function it discovered three steps earlier. The earlier findings haven't been deleted from context, but they're competing with a growing pile of exploration noise for attention.

### Scratchpad Files

The direct fix is to stop relying on conversational memory entirely for durable findings. A scratchpad file — a plain text or markdown file the agent writes to and re-reads — persists key findings (function signatures, file paths, discovered architecture decisions) across context boundaries, independent of how much unrelated exploration happens afterward.

```text
findings.md
- RefundProcessor lives in src/billing/refund.py:42
- It calls PaymentGateway.void() before writing a RefundRecord
- RefundRecord has NO foreign key to Order — joined via order_number string (tech debt)
```

Referencing this file for subsequent questions counteracts degradation directly: instead of asking the model to recall a detail from deep in a long context window, the answer comes from a small, explicitly-loaded, authoritative source.

### Subagent Delegation for Isolating Verbose Exploration

Spawning a subagent to investigate a specific, bounded question ("find all test files for the billing module," "trace every caller of `RefundProcessor.process()`") keeps the *main* agent's context clean. The subagent absorbs the verbose grep/read output; it reports back a condensed answer. The main agent preserves high-level coordination without its own context filling up with every intermediate file it didn't need to see directly.

> [!tip] Summarize before the next delegation round
> When exploration happens in phases, summarize key findings from one phase before spawning subagents for the next, and inject that summary into their initial context. This prevents each new subagent from re-discovering what the previous phase already established, and keeps the main agent's own context from growing unboundedly across many delegation rounds.

### Crash Recovery via State-Export Manifests

For exploration or build sessions that might be interrupted (a crash, a session timeout, a manual restart), structure state persistence so recovery doesn't mean starting over:

- Each agent/subagent exports its state (what it found, what it was doing, what's still pending) to a known location on disk.
- A coordinator, on resume, loads a **manifest** summarizing what each agent had completed and where it left off.

This turns "the session died" into "resume from the manifest" instead of "redo the last hour of exploration."

### Using `/compact`

Within a single Claude Code session, `/compact` reduces context usage by condensing the conversation so far, freeing room to continue without hitting context limits — useful specifically when a long exploration phase has filled context with verbose discovery output (file dumps, search results) that's no longer needed turn-by-turn, but you want to keep working in the same session rather than starting a fresh one and losing continuity.

---

## Related Notes

- [[01_Context_Preservation_and_Escalation|Context Preservation & Escalation]]
- [[03_Human_Review_and_Provenance|Human Review & Provenance]]
- [[../../01_Agentic_Architecture_and_Orchestration/Theory/02_Multi_Agent_Orchestration|Multi-Agent Orchestration]]
- [[../../00_Exam_Guide/Exam_Scenarios|Exam Scenarios — Scenario 3: Multi-Agent Research System · Scenario 4: Developer Productivity]]

---

[[../_Index|← Back to Context Management & Reliability Index]]
