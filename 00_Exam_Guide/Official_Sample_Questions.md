---
tags: [exam-guide, official, sample-questions]
topic: "00 - Exam Guide"
source: "Claude Certified Architect – Foundations, Exam Guide v1.0, Section 9 (publicly published sample items)"
---

# Official Sample Questions (Published by Anthropic)

These 12 items are reproduced from Section 9 of the official Exam Guide, which Anthropic publishes specifically so candidates can study the exam's format, difficulty, and reasoning style. They are grouped by [[Exam_Scenarios|scenario]]. Treat these as ground truth for calibration — the domain [[../Home|Practice Exams]] in this vault contain additional, original questions modeled on the same style, not verbatim exam-bank items (which are confidential under the exam NDA).

> [!tip] Pattern to notice
> Across all 12 items, the correct answer is almost always the **cheapest fix that addresses the stated root cause** — not the most sophisticated one. Wrong answers repeatedly reach for ML classifiers, sentiment analysis, bigger models, or more infrastructure when the guide's own explanations say a smaller, targeted change (a tool description, an explicit criterion, a hook) was correct.

---

## Scenario: Customer Support Resolution Agent

**Q1.** Production data shows that in 12% of cases, your agent skips `get_customer` entirely and calls `lookup_order` using only the customer's stated name, occasionally leading to misidentified accounts and incorrect refunds. What change would most effectively address this reliability issue?

A. Add a programmatic prerequisite that blocks `lookup_order` and `process_refund` calls until `get_customer` has returned a verified customer ID.
B. Enhance the system prompt to state that customer verification via `get_customer` is mandatory before any order operations.
C. Add few-shot examples showing the agent always calling `get_customer` first, even when customers volunteer order details.
D. Implement a routing classifier that analyzes each request and enables only the subset of tools appropriate for that request type.

**Answer: A.** Programmatic enforcement (a hook / prerequisite gate) gives deterministic guarantees that prompt-based approaches (B, C) cannot — critical when errors have financial consequences. D fixes tool *availability*, not tool *ordering*, which isn't the actual problem. → [[../01_Agentic_Architecture_and_Orchestration/Theory/03_Workflow_Control_and_Session_Management|Workflow enforcement & handoff patterns]]

**Q2.** Production logs show the agent frequently calls `get_customer` when users ask about orders (e.g. "check my order #12345"), instead of `lookup_order`. Both tools have minimal descriptions ("Retrieves customer information" / "Retrieves order details") and accept similar identifier formats. What's the most effective **first step**?

A. Add 5–8 few-shot examples to the system prompt demonstrating correct tool selection.
B. Expand each tool's description to include input formats, example queries, edge cases, and boundaries vs. similar tools.
C. Implement a routing layer that parses input before each turn and pre-selects the tool via keyword/identifier detection.
D. Consolidate both tools into a single `lookup_entity` tool that internally determines which backend to query.

**Answer: B.** Tool descriptions are the primary mechanism LLMs use for tool selection — the root cause here is a description problem, and B is the lowest-effort, highest-leverage fix. A adds token overhead without touching the root cause. C bypasses the model's own reasoning with a brittle parser. D is a legitimate architectural choice but is more effort than a "first step" warrants. → [[../02_Tool_Design_and_MCP_Integration/Theory/01_Tool_Interface_Design|Tool Interface Design]]

**Q3.** Your agent achieves 55% first-contact resolution vs. an 80% target. Logs show it escalates *straightforward* cases (standard damage replacements with photo evidence) while attempting to autonomously handle *complex* situations requiring policy exceptions. Most effective way to improve escalation calibration?

A. Add explicit escalation criteria to the system prompt with few-shot examples of when to escalate vs. resolve autonomously.
B. Have the agent self-report a 1–10 confidence score and auto-route below a threshold.
C. Deploy a separate classifier model trained on historical tickets to predict escalation need.
D. Implement sentiment analysis and auto-escalate on negative-sentiment threshold.

**Answer: A.** The root cause is unclear decision boundaries — explicit criteria + few-shot is the proportionate first response. B fails because LLM self-reported confidence is poorly calibrated (the agent is already wrongly confident on hard cases). C is over-engineered before prompt optimization has even been tried. D solves a different problem — sentiment doesn't correlate with case complexity. → [[../05_Context_Management_and_Reliability/Theory/01_Context_Preservation_and_Escalation|Escalation & Ambiguity Resolution]]

