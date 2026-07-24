---
tags: [theory, agents, multi-agent, orchestration, subagents]
topic: "01 - Agentic Architecture & Orchestration"
---

# Multi-Agent Orchestration

> [!important] Maps to Tasks 1.2 and 1.3
> **1.2 — Orchestrate multi-agent systems with coordinator-subagent patterns.** **1.3 — Configure subagent invocation, context passing, and spawning.** Together these cover the hub-and-spoke architecture, the `Task` tool as the spawning mechanism, and the rules around context isolation that trip up most multi-agent designs.

## Hub-and-Spoke Architecture

A coordinator-subagent system is a **hub-and-spoke**, not a mesh: the coordinator is the hub, and every subagent is a spoke that only talks to the coordinator — never directly to each other.

```
                 ┌──────────────┐
   User ───────▶ │  Coordinator │
                 └──────┬───────┘
        ┌───────────────┼───────────────┐
        ▼                ▼               ▼
  ┌───────────┐   ┌─────────────┐  ┌───────────┐
  │ Subagent A │   │ Subagent B  │  │ Subagent C │
  │ (web search)│   │ (doc analysis)│ │ (synthesis)│
  └───────────┘   └─────────────┘  └───────────┘
```

The coordinator owns:

- **Decomposition** — breaking the goal into subtasks
- **Delegation** — deciding which subagent(s) to invoke, and with what scoped context
- **Routing** — all inter-subagent communication passes through it; subagents never call each other directly
- **Error handling** — a subagent failure surfaces to the coordinator, not silently to the user
- **Aggregation** — synthesizing subagent outputs into a coherent final result

> [!tip] Why route everything through the coordinator?
> Centralizing communication gives you one place for observability (every handoff is logged) and one place for consistent error handling (a subagent timeout is handled the same way regardless of which subagent failed). A mesh where subagents call each other directly loses both properties.

## Subagents Have Isolated Context — This Is the #1 Source of Bugs

**Subagents do NOT automatically inherit the coordinator's conversation history.** Each subagent invocation starts with a blank context window; whatever the subagent needs to know must be explicitly written into the prompt you give it.

> [!warning] The most common multi-agent bug on this exam
> A coordinator that says "delegate the verification to the research subagent" without restating *what* to verify produces a subagent with no idea what "it" refers to. If a task statement or sample question shows a subagent producing generic, contextless, or repeated-from-scratch work, isolated context is almost always the root cause.

This isolation is a feature, not a limitation to work around by trying to share memory — it keeps each subagent's context window focused on its own scoped task instead of accumulating the coordinator's entire history. The fix is always **explicit context passing** (see Task 1.3, below), never an attempt to give subagents automatic access to the coordinator's transcript.

## Decomposition Breadth: the Narrow-Decomposition Risk

The coordinator's decomposition step determines coverage. If the coordinator generates subtasks that are individually correct but collectively too narrow, **every subagent can succeed and the final output can still be wrong** — because whole sub-topics were never assigned to anyone.

> [!example] Official exam pattern
> A research coordinator asked to cover "the impact of AI on creative industries" decomposes into "AI in digital art," "AI in graphic design," "AI in photography" — three visual-arts subtasks. Web search, document analysis, and synthesis all execute their assigned work correctly. The final report is still wrong: it never mentions music, writing, or film, because the coordinator's decomposition never generated tasks for them. The bug is in decomposition breadth, not in any individual subagent — don't blame a downstream agent for correctly executing a scope it was never given.

Mitigations:

- **Dynamically select which subagents to invoke** based on the actual complexity and breadth of the query, rather than always routing every request through a fixed pipeline of every available subagent type.
- **Partition scope explicitly** across subagents to minimize both gaps and duplication — each subagent's assignment should be traceable back to a piece of the original goal.
- **Iterative refinement**: after synthesis, the coordinator evaluates the combined output for coverage gaps and **re-delegates with targeted queries** to fill them, rather than treating the first synthesis pass as final.

```python
# Illustrative coordinator loop — evaluate synthesis output, re-delegate on gaps
synthesis = synthesize(subagent_results)
gaps = coordinator_evaluate_coverage(original_goal, synthesis)
while gaps:
    targeted_results = [dispatch_subagent(gap) for gap in gaps]
    synthesis = synthesize([synthesis] + targeted_results)
    gaps = coordinator_evaluate_coverage(original_goal, synthesis)
```

## Task 1.3 — Spawning Subagents: the `Task` Tool

In the Claude Agent SDK, the coordinator spawns subagents through the built-in **`Task` tool** — it is the mechanism, not a metaphor. For a coordinator to be able to invoke subagents at all, its tool configuration must include `Task` in `allowedTools`:

