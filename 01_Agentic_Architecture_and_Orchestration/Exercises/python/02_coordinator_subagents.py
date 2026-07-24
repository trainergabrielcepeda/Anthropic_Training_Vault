"""
Exercise 2 — Coordinator Dispatching to Parallel Subagents
Domain: Agentic Architecture & Orchestration (Tasks 1.2, 1.3)

Covers:
  - Hub-and-spoke: a coordinator dispatches to 2+ subagents and is the only
    thing that talks to each of them (they never talk to each other)
  - Explicit context passing — each subagent gets a fully self-contained
    prompt. There is NO shared conversation history and NO shared memory
    between the separate messages.create() calls below.
  - Parallel dispatch of independent subagent work (via a thread pool here,
    standing in for the harness executing multiple tool_use blocks at once)
  - Coordinator synthesis + a gap-check / re-delegation pass

IMPORTANT — how this maps to the Claude Agent SDK in production:
  This file uses plain, separate `client.messages.create()` calls with
  distinct system prompts and distinct (scoped) tool sets to SIMULATE
  subagents, because these exercises target the raw Anthropic SDK. In a
  real Claude Agent SDK deployment, this exact pattern is implemented with
  the built-in `Task` tool: the coordinator's `allowedTools` must include
  `"Task"`, and each subagent "role" below (web-search, doc-analysis) would
  instead be an `AgentDefinition` (description + system prompt + scoped
  tools) registered on the coordinator's `agents` config. Spawning them in
  parallel means emitting multiple `Task` tool_use blocks in a SINGLE
  coordinator turn — the concurrent dispatch below is the same idea,
  implemented at the raw-API level with a thread pool instead of the SDK's
  built-in Task tool.
"""

import json
from concurrent.futures import ThreadPoolExecutor
import anthropic

client = anthropic.Anthropic()

COORDINATOR_MODEL = "claude-opus-4-8"   # coordinator/orchestrator role — see Environment_Setup.md
SUBAGENT_MODEL = "claude-haiku-4-5-20251001"  # fast, scoped, low-cost subagent work


def call_subagent(role: str, system_prompt: str, user_prompt: str) -> dict:
    """A 'subagent' is just a separate, isolated messages.create() call.

    Nothing here is shared with the coordinator's own conversation history
    or with any other subagent call — that isolation is deliberate and is
    exactly what Task 1.3 means by "no automatic inheritance, no shared
    memory between invocations." Every fact the subagent needs must be in
    user_prompt.
    """
    response = client.messages.create(
        model=SUBAGENT_MODEL,
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = next((b.text for b in response.content if b.type == "text"), "")
    return {"role": role, "output": text}


def dispatch_subagents_in_parallel(jobs: list[dict]) -> list[dict]:
    """jobs: [{"role": ..., "system_prompt": ..., "user_prompt": ...}, ...]

    Runs all jobs concurrently. This models "emit multiple Task tool calls
    in a single coordinator response" — the point is that independent
    subtasks run at the same time instead of one full round-trip each.
    """
    with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        futures = [
            pool.submit(call_subagent, j["role"], j["system_prompt"], j["user_prompt"])
            for j in jobs
        ]
        return [f.result() for f in futures]


def coordinator_decompose(goal: str) -> list[dict]:
    """The coordinator decides WHICH subagents to invoke and with WHAT
    scoped context. Note each job's user_prompt is fully self-contained —
    it restates the goal rather than assuming the subagent can see it."""
    return [
        {
            "role": "web-researcher",
            "system_prompt": (
                "You are a focused web research subagent. Given a topic, "
                "produce 2-3 concrete, plausible findings a web search would "
                "surface, each tagged with a made-up but realistic source URL. "
                "This is a training exercise — invent plausible findings, do "
                "not claim to have actually searched the web."
            ),
            "user_prompt": (
                f"Research goal (from the coordinator): {goal}\n\n"
                "Focus specifically on recent (last 12 months) developments. "
                "Report findings as a bulleted list with a source URL per bullet."
            ),
        },
        {
            "role": "doc-analyzer",
            "system_prompt": (
                "You are a document analysis subagent. Given a topic, "
                "summarize what a set of internal knowledge-base documents "
                "would likely say about it, citing a made-up but realistic "
                "document name and page number per claim. This is a training "
                "exercise — invent plausible citations."
            ),
            "user_prompt": (
                f"Research goal (from the coordinator): {goal}\n\n"
                "Focus specifically on historical context and prior internal "
                "analysis. Report findings as a bulleted list with "
                "[doc_name.pdf, p.N] citations."
            ),
        },
    ]


def coordinator_synthesize(goal: str, subagent_results: list[dict]) -> str:
    """The coordinator is the only thing that sees every subagent's output
    and produces the final synthesis — subagents never see each other's work."""
    findings_block = "\n\n".join(
        f"### {r['role']} findings\n{r['output']}" for r in subagent_results
    )
    response = client.messages.create(
        model=COORDINATOR_MODEL,
        max_tokens=1024,
        system=(
            "You are a research coordinator. Synthesize the subagent "
            "findings below into one coherent, cited answer to the "
            "original goal. Preserve each claim's source attribution."
        ),
        messages=[{
            "role": "user",
            "content": f"Original goal: {goal}\n\n{findings_block}",
        }],
    )
    return next((b.text for b in response.content if b.type == "text"), "")


def coordinator_check_coverage_gaps(goal: str, synthesis: str) -> str | None:
    """A lightweight gap-check pass: does the synthesis leave an obvious
    sub-topic of the goal uncovered? This models the "coordinator evaluates
    synthesis output for gaps and re-delegates with a targeted query"
    pattern from Task 1.2 — guarding against decomposition that was too
    narrow (see the Scenario 3 example in the theory notes)."""
    response = client.messages.create(
        model=COORDINATOR_MODEL,
        max_tokens=256,
        system=(
            "You audit research syntheses for coverage gaps relative to the "
            "stated goal. Reply with a single short follow-up research query "
            "for the most significant gap, or the single word NONE if "
            "coverage looks adequate."
        ),
        messages=[{
            "role": "user",
            "content": f"Goal: {goal}\n\nSynthesis:\n{synthesis}",
        }],
    )
    text = next((b.text for b in response.content if b.type == "text"), "NONE").strip()
    return None if text.upper().startswith("NONE") else text


def run_coordinator(goal: str) -> str:
    print(f"Goal: {goal}\n{'-' * 60}")

    jobs = coordinator_decompose(goal)
    print(f"Dispatching {len(jobs)} subagents in parallel: {[j['role'] for j in jobs]}")
    results = dispatch_subagents_in_parallel(jobs)
    for r in results:
        print(f"\n--- {r['role']} output ---\n{r['output']}")

    synthesis = coordinator_synthesize(goal, results)
    print(f"\n--- Initial synthesis ---\n{synthesis}")

    gap_query = coordinator_check_coverage_gaps(goal, synthesis)
    if gap_query:
        print(f"\nCoverage gap detected — re-delegating: {gap_query}")
        follow_up = call_subagent(
            "web-researcher-followup",
            jobs[0]["system_prompt"],
            f"Follow-up research goal (from the coordinator): {gap_query}",
        )
        synthesis = coordinator_synthesize(goal, results + [follow_up])
        print(f"\n--- Revised synthesis ---\n{synthesis}")
    else:
        print("\nNo coverage gaps detected.")

    return synthesis


if __name__ == "__main__":
    final = run_coordinator(
        "What is the current state of on-device (edge) LLM inference?"
    )
    print(f"\n{'=' * 60}\nFinal synthesized answer:\n{final}")
