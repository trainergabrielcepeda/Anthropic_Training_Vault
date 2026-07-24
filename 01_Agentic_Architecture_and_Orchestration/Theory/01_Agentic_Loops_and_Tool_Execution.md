---
tags: [theory, agents, agentic-loop, tool-use]
topic: "01 - Agentic Architecture & Orchestration"
---

# Agentic Loops & Tool Execution

> [!important] Maps to Task 1.1
> **Design and implement agentic loops for autonomous task execution.** This note covers the exam's core mental model for "what is an agent, mechanically" — the loop lifecycle, how tool results become the next turn's context, and the anti-patterns the exam consistently rejects.

## The Agentic Loop Lifecycle

An agent built on the Claude API (or the Claude Agent SDK) is fundamentally a loop around a single primitive: `POST /v1/messages`. Each iteration follows the same four-step lifecycle:

1. **Send a request** — the full conversation history (`messages`), the `tools` array, and a `system` prompt go to the model.
2. **Inspect `stop_reason`** — the response tells you *why* generation stopped. This field, not the text content, is the control-flow signal.
3. **Execute requested tools** — if the model asked for tools, your harness runs them (locally, against your backend, or via MCP).
4. **Return results for the next iteration** — tool outputs are appended to the conversation as `tool_result` blocks, and the loop sends the updated history back to the model.

```
┌─────────────────────────────────────────────┐
│  1. Send request (messages + tools + system) │
│              ↓                               │
│  2. Inspect response.stop_reason              │
│         ├── "tool_use"  → step 3              │
│         └── "end_turn"  → loop terminates     │
│              ↓                               │
│  3. Execute each requested tool               │
│              ↓                               │
│  4. Append tool_result blocks to messages     │
│              ↓                               │
│  Back to step 1                               │
└─────────────────────────────────────────────┘
```

## `stop_reason`: the only signal that matters for control flow

| `stop_reason` | Meaning | Loop action |
| --- | --- | --- |
| `tool_use` | Claude wants to call one or more tools | Execute them, append results, continue the loop |
| `end_turn` | Claude finished its response with no further tool calls | Terminate the loop — this is the task's natural completion |
| `max_tokens` | Hit the output token cap | Not completion — retry with a higher `max_tokens` or stream |
| `pause_turn` | A server-side tool (web search, code execution) hit its internal iteration limit | Resume by re-sending the same history — do not treat as done |

> [!tip] The exam's framing
> Task 1.1 explicitly scopes the loop decision to **`"tool_use"` vs `"end_turn"`**. Everything else in the loop control flow is downstream of that one branch: continue while `tool_use`, terminate on `end_turn`.

## How tool results become the next turn's context

The API is stateless — nothing is remembered between calls. Every piece of state the model should "know about" for its next decision must be explicitly present in the `messages` array you send. This is why appending tool results correctly is the mechanism that lets Claude reason about its next action at all:

```python
import anthropic

client = anthropic.Anthropic()
messages = [{"role": "user", "content": "Look up order #A1029 and confirm the ship date."}]

while True:
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=4096,
        system="You are a support agent. Use tools to answer accurately.",
        tools=TOOLS,
        messages=messages,
    )

    # The assistant turn — including any tool_use blocks — must be appended
    # in full. Dropping it breaks the tool_use_id pairing on the next call.
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "end_turn":
        break  # primary termination signal — the task is done

    if response.stop_reason == "tool_use":
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,   # must match the tool_use block's id
                    "content": result,
                })
        # Tool results go back as a *user* turn — this is what lets the model
        # reason about the result on its next iteration.
        messages.append({"role": "user", "content": tool_results})
        continue

    break  # any other stop_reason: handle explicitly, don't silently loop
```

Two details the exam tests directly:

