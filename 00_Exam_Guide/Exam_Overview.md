---
tags: [exam-guide, official]
topic: "00 - Exam Guide"
source: "Claude Certified Architect – Foundations, Exam Guide v1.0, effective July 2026"
---

# Exam Overview — Claude Certified Architect – Foundations (CCAR-F)

> [!important] This note distills the official exam guide
> Facts below come from Anthropic's published *Claude Certified Architect – Foundations Exam Guide* (v1.0, effective July 2026, exam code **CCAR-F**). The guide is downloadable from the [Anthropic Partner Academy](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification). Anthropic states the guide is "subject to change without notice" — re-check it before scheduling.

## What changed (name history)

| Era | Name / code |
| --- | ----------- |
| Launch, March 2026 | Claude Certified Architect – Foundations (**CCA-F**), partner-only |
| July 2026 | Renamed **CCAR-F**; exam opened to the public; certification program expanded to a 4-exam family |

The 2026 certification family: **Claude Certified Associate – Foundations (CCAO-F)** for non-builders, **Claude Certified Developer – Foundations (CCDV-F)**, **Claude Certified Architect – Foundations (CCAR-F)** — this vault's target — and **Claude Certified Architect – Professional (CCAR-P)** as the advanced follow-on. Don't confuse this vault's material with the Associate or Developer tracks; they test different things.

## Who this exam is for

A solution architect who designs and implements **production applications with Claude**, with 6+ months hands-on experience across the Claude Agent SDK, Claude Code, the Claude API, and MCP. The exam assumes you can already write a prompt — it tests whether you can architect something that holds together in production: orchestration, configuration, tool design, and reliability tradeoffs.

## Exam facts at a glance

| | |
| --- | --- |
| Credential | Claude Certified Architect – Foundations |
| Exam code | CCAR-F |
| Items | 60 (multiple-choice and multiple-response — each item states how many responses to select) |
| Structure | 4 scenarios presented, drawn at random from a bank of 6 fixed scenarios (see [[Exam_Scenarios]]) |
| Time limit | 120 minutes |
| Delivery | Proctored — online (webcam) or Pearson VUE test center |
| Passing score | 720 on a scaled 100–1,000 range (criterion-referenced, not curved) |
| Fee | $125 USD (was $99 at March 2026 launch) |
| Validity | 12 months from award date; free non-proctored renewal assessment if taken on time |
| Retakes | 14 days after 1st fail, 30 days after 2nd, 90 days after 3rd; max 4 attempts / rolling 12 months; fee applies each time |

## Domain weighting (the blueprint)

| # | Domain | Weight |
| - | ------ | ------ |
| 1 | Agentic Architecture & Orchestration | **27%** |
| 2 | Tool Design & MCP Integration | **18%** |
| 3 | Claude Code Configuration & Workflows | **20%** |
| 4 | Prompt Engineering & Structured Output | **20%** |
| 5 | Context Management & Reliability | **15%** |

This vault's five topic folders map 1:1 to these domains, in this order and with these weights — see [[../Home|Home]] for navigation.

## How it's scored

Criterion-referenced: you're measured against a fixed performance standard set by a formal standard-setting study (subject matter experts judging minimally-qualified-candidate performance), not curved against other candidates. Your score report shows pass/fail plus percent-correct **per domain** — but the domain breakdown is informational only; your pass/fail is decided by the total scaled score, not by clearing any per-domain bar.

## Registration

Handled via the Anthropic Partner Academy → Pearson VUE (OnVUE). Delivery moved to Pearson VUE in early July 2026. You can cancel/reschedule up to 24 hours before your appointment without forfeiting the fee.

## Exam-day conduct

Closed-book, proctored. If testing online: stay in webcam view the whole session, clear workspace (no notes/phones/second monitor), no communicating with anyone, no capturing exam content. You must accept an NDA before the exam starts — declining ends the session with no refund.

## What this means for how you study

- Don't over-invest in general "what is Claude" / model-comparison trivia — see [[Out_of_Scope_Topics]]. Anthropic explicitly excludes it.
- Expect **scenario-anchored** questions, not isolated trivia. Each of the 6 scenarios frames several items across 2–3 domains at once — see [[Exam_Scenarios]].
- Study the 12 officially published sample items closely — see [[Official_Sample_Questions]]. They reveal the exam's actual reasoning style: root-cause identification, "most effective first step," and rejecting over-engineered options.
- The distractor pattern repeats: the wrong answers are usually (a) prompt-only/probabilistic fixes where deterministic enforcement is needed, (b) over-engineered infrastructure for a problem that has a cheap first fix, or (c) treating a symptom instead of the stated root cause.

## Related notes

- [[Exam_Scenarios]] — the 6 official scenarios questions are drawn from
- [[Official_Sample_Questions]] — 12 official sample items with explanations
- [[Out_of_Scope_Topics]] — what will *not* be tested
- [[../Home|Home]] — vault navigation and domain links
