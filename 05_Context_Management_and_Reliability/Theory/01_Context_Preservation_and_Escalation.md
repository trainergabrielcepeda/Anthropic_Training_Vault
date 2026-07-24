---
tags: [theory, context-management, escalation, reliability]
topic: "05 - Context Management & Reliability"
---

# Context Preservation & Escalation

Long-running agent conversations fail in two characteristic ways: the agent quietly loses information it was told earlier (a context-preservation failure), or it makes the wrong call about whether to keep going on its own vs. hand off to a human (an escalation-calibration failure). Both are reliability problems, not capability problems — the model is smart enough to handle the case; the surrounding system just didn't give it what it needed, or didn't tell it when to stop.

---

## The Progressive Summarization Trap

As a conversation grows, a common mitigation is to periodically summarize older turns to save tokens. This works for narrative context ("the customer was frustrated about shipping delays") but is dangerous for **transactional facts** — the exact values a resolution depends on.

> [!warning] What gets lost in summarization
> Numerical values, percentages, dates, order numbers, and customer-stated expectations are exactly the details a summarizer treats as "detail" and compresses away. "Customer ordered 3 units on July 2nd expecting delivery by July 9th, willing to accept a 15% partial refund" can silently become "customer had a delivery issue" — and now the agent can't correctly evaluate a refund request three turns later.

The fix is **not** a better summarization prompt. It's structural: don't let transactional facts pass through the summarizer at all.

### Case Facts: A Persistent Layer Outside Summarized History

Maintain a small, structured "case facts" block — order numbers, amounts, dates, stated expectations, issue status — extracted the moment they appear, and re-inject it into **every** subsequent prompt, separate from (and never subject to) the summarized conversation history.

```text
CASE FACTS (persistent — do not summarize):
- order_id: 8841203
- order_date: 2026-07-02
- promised_delivery: 2026-07-09
- amount_charged: $214.50
- customer_ask: 15% partial refund
- issue_status: open, awaiting manager approval

--- Summarized conversation history below ---
Customer contacted support about a delayed shipment...
```

For sessions juggling more than one issue at a time, extend this into a **structured issue layer** — one case-facts record per issue — rather than a single flat block, so resolving issue A doesn't require re-deriving facts about issue B from a blended summary.

> [!tip] Same principle applies to subagent handoffs
> When a subagent reports findings back to a coordinator, requiring it to include **metadata** — dates, source locations, methodology — in its structured output prevents exactly the same loss. A downstream agent with a limited context budget should receive key facts, citations, and relevance scores instead of the subagent's full verbose reasoning chain; the coordinator can't act correctly on a compressed narrative that dropped the numbers.

---

## The "Lost in the Middle" Effect

Independent of summarization, models reliably attend most strongly to the **beginning** and **end** of a long input, and are more likely to under-weight or omit information buried in the **middle**. This isn't a summarization artifact — it happens even when the full, unsummarized text is present in context.

> [!example] Where this bites in practice
> A research-synthesis agent aggregates 10 documents into one prompt. Document 5 (in the middle) contains the one finding that contradicts the other nine. The agent's summary omits it — not because it was filtered out, but because it received less attention than document 1 and document 10.

**Mitigation:** put key-findings summaries at the **beginning** of aggregated inputs, under explicit section headers, rather than relying on positional luck:

```text
## KEY FINDINGS (read first)
- Finding from Doc 5 contradicts the majority: [detail]
- Finding from Doc 1: ...
- Finding from Doc 10: ...

## FULL SOURCE MATERIAL BELOW
[Doc 1] ... [Doc 5] ... [Doc 10]
```

This does not replace giving Claude the full source material — it front-loads a map of what matters so nothing in the middle gets silently dropped.

---

## Tool Results Accumulate Disproportionately to Relevance

Every tool call result gets appended to context, whether or not most of it is useful going forward. A `lookup_order` call might return 40+ fields (shipping carrier metadata, internal warehouse codes, audit timestamps) when only 5 matter for the current task (order status, amount, date, item, customer ID). Left unfiltered, tool output compounds across a multi-turn session and consumes tokens far out of proportion to the value it delivers.

> [!tip] Trim before it accumulates
> Extract and pass forward only the fields relevant to the task, immediately after the tool call returns — not "later, when context gets tight." By the time context is tight, the bloat is already baked into history that later requests must resend in full.