- The **assistant turn is appended verbatim**, including `tool_use` blocks — not just the extracted text. If you only append `block.text`, the next request loses the `tool_use_id` values and the API rejects the mismatched `tool_result`.
- Tool results are returned as a **single `user` message** containing all `tool_result` blocks from that turn, not one message per tool call. Splitting them across messages is a documented anti-pattern that also degrades parallel tool use over time.

## Model-driven decisions vs. pre-configured decision trees

A recurring distinction on this exam: agentic loops are **model-driven**, not scripted. Claude reasons about *which* tool to call next, given the current state of the conversation — your harness does not hardcode "after `get_customer`, always call `lookup_order`."

| | Model-driven (agentic loop) | Pre-configured decision tree |
| --- | --- | --- |
| Who decides the next action | Claude, based on the full context | A human-authored `if/elif` chain or state machine |
| Adapts to novel inputs | Yes — reasons over whatever the tool result actually contains | No — only handles paths the author anticipated |
| Where control logic lives | In the model's reasoning, informed by tool descriptions and system prompt | In application code |
| When to prefer it | Open-ended tasks, ambiguous inputs, unknown number of steps | Fully specified, deterministic workflows |

This doesn't mean the harness has *no* control — see [[03_Workflow_Control_and_Session_Management|Workflow Control & Session Management]] for where **programmatic enforcement** (hooks, prerequisite gates) belongs even inside a model-driven loop. The distinction is about who chooses *which* tool to call *next*, not whether the system has any deterministic guardrails at all.

## Anti-Patterns to Avoid

> [!warning] These three show up as wrong answers across multiple scenarios
> The exam repeatedly frames these as the "looks reasonable but is actually broken" distractor.

1. **Parsing natural-language signals to determine termination.** Scanning the assistant's text for phrases like "I'm done" or "Task complete" is fragile — phrasing varies, and a model discussing *why* it isn't done yet can accidentally contain the same trigger words. `stop_reason` is a structured, guaranteed field; text-sniffing is not.
2. **Arbitrary iteration caps as the *primary* stopping mechanism.** A loop that runs `for turn in range(MAX_TURNS)` and treats hitting the cap as normal completion conflates two different concerns: "the task is done" (`stop_reason == "end_turn"`) and "something is stuck" (a safety circuit breaker). An iteration cap is legitimate as a **secondary safety net** — logged and escalated as an anomaly — never as the condition that defines success.
3. **Checking assistant text content as a completion indicator.** Similar to (1) but broader: any logic that inspects `response.content` text blocks to decide whether to keep looping, instead of branching on `stop_reason`, is unreliable. The model's prose is for the user; `stop_reason` is for your control flow.

> [!example] What the safety net should look like
> ```python
> MAX_ITERATIONS = 20  # circuit breaker, NOT the primary stop condition
> for iteration in range(MAX_ITERATIONS):
>     response = client.messages.create(...)
>     messages.append({"role": "assistant", "content": response.content})
>     if response.stop_reason == "end_turn":
>         break
>     if response.stop_reason == "tool_use":
>         messages.append({"role": "user", "content": run_tools(response.content)})
>         continue
>     break
> else:
>     # Loop exhausted without end_turn — this is an anomaly, not success.
>     log_and_escalate("agent loop exceeded max iterations without completing")
> ```

## Related Notes

- [[02_Multi_Agent_Orchestration|Multi-Agent Orchestration]] — what happens when one loop delegates work to other agent loops
- [[03_Workflow_Control_and_Session_Management|Workflow Control & Session Management]] — programmatic enforcement, hooks, and session resumption
- [[../../02_Tool_Design_and_MCP_Integration/Theory/01_Tool_Interface_Design|Tool Interface Design]] — the tool-definition side of the `tool_use` → `tool_result` cycle, plus description quality and boundaries
- [[../../00_Exam_Guide/Exam_Scenarios|Exam Scenarios]] — Scenario 1 (Customer Support Resolution Agent) is the primary lens for this task statement

---

[[../_Index|← Back to Domain 1 Index]]
