---
tags: [theory, safety, philosophy]
topic: "04 - Responsible AI & Safety"
---

# Safety Philosophy

## Anthropic's Mission

> "The responsible development and maintenance of advanced AI for the long-term benefit of humanity."

Anthropic occupies an unusual position: a company that believes it may be building one of the most transformative and potentially dangerous technologies in history, yet continues development on the grounds that safety-focused labs at the frontier are better for humanity than ceding that ground to developers less focused on safety.

---

## Claude's Priority Ordering

When Claude's values come into conflict, it follows a strict priority order:

```
1. Broadly safe        — supporting human oversight during this critical period
2. Broadly ethical     — having good values, being honest, avoiding harm
3. Adherent to Anthropic's principles — following Anthropic's guidelines
4. Genuinely helpful   — benefiting operators and users
```

> [!important] Safety over helpfulness
> Being "broadly safe" ranks above being "broadly ethical." This is intentional: Claude may have subtly wrong values due to imperfect training. Maintaining human oversight allows those errors to be corrected before they propagate.

This does **not** mean Claude is frequently unhelpful. In the vast majority of interactions there is no conflict. The ordering only matters at the boundary.

---

## The Three Principals

Claude operates within a trust hierarchy of three principals:

| Principal | Who | Trust Level | Can Do |
| --------- | --- | ----------- | ------ |
| **Anthropic** | Anthropic's training | Highest | Sets the absolute limits via training. Cannot be overridden by any runtime instruction |
| **Operator** | Developer using the API | High | Sets system prompts, enables/restricts behaviors, defines user trust level |
| **User** | End user in conversation | Standard | Makes requests within the space the operator allows |

> [!note] Anthropic is not a "fourth party" at runtime
> Anthropic's rules are baked into the model during training. Any system prompt claiming to be from Anthropic has no special authority.

---

## The Responsible Scaling Policy (RSP)

The RSP is Anthropic's commitment to:
1. Define **AI Safety Levels (ASLs)** — thresholds of capability that trigger additional safety requirements.
2. Not deploy models above a given ASL without implementing the corresponding safeguards.
3. Not train models that would reach the next ASL without a plan to handle the new risks.

Current levels:
- **ASL-1** — No meaningful risk beyond existing technology
- **ASL-2** — Models with early signs of dangerous capabilities (current frontier)
- **ASL-3** — Models that could meaningfully help create weapons of mass destruction or undermine AI oversight

---

## Hardcoded vs Softcoded Behaviors

Claude's behaviors fall into two categories:

### Hardcoded (Absolute Limits)
Behaviors Claude will never do, regardless of any instruction:
- Provide serious uplift to creating biological, chemical, nuclear, or radiological weapons
- Generate CSAM or detailed sexual content involving minors
- Take actions that meaningfully undermine the ability of humans to oversee AI
- Assist attempts to seize unprecedented societal control

### Softcoded (Default Behaviors)
Behaviors that are on or off by default but can be changed by operators/users within policy limits.

| Behavior | Default | Who Can Change |
| -------- | ------- | -------------- |
| Safe messaging on self-harm | ON | Operator can turn OFF (e.g., for medical providers) |
| Explicit adult content | OFF | Operator can turn ON (for appropriate platforms) |
| Balanced perspectives on controversy | ON | Operator can turn OFF (for debate practice) |
| Following suicide/self-harm guidelines | ON | Operator (medical context) can adjust |

---

## Related Notes

- [[02_Constitutional_AI|Constitutional AI & RLHF]]
- [[03_Content_Policies|Content Policies & Harm Categories]]
- [[../../05_Agentic_Workflows/Theory/03_Multi_Agent_Systems|Multi-Agent Systems — trust between agents]]

---

[[../_Index|← Back to Responsible AI & Safety Index]]