This is also why passing **complete** conversation history in each request matters for coherence — but "complete" should mean complete *relevant* state, not an unfiltered transcript of every raw tool payload ever returned.

---

## Escalation Triggers That Actually Work

An agent that never escalates isn't more capable — it's silently failing on the cases it can't actually handle. An agent that escalates too eagerly defeats the purpose of automating resolution. Calibration comes from **explicit criteria**, not the model's own read of how it's doing.

### When to escalate

| Trigger | Response |
| --- | --- |
| Customer explicitly asks for a human | Escalate **immediately** — do not first attempt resolution, do not ask "are you sure?" |
| Request falls into a genuine **policy gap** (not covered, not merely hard) | Escalate — the agent has no authority to improvise policy |
| No meaningful progress possible (missing data, blocked dependency) | Escalate with what was tried |
| Case is merely complex but within documented policy | Attempt resolution; acknowledge difficulty but do not escalate reflexively |

> [!warning] "Complex" is not an escalation trigger — "no authority" is
> A multi-step refund with several line items is complex but resolvable if policy covers it. A request to match a competitor's price when policy only defines *own-site* price adjustments is a **policy gap** — the agent isn't unsure how to execute, it has no rule to execute at all. That distinction is what should drive escalation, not a subjective sense of difficulty.

### Honoring explicit requests immediately

If a customer says "let me talk to a person," escalate on that turn. Do not spend a turn attempting a resolution first — that reads as ignoring the customer's stated preference, even if the resolution would have worked. If a customer expresses frustration but hasn't explicitly asked for a human, acknowledge the frustration and offer to resolve if the case is within capability; escalate only if they reiterate the preference for a human.

### Building this into the system prompt

The most effective mechanism is **explicit escalation criteria plus few-shot examples** in the system prompt — concrete "escalate in this situation / resolve in this situation" pairs — not a general instruction to "escalate complex cases," which leaves the actual boundary undefined and inconsistently applied.

---

## Why Sentiment and Self-Reported Confidence Are Unreliable Proxies

Two tempting shortcuts for escalation routing both fail for the same underlying reason: neither one measures the thing that actually matters, which is whether the request falls within documented policy and available tools.

> [!warning] Sentiment-based escalation
> Auto-escalating on negative sentiment routes based on **tone**, not **case complexity**. A calm customer can have a genuinely policy-gap request; a frustrated customer can have a trivial, fully-covered one. Sentiment and resolvability are uncorrelated.

> [!warning] Self-reported confidence scores
> Asking the model to rate its own confidence (e.g., 1–10) and routing below a threshold sounds appealing but is poorly calibrated in exactly the cases that matter most: an agent that is *wrongly* confident on a hard case will self-report high confidence and never trigger the escalation it should. Confidence self-reports and actual correctness are not reliably correlated — that's precisely why explicit, externally-defined criteria (not the model's internal assessment) have to be the trigger.

Both patterns are seductive because they're cheap to implement — a threshold check on a number the model already produces. That cheapness is the trap: neither replaces the harder, correct work of writing down explicit escalation criteria.

---

## Multiple Matches Require Clarification, Not Heuristic Selection

When a tool call returns more than one plausible match — two customer accounts with the same name, several orders matching a partial identifier — the correct response is to **ask the customer for an additional identifier** (email, order number, ZIP code), not to guess based on recency, order value, or any other heuristic.

> [!example] Why heuristic selection is dangerous
> "Pick the most recent order" silently picks the wrong account when the customer is asking about an older one. Because the agent picked *confidently*, the resulting error looks like a correct answer until the customer notices it's about the wrong purchase — which, for something like a refund, has real financial and trust consequences. A short clarifying question costs one turn; a wrong account selection costs a support escalation once the customer discovers it later.

---

## Related Notes

- [[02_Error_Propagation_and_Codebase_Context|Error Propagation & Codebase Context]]
- [[03_Human_Review_and_Provenance|Human Review & Provenance]]
- [[../../01_Agentic_Architecture_and_Orchestration/Theory/03_Workflow_Control_and_Session_Management|Workflow Control & Session Management]]
- [[../../00_Exam_Guide/Exam_Scenarios|Exam Scenarios — Scenario 1: Customer Support Resolution Agent]]

---

[[../_Index|← Back to Context Management & Reliability Index]]
