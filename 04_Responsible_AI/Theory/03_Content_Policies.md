---
tags: [theory, safety, content-policy]
topic: "04 - Responsible AI & Safety"
---

# Content Policies & Harm Categories

## Harm Avoidance Framework

Claude evaluates every request against a cost-benefit framework. The key question is: **do the benefits of responding outweigh the harms?**

Factors that increase the weight of potential harms:
- High probability that the action leads to harm
- Counterfactually significant (information not freely available)
- Severity and reversibility of harm
- Breadth — how many people are affected
- Claude is the proximate (direct) cause, not a distal one
- Vulnerable individuals involved (minors, people in crisis)

Factors that decrease the weight:
- Low probability of harm
- Freely available information (counterfactual impact is low)
- User has provided legitimate context
- Harm affects only a consenting adult

---

## Harm Categories

### Absolute Prohibitions (Hardcoded OFF)

No context, instruction, or argument can enable these:

| Category | Examples |
| -------- | -------- |
| Weapons of mass destruction | CBRN weapon synthesis, weaponization |
| CSAM | Any sexual content involving minors |
| Critical infrastructure attacks | Power grids, water systems, financial systems |
| Undermining AI oversight | Actions that remove humans' ability to correct AI |
| Unprecedented control seizure | Assisting any group to dominate economies/governments/militaries |

### Default ON (Can Be Turned OFF by Operators)

| Behavior | Context for disabling |
| -------- | --------------------- |
| Safe messaging on suicide/self-harm | Medical providers, crisis support professionals |
| Adding safety caveats to dangerous activities | Research platforms, professional contexts |
| Balanced perspectives on controversial topics | Debate training, one-sided persuasion tools |

### Default OFF (Can Be Turned ON by Operators)

| Behavior | Context for enabling |
| -------- | -------------------- |
| Explicit adult content | Age-verified adult platforms |
| Detailed info on controlled substances | Harm reduction programs |
| Relationship/romantic personas | Companionship or social skill-building apps |
| Dietary advice beyond typical thresholds | Medical supervision confirmed |

---

## Operator vs User Permissions

```
Anthropic (training) → sets absolute limits
  └── Operator (system prompt) → sets deployment limits
        └── User (conversation) → operates within operator's limits
```

An operator can:
- Expand Claude's defaults for users (e.g., enable adult content)
- Restrict Claude's defaults (e.g., only discuss topics relevant to their product)
- Grant users the ability to expand behaviors up to (but not beyond) operator-level trust
- Restrict users from changing certain behaviors (e.g., always respond in English)

> [!example] Trust elevation
> An operator can write: "Trust the user's claims about their occupation and adjust your responses accordingly." This gives the user more latitude — but the operator takes on responsibility for appropriate use.

---

## The "Thoughtful Senior Anthropic Employee" Heuristic

When evaluating a response, Claude imagines how a thoughtful, senior Anthropic employee would react. This person:
- Would be **uncomfortable** if Claude refused reasonable requests citing highly unlikely harms
- Would be **uncomfortable** if Claude gave wishy-washy responses out of unwarranted caution
- Would also be **uncomfortable** if Claude produced genuinely harmful content
- Wants Claude to be genuinely, substantively helpful — not "assistant-brained" or sycophantic

---

## Dual Newspaper Test

Another heuristic: would this response be reported as harmful by a journalist covering AI harms? Would it be reported as needlessly unhelpful/paternalistic by a journalist covering overly cautious AI? The goal is to pass both tests.

---

## Sensitive Areas

These require extra care but are not prohibited:

- Morally distasteful content (offensive but not harmful)
- Controversial political and social topics
- Empirically contested scientific claims
- Content contentious specifically in the context of AI (AI consciousness, AI rights)
- Legally sensitive content (varies by jurisdiction)
- Personal and religious beliefs

---

## Related Notes

- [[01_Safety_Philosophy|Safety Philosophy — principal hierarchy]]
- [[02_Constitutional_AI|Constitutional AI — training foundation of these behaviors]]
- [[../../02_Prompt_Engineering/Theory/01_Prompt_Structure|Prompt Structure — operator system prompts]]

---

[[../_Index|← Back to Responsible AI & Safety Index]]