---

## Scenario: Code Generation with Claude Code

**Q4.** You want a custom `/review` slash command with your team's code review checklist, available to every developer on clone/pull. Where should you create it?

A. `.claude/commands/` in the project repository
B. `~/.claude/commands/` in each developer's home directory
C. The `CLAUDE.md` file at the project root
D. A `.claude/config.json` file with a commands array

**Answer: A.** Project-scoped commands live in `.claude/commands/`, version-controlled and shared. B is personal/unshared. C is for context, not command definitions. D doesn't exist in Claude Code. → [[../03_Claude_Code_Configuration_and_Workflows/Theory/02_Commands_Skills_and_Plan_Mode|Commands, Skills & Plan Mode]]

**Q5.** You're restructuring a monolith into microservices — dozens of files, decisions about service boundaries and module dependencies. Which approach?

A. Enter plan mode to explore the codebase and design an approach before making changes.
B. Start direct execution incrementally, letting implementation reveal service boundaries.
C. Direct execution with comprehensive upfront instructions detailing exact service structure.
D. Begin in direct execution and only switch to plan mode if unexpected complexity appears.

**Answer: A.** Plan mode exists exactly for large-scale, multi-file, architecturally-ambiguous work — it prevents costly rework. B risks late-discovered rework. C assumes you already know the answer without exploring. D ignores that the complexity is already known upfront, not something that might emerge. → [[../03_Claude_Code_Configuration_and_Workflows/Theory/02_Commands_Skills_and_Plan_Mode|Commands, Skills & Plan Mode]]

**Q6.** Distinct conventions per area (React hooks, async/await API handlers, repository-pattern models); test files (`Button.test.tsx`) sit next to the code they test, scattered everywhere, and must share one convention regardless of location. Most maintainable way to auto-apply the right convention?

A. `.claude/rules/` files with YAML frontmatter glob patterns to conditionally apply conventions by path.
B. Consolidate everything in root `CLAUDE.md` under headers, relying on Claude to infer the right section.
C. Create `.claude/skills/` per code type with conventions in their `SKILL.md`.
D. A separate `CLAUDE.md` in each subdirectory with that area's conventions.

**Answer: A.** Glob-pattern rules (e.g. `**/*.test.tsx`) apply by file type regardless of directory — essential when matching files are scattered. B relies on inference, not explicit matching. C requires manual/model-chosen invocation, not deterministic auto-application. D can't span files scattered across many directories since CLAUDE.md is directory-bound. → [[../03_Claude_Code_Configuration_and_Workflows/Theory/01_CLAUDE_md_and_Configuration|CLAUDE.md & Path-Specific Rules]]

---

## Scenario: Multi-Agent Research System

**Q7.** Topic: "impact of AI on creative industries." Each subagent completes successfully — web search finds relevant articles, document analysis summarizes correctly, synthesis is coherent — but the final report covers only visual arts, missing music, writing, film entirely. Coordinator logs show it decomposed into "AI in digital art creation," "AI in graphic design," "AI in photography." Most likely root cause?

A. The synthesis agent lacks instructions for identifying coverage gaps.
B. The coordinator's task decomposition is too narrow — subagent assignments don't cover all relevant domains of the topic.
C. The web search agent's queries aren't comprehensive enough.
D. The document analysis agent is over-filtering non-visual sources.

**Answer: B.** The logs show the root cause directly: the coordinator only generated visual-arts subtasks. Every subagent did its assigned job correctly — A, C, D all incorrectly blame agents that performed correctly within the (too-narrow) scope they were given. → [[../01_Agentic_Architecture_and_Orchestration/Theory/02_Multi_Agent_Orchestration|Multi-Agent Orchestration]]

**Q8.** The web search subagent times out mid-research. How should this failure flow back to the coordinator for the best recovery?

A. Return structured error context: failure type, attempted query, partial results, alternative approaches.
B. Retry with exponential backoff inside the subagent, returning a generic "search unavailable" only after retries exhaust.
C. Catch the timeout and return an empty result set marked as successful.
D. Propagate the exception to a top-level handler that terminates the entire workflow.

