---
tags: [theory, claude-code, iteration, ci-cd]
topic: "03 - Claude Code Configuration & Workflows"
---

# Iterative Refinement & CI/CD

## Why "Just Describe It Better" Runs Out

Prose descriptions of a desired transformation are interpreted inconsistently once the transformation has any nuance — edge cases, formatting rules, ordering. Rather than iterating on prose wording indefinitely, three concrete techniques converge faster.

---

## Concrete Input/Output Examples

When a natural-language description produces inconsistent results, the highest-leverage fix is usually **2–3 concrete input/output examples**, not a longer paragraph of description.

> [!example] Prose vs. examples
> Prose: "Normalize phone numbers to E.164 format, handling extensions reasonably."
> Examples:
> ```
> "(415) 555-0132" → "+14155550132"
> "555-0132 ext 4"  → "+15555550132;ext=4"
> "+44 20 7946 0958" → "+442079460958"
> ```
> The examples resolve ambiguity prose can't: what "reasonably" means for extensions, whether a bare 7-digit number gets a default area code assumption, how international numbers are treated. Two or three well-chosen examples, especially ones covering edge cases, communicate the transformation more reliably than an equivalent amount of additional prose.

---

## Test-Driven Iteration

Write the test suite **first** — covering expected behavior, edge cases, and (where relevant) performance bounds — then implement and iterate by sharing test failures rather than re-describing the requirement from scratch each round.

```
1. Write tests covering: happy path, null/empty input, boundary values, one performance constraint.
2. Ask Claude to implement against the tests.
3. Run the tests. Share the failing output (not a re-explanation) as the next input.
4. Repeat until green.
```

This works because a failing test with an actual-vs-expected diff is a much more precise signal than another paragraph of prose — it pinpoints exactly which case broke, without you having to re-derive and re-state the requirement.

> [!example] Fixing edge-case handling with a specific test case
> A migration script mishandles `NULL` values in a legacy column. Rather than saying "handle nulls better," provide the specific failing case: input row `{user_id: 42, plan: NULL}`, expected output `{user_id: 42, plan: "free"}` (the documented default), actual output currently `{user_id: 42, plan: null}`. That one concrete case is enough to fix the bug precisely, where "handle nulls better" risks an overcorrection that breaks a different case.

---

## The Interview Pattern

For unfamiliar domains, have Claude **ask questions before implementing** rather than immediately writing code against assumptions. This surfaces considerations you might not think to specify upfront — cache invalidation strategy, failure-mode behavior, concurrency assumptions — before they're baked into a design.

> [!example] Interview pattern in practice
> "Design a caching layer for this pricing API" → instead of immediate implementation, Claude asks: How long can stale prices be served? What happens on a cache miss during a pricing-source outage — serve stale, block, or fail? Is invalidation push-based (webhook) or TTL-based? Answering these up front is far cheaper than discovering the answers via a production incident after the cache is already built.

Use this pattern specifically when you (or the requester) don't yet know all the constraints — it's wasted overhead on a well-understood, already-fully-specified task.

---

## Batching Feedback: All Issues at Once vs. Sequentially

Whether to give Claude every known issue in one detailed message or fix issues one at a time depends on whether the issues **interact**:

| Issue relationship | Best approach |
| ------------------- | ------------- |
| Interacting (fixing one changes the right fix for another) | Provide **all** issues in one message, with full context on each |
| Independent (fixes don't affect each other) | Fine to iterate sequentially, one at a time |

> [!warning] Why interacting issues need to be batched
> If issue A is "the retry logic double-counts on timeout" and issue B is "the counter isn't thread-safe," fixing A first (adding a lock-free retry guard) can shape how B should be fixed (whether the guard itself needs to be the thread-safe primitive). Fixing sequentially risks a first fix that has to be partially undone once the second issue's context arrives. Give both up front so Claude designs one coherent fix.
> Independent issues (a typo in one function, a missing null check in an unrelated one) don't have this risk — sequential fixing is fine and keeps each round simpler to verify.

---

## Claude Code in CI/CD

### Non-interactive mode: `-p` / `--print`

Interactive Claude Code waits for input. In a pipeline, that means a hang, not a failure — the job never times out cleanly, it just sits.

```bash
claude -p "Review this PR diff for security issues and correctness bugs."
```

`-p` (`--print`) runs Claude Code non-interactively: it processes the prompt and exits, which is required for any CI/CD invocation. Workarounds like redirecting stdin from `/dev/null` or inventing an env var address the symptom, not the actual documented mechanism — `-p` is correct.

### Structured output for machine-parseable findings

```bash
claude -p "Review this diff for bugs and security issues." \
  --output-format json \
  --json-schema review-schema.json
```

`--output-format json` plus `--json-schema` makes Claude Code emit findings your pipeline can parse programmatically — e.g. to post one inline PR comment per finding, rather than a single unstructured wall of text a human has to re-triage.

### CLAUDE.md as the context bridge for CI-invoked runs

A CI-invoked `claude -p` run has no memory of prior interactive sessions — CLAUDE.md is how it learns project context automatically: testing standards, fixture conventions, what counts as a valid finding vs. noise for this repo's review criteria. Documenting "what a valuable test looks like here" and "which fixtures already exist" in CLAUDE.md measurably improves both generated tests (fewer duplicates of existing coverage) and review quality (fewer false positives flagged against intentional patterns).

### Avoiding duplicate findings across re-runs

When re-running a review after new commits land on a PR, include the prior review's findings in context and instruct Claude to report only **new or still-unaddressed** issues. Without this, every re-run re-surfaces every previously-reported issue as if it were new, and reviewers start ignoring the bot.

### Avoiding duplicate generated tests

Similarly, when generating tests in CI, provide the existing test files as context so Claude doesn't regenerate scenarios that are already covered — it should extend coverage, not duplicate it.

### Session isolation for self-review

> [!warning] The same session that wrote the code is a weaker reviewer of that code
> A Claude Code session that just generated a change carries the same assumptions and blind spots into reviewing it — it's prone to confirming its own reasoning rather than challenging it. An **independent** review invocation (a fresh session/process with no memory of the generation session, only the diff) reviews the change on its own merits and catches issues a self-review is structurally less likely to surface. In CI, this means the generation step and the review step should be separate `claude -p` invocations, not one session asked to "now review what you just wrote."

---

## Related Notes

- [[01_CLAUDE_md_and_Configuration|CLAUDE.md & Path-Specific Rules]]
- [[02_Commands_Skills_and_Plan_Mode|Commands, Skills & Plan Mode]]
- [[../Exercises/ci_cd/README|Exercise: `claude -p` + `--output-format json` in a review script]]

---

[[../_Index|← Back to Claude Code Configuration & Workflows Index]]
