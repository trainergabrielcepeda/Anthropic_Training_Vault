---
tags: [exam-guide, official, scope]
topic: "00 - Exam Guide"
source: "Claude Certified Architect – Foundations, Exam Guide v1.0, Section 17 Appendix"
---

# In-Scope vs. Out-of-Scope Topics

Straight from the official exam guide's appendix. Use this to stop studying things that won't pay off and to sanity-check that nothing in this vault drifts into tested-but-missing or untested-but-included territory.

## Explicitly out of scope (will NOT appear on the exam)

- Fine-tuning Claude models or training custom models
- Claude API authentication, billing, or account management
- Detailed implementation of specific programming languages/frameworks (beyond what tool/schema config requires)
- Deploying or hosting MCP servers (infrastructure, networking, container orchestration)
- Claude's internal architecture, training process, or model weights
- **Constitutional AI, RLHF, or safety training methodologies**
- Embedding models or vector database implementation details
- Computer use (browser automation, desktop interaction)
- Vision / image analysis capabilities
- Streaming API implementation or server-sent events
- Rate limiting, quotas, or API pricing calculations
- OAuth, API key rotation, or authentication protocol details
- Specific cloud provider configurations (AWS, GCP, Azure)
- Performance benchmarking or model comparison metrics
- Prompt caching implementation details (beyond knowing it exists)
- Token counting algorithms or tokenization specifics

> [!warning] Why this matters for this vault
> An earlier version of this vault was built around a different, hypothetical "Associate" blueprint that spent ~15% of its weight on Responsible AI/Constitutional AI and a full domain on general model overview and API auth. **None of that is tested by CCAR-F.** That domain has been retired from this vault; don't resurrect it as exam prep (it's still perfectly good material for general Claude literacy — just not for this credential).

## In-scope topics (explicitly tested)

Grouped roughly by domain — see each domain's `_Index.md` for the full task-statement breakdown:

- Agentic loop implementation: `stop_reason`-driven control flow, tool result handling, loop termination
- Multi-agent orchestration: coordinator-subagent patterns, task decomposition, parallel execution, iterative refinement loops
- Subagent context management: explicit context passing, structured state persistence, crash recovery via manifests
- Tool interface design: description quality, splitting vs. consolidating tools, naming to reduce ambiguity
- MCP tool/resource design: resources for content catalogs, tools for actions, description quality for adoption
- MCP server configuration: project vs. user scope, env var expansion, multi-server simultaneous access
- Error handling and propagation: structured error responses, transient vs. business vs. permission errors, local recovery before escalation
- Escalation decision-making: explicit criteria, honoring customer preference, policy-gap identification
- CLAUDE.md configuration: hierarchy, `@import`, `.claude/rules/` glob patterns
- Custom commands and skills: project vs. user scope, `context: fork`, `allowed-tools`, `argument-hint`
- Plan mode vs. direct execution: complexity assessment
- Iterative refinement: input/output examples, test-driven iteration, interview pattern
- Structured output via `tool_use`: schema design, `tool_choice`, nullable fields to prevent hallucination
- Few-shot prompting: ambiguous-scenario targeting, format consistency, false-positive reduction
- Batch processing: Message Batches API fit, latency-tolerance assessment, failure handling by `custom_id`
- Context window optimization: trimming verbose tool output, structured fact extraction, position-aware ordering
- Human review workflows: confidence calibration, stratified sampling, accuracy segmentation
- Information provenance: claim-source mappings, temporal data, conflict annotation, coverage-gap reporting

## Technologies/concepts that might appear

Claude Agent SDK · Model Context Protocol (MCP) · Claude Code (CLAUDE.md, `.claude/rules/`, `.claude/commands/`, `.claude/skills/`, plan mode, `/memory`, `/compact`, `--resume`, `fork_session`, Explore subagent) · Claude Code CLI (`-p`/`--print`, `--output-format json`, `--json-schema`) · Claude API (`tool_use`, `tool_choice`, `stop_reason`, `max_tokens`, system prompts) · Message Batches API · JSON Schema · Pydantic · built-in tools (Read, Write, Edit, Bash, Grep, Glob) · few-shot prompting · prompt chaining · context window management · session management · confidence scoring.

---

[[Official_Sample_Questions|← Official Sample Questions]] · [[Exam_Overview|Exam Overview]] · [[../Home|Home]]