**Answer: A.** Structured error context is what lets the coordinator make an *intelligent* recovery decision. B hides context behind a generic status. C silently masks failure as success. D over-reacts by killing a workflow that partial results could still salvage. → [[../05_Context_Management_and_Reliability/Theory/02_Error_Propagation_and_Codebase_Context|Error Propagation Strategies]]

**Q9.** The synthesis agent frequently needs to verify simple facts (dates, names, stats) while combining findings; today it round-trips through the coordinator → web search agent → back, adding 2–3 round trips and +40% latency. 85% of verifications are simple fact-checks, 15% need deeper investigation. Best fix?

A. Give the synthesis agent a scoped `verify_fact` tool for simple lookups; route complex verification through the coordinator as before.
B. Have synthesis batch all verification needs and send them to the coordinator at the end of its pass.
C. Give the synthesis agent full web search tool access to handle everything itself.
D. Have the web search agent proactively cache extra context per source, anticipating synthesis needs.

**Answer: A.** Least-privilege: give the 85%-case a cheap scoped tool, keep the existing coordinator path for the 15%-case. B creates blocking dependencies (later steps may depend on earlier verified facts). C over-provisions synthesis and breaks separation of concerns. D relies on unreliable speculative caching. → [[../02_Tool_Design_and_MCP_Integration/Theory/02_Error_Handling_and_Tool_Distribution|Distributing Tools Across Agents]]

---

## Scenario: Claude Code for Continuous Integration

**Q10.** `claude "Analyze this pull request for security issues"` hangs indefinitely in the pipeline; logs show Claude Code waiting for interactive input. Correct fix?

A. Add the `-p` flag: `claude -p "Analyze this pull request for security issues"`
B. Set env var `CLAUDE_HEADLESS=true`.
C. Redirect stdin from `/dev/null`.
D. Add a `--batch` flag.

**Answer: A.** `-p` / `--print` is the documented non-interactive mode for CI. B and D reference flags/env vars that don't exist; C is a Unix workaround that doesn't address the actual CLI mode. → [[../03_Claude_Code_Configuration_and_Workflows/Theory/03_Iterative_Refinement_and_CICD|Claude Code in CI/CD]]

**Q11.** Team wants to cut API cost for two workflows: (1) a **blocking** pre-merge check developers wait on, (2) an **overnight** technical debt report. Manager proposes moving both to the Message Batches API for the 50% savings. How should you evaluate this?

A. Batch the technical debt reports only; keep real-time calls for the blocking pre-merge check.
B. Batch both, with status polling.
C. Keep both real-time to avoid batch result-ordering issues.
D. Batch both with a timeout fallback to real-time.

**Answer: A.** The Batches API can take up to 24h with no latency SLA — unsuitable for a blocking check, ideal for an overnight job. B ignores that "often faster" isn't good enough for a blocking workflow. C is a non-issue — batch results correlate via `custom_id`. D adds needless complexity when matching each API to its use case is simpler. → [[../04_Prompt_Engineering_and_Structured_Output/Theory/03_Batch_Processing_and_Multi_Pass_Review|Batch Processing Strategies]]

**Q12.** A PR touches 14 files in the stock tracking module. A single-pass review of all 14 together is inconsistent: deep feedback on some files, superficial on others, and it flags a pattern as a bug in one file while approving identical code elsewhere in the same PR. How should you restructure the review?

A. Split into focused passes: per-file local-issue analysis, then a separate cross-file integration pass.
B. Require developers to submit smaller 3–4 file PRs.
C. Switch to a higher-tier model with a larger context window to fit all 14 files.
D. Run 3 independent passes and only flag issues appearing in ≥2 of 3.

**Answer: A.** The root cause is attention dilution across many files at once; splitting into per-file + integration passes fixes it directly. B shifts the burden to developers. C misdiagnoses the problem as a context-size issue when it's an attention-quality issue. D would suppress real bugs that are only caught intermittently. → [[../04_Prompt_Engineering_and_Structured_Output/Theory/03_Batch_Processing_and_Multi_Pass_Review|Multi-Instance & Multi-Pass Review]]

---

[[Exam_Scenarios|← Exam Scenarios]] · [[Out_of_Scope_Topics|Out-of-Scope Topics →]]
