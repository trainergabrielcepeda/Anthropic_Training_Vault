---
tags: [theory, tools, mcp, tool-design]
topic: "02 - Tool Design & MCP Integration"
task: "2.1"
---

# Tool Interface Design

> [!important] Exam Task 2.1
> Design effective tool interfaces with clear descriptions and boundaries.

This note assumes you already know the basic mechanics of tool use (the `tool_use` / `tool_result` two-turn cycle, `stop_reason`, JSON Schema for `input_schema`). The exam does not re-test that plumbing — it tests whether you can diagnose and fix **description quality** and **tool boundary** problems, which is where real agent systems actually break. See the quick recap below if you need a refresher, then skip to [[#Descriptions Are the Primary Selection Signal]].

---

## Quick Recap — Tool Definition Mechanics

A tool is a JSON schema you expose to Claude:

```json
{
  "name": "lookup_order",
  "description": "...",
  "input_schema": {
    "type": "object",
    "properties": { "order_id": { "type": "string" } },
    "required": ["order_id"]
  }
}
```

Claude never executes tools itself. It emits a `tool_use` content block (`stop_reason: "tool_use"`) with a `name`, an `input` object matching your schema, and an `id`. Your application executes the real logic and appends a `tool_result` block referencing that same `id` back into `messages` before the conversation can continue. Of the three fields in a tool definition, `description` is the one Claude relies on most heavily — everything below is about getting that field right.

---

## Descriptions Are the Primary Selection Signal

When Claude has multiple tools available, it does not have access to your internal implementation, your database schema, or your team's mental model of "what this tool is really for." It has exactly one thing to reason from: the `name` and `description` you wrote (plus the surrounding conversation). This makes tool descriptions the **primary mechanism** Claude uses to decide both *whether* to call a tool and *which* tool to call among similar options.

> [!warning] Minimal descriptions cause unreliable selection
> `"description": "Retrieves customer information"` and `"description": "Retrieves order details"` look unambiguous to a human who already knows the system. To Claude, faced with "check my order #12345," both descriptions are plausible matches — nothing in either string says which one owns order lookups. The result is inconsistent routing: the same class of question gets handled by different tools from one run to the next.

**Example — real production failure pattern:**

```json
// Tool A
{ "name": "analyze_content", "description": "Analyzes content and provides insights." }

// Tool B
{ "name": "analyze_document", "description": "Analyzes a document and returns information." }
```

Nothing here tells Claude what kind of input each tool expects, what output shape it returns, or when one is correct over the other. Near-identical, low-information descriptions like this are the single most common root cause of tool misrouting — not model capability, not the number of tools, not the ordering of the tools array.

---

## Anatomy of a Good Description

A well-written description answers four questions a teammate would need answered before they could use the tool correctly:

| Question | What to include |
| -------- | ---------------- |
| What does it do? | A precise, one-sentence purpose statement |
| What goes in? | Input format, with 1-2 example values |
| What comes out? | Output shape / what the caller can expect back |
| When (not) to use it? | Trigger conditions, and explicit exclusions vs. similar tools |

```json
{
  "name": "extract_data_points",
  "description": "Pull one or more specific, named data points (numbers, dates, names, figures) out of a document. Use when the user asks for a precise value such as 'total revenue', 'filing date', or 'CEO name'. Input: raw text plus the field(s) to extract. Output: the exact value(s) found, or null if not present. Do NOT use this for open-ended summarization or claim verification — use summarize_content or verify_claim_against_source instead."
}
```

> [!tip] Write the exclusion, not just the inclusion
> "Do NOT use this for X — use Y instead" is doing as much routing work as the positive description. Boundary language is what lets Claude disambiguate between tools that operate in the same general area.

---

## Splitting Generic Tools Into Purpose-Specific Tools

A common anti-pattern is a single "do everything" tool with an internal `mode` or `action` parameter that silently decides behavior:

```json
{
  "name": "process_document",
  "input_schema": {
    "properties": {
      "mode": { "type": "string", "enum": ["summarize", "extract", "verify"] }
    }
  }
}
```

This pushes the disambiguation problem *inside* the tool call, where Claude has to pick the right `mode` value correctly on every call — a harder, less visible failure mode than picking the wrong tool, because a wrong `mode` still looks like a successful `tool_use` block.

**Fix: split by purpose**, giving each capability its own name, description, and input/output contract:

- `summarize_content(text)` → condensed key points
- `extract_data_points(text, field)` → a specific named value
- `verify_claim_against_source(text, claim)` → supported / contradicted / not addressed

Each tool's *name* now carries routing signal before Claude even reads the description. This is strictly better than a well-documented `mode` enum, because tool selection is a capability Claude is specifically trained to do well; picking the right value of an opaque internal parameter is not.

> [!example] Renaming to eliminate overlap
> If two tools do genuinely different things but share vague, overlapping names (`get_data` vs. `fetch_data`), renaming them to reflect their actual behavior (`query_live_inventory` vs. `read_cached_snapshot`) plus rewriting the descriptions around that distinction is usually enough to fix misrouting — no architecture change required.

---

## System-Prompt Keyword Sensitivity

Tool descriptions aren't the only source of routing signal — instructions in the system prompt can override them, sometimes unintentionally. A blanket instruction like:

> "Always check inventory levels before answering product questions."

creates a **keyword-driven association**: any user message containing "product" now risks triggering `check_inventory`, even for something like "What's your return policy?" (which mentions "product" only in passing). The tool's own description may be perfectly scoped — the problem is a system-prompt rule that isn't.

> [!warning] Review system prompts for keyword triggers, not just tool descriptions
> When diagnosing a misrouting bug, check both places. If the tool descriptions are already precise and boundaried but the behavior is still keyword-driven, the fix is rewriting the system-prompt instruction to state the *specific conditions* under which the tool should be called — not to touch the tool definition at all.

---

## Diagnosing Misrouting — the First Step

When production logs show a tool being called incorrectly or inconsistently, the exam consistently rewards the **cheapest fix that addresses the stated root cause**:

1. **First**, check whether the descriptions are vague/overlapping → rewrite them with input formats, example queries, and explicit boundaries. This is almost always the correct first step.
2. **Only if** two tools are structurally redundant (not just poorly described) → consider splitting/renaming/consolidating.
3. **Avoid** reaching for a routing classifier, a keyword pre-parser, or few-shot examples as a first response — these add complexity or token overhead without fixing the description that caused the ambiguity in the first place.

---

## Tool Interface Design Checklist

- [ ] Description states what the tool does, in one precise sentence
- [ ] Description includes an example input/query
- [ ] Description states the output shape or what the caller receives
- [ ] Description explicitly excludes cases handled by similar tools ("do NOT use for...")
- [ ] Tool name itself signals purpose (avoid `process_*`, `handle_*`, `do_*` with a hidden mode parameter)
- [ ] System prompt reviewed for keyword-triggered instructions that could override tool descriptions
- [ ] No two tools in the same request have descriptions that could plausibly apply to the same user query

---

## Related Notes

- [[02_Error_Handling_and_Tool_Distribution|Error Handling & Tool Distribution]]
- [[03_MCP_Servers_and_Builtin_Tools|MCP Servers & Built-in Tools]]
- [[../../00_Exam_Guide/Official_Sample_Questions|Official Sample Questions — Q2 walks through this exact diagnosis]]

---

[[../_Index|← Back to Domain 2 Index]]