```python
# Illustrative — Claude Agent SDK coordinator configuration
options = ClaudeAgentOptions(
    allowed_tools=["Task", "Read", "Grep"],  # "Task" is required to spawn subagents
    agents={
        "web-researcher": AgentDefinition(
            description="Searches the web for current information on a narrow, well-scoped topic.",
            prompt="You are a focused web research subagent. Report findings with source URLs.",
            tools=["WebSearch", "WebFetch"],
            model="haiku",
        ),
        "doc-analyzer": AgentDefinition(
            description="Extracts and summarizes findings from a provided set of documents.",
            prompt="You are a document analysis subagent. Cite page numbers for every claim.",
            tools=["Read", "Grep"],
            model="sonnet",
        ),
    },
)
```

`AgentDefinition` is where subagent-specific configuration lives: a **description** (used for routing/selection), a **system prompt** scoped to that subagent's job, and **tool restrictions** — each subagent type gets only the tools its role requires, not the coordinator's full toolset.

### Explicit context passing — no automatic inheritance, no shared memory

Because subagents don't inherit history, every `Task` invocation must **include complete prior findings directly in the prompt**. This is the practical mechanism behind "isolated context" above:

```python
# Bad — assumes the subagent knows what "it" and "the prior findings" refer to
Task(subagent_type="doc-analyzer", prompt="Analyze the documents and cross-check them.")

# Good — the prompt is self-contained
Task(
    subagent_type="doc-analyzer",
    prompt=(
        "Cross-check the following claim against the attached documents: "
        "'Revenue grew 12% YoY in Q3.' Prior research found this claim in "
        "source [Q3_earnings.pdf, p.4] and a conflicting figure of 9% in "
        "[analyst_note.pdf, p.1]. Determine which is correct and cite page numbers."
    ),
)
```

> [!tip] Preserve attribution across handoffs with structured data
> When passing prior findings into a subagent prompt, use a structured format that separates **content** from **metadata** — source URL, document name, page number — rather than flattening everything into prose. This is what lets a claim survive multiple handoffs (subagent → coordinator → synthesis subagent) without losing *where it came from*, which matters directly for citation quality in a research system (see [[../../00_Exam_Guide/Exam_Scenarios|Scenario 3]]).

### Spawning subagents in parallel

To actually run subagents concurrently, the coordinator must emit **multiple `Task` tool calls in a single response** — not issue one `Task` call, wait for the turn to complete, and issue another in a later turn. One assistant turn containing several `tool_use` blocks (all `Task` calls) is what enables the harness to dispatch them concurrently; sequential turns force sequential execution even if nothing about the subtasks is dependent.

```python
# Bad — two separate coordinator turns force sequential subagent execution
turn_1: Task(subagent_type="web-researcher", prompt="Research X")
# ... wait for result ...
turn_2: Task(subagent_type="web-researcher", prompt="Research Y")

# Good — one coordinator turn, two Task calls → dispatched in parallel
turn_1: [
    Task(subagent_type="web-researcher", prompt="Research X"),
    Task(subagent_type="web-researcher", prompt="Research Y"),
]
```

### Writing coordinator prompts: goals, not procedures

Coordinator prompts (and the prompts a coordinator writes into `Task` calls) should specify **goals and quality criteria**, not a rigid step-by-step procedure. A subagent given "call `web_search` with these 3 exact queries in this exact order" cannot adapt when the first query returns nothing useful. A subagent given "find at least 3 independent sources on X; prioritize primary sources over aggregators" can adjust its approach while staying aligned with what the coordinator actually needs.

### Fork-based session management (`fork_session`)

`fork_session` creates an independent branch from a shared baseline — useful when you want to explore **divergent approaches** from the same starting context without either branch affecting the other. This differs from spawning a subagent for a *different* subtask: forking is for exploring *alternative* paths through the *same* task (e.g., two competing refactoring strategies evaluated from an identical codebase analysis). See [[03_Workflow_Control_and_Session_Management|Workflow Control & Session Management]] for the full session-management treatment, including when forking beats resuming.

## Related Notes

- [[01_Agentic_Loops_and_Tool_Execution|Agentic Loops & Tool Execution]] — the single-agent loop mechanics each subagent runs internally
- [[03_Workflow_Control_and_Session_Management|Workflow Control & Session Management]] — enforcement, handoffs, decomposition strategy, and session forking
- [[../../02_Tool_Design_and_MCP_Integration/Theory/02_Error_Handling_and_Tool_Distribution|Distributing Tools Across Agents]] — scoping tools per subagent role
- [[../../00_Exam_Guide/Exam_Scenarios|Exam Scenarios]] — Scenario 3 (Multi-Agent Research System) is the primary lens for these task statements

---

[[../_Index|← Back to Domain 1 Index]]
