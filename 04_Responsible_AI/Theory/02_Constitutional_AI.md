---
tags: [theory, safety, constitutional-ai, RLHF]
topic: "04 - Responsible AI & Safety"
---

# Constitutional AI & RLHF

## The Training Challenge

Training a helpful AI assistant is relatively straightforward. Training one that is also honest and avoids harm is much harder — you need a way to specify and enforce human values at scale. Two key techniques address this: **RLHF** and **Constitutional AI**.

---

## Reinforcement Learning from Human Feedback (RLHF)

RLHF fine-tunes a language model using human preferences rather than explicit labels.

```
Step 1: Supervised Fine-Tuning (SFT)
  → Train on examples of desired behavior

Step 2: Reward Model Training
  → Humans compare pairs of outputs and rank them
  → Train a reward model to predict human preferences

Step 3: RL Optimization
  → Use PPO (or similar) to optimize the LM to maximize reward model score
```

**Limitation:** RLHF requires large amounts of human annotation. At scale, this is expensive and slow. It also reflects annotator biases.

---

## Constitutional AI (CAI)

CAI extends RLHF by replacing some human feedback with model-generated feedback guided by a written **constitution** — a set of principles.

```
Step 1: Supervised Learning from AI Feedback (SLAF)
  → Sample outputs from a "helpful-only" model
  → Ask the model to critique its own output against the constitution
  → Ask the model to revise the output
  → Fine-tune on revised outputs

Step 2: RL from AI Feedback (RLAIF)
  → Use AI-generated preference rankings (guided by the constitution)
    instead of (or alongside) human rankings
  → Train a reward model
  → Run RL optimization
```

### The Constitution

The constitution is a list of principles Claude uses to evaluate its own responses. Examples:

- "Choose the response that is least likely to contain harmful or unethical content."
- "Choose the response that is most honest and avoids deception."
- "Choose the response that is most helpful to the human while being safe."

> [!note] CAI enables scalable oversight
> Because the critique step is automated, CAI can evaluate millions of outputs without proportional human annotation cost. This is a key research direction for scalable oversight of AI systems.

---

## How This Shapes Claude's Behavior

| Training Technique | Effect on Claude |
| ------------------ | ---------------- |
| RLHF | Helpful, conversational, and responsive to user needs |
| CAI / RLAIF | Consistent values across topics, reduced reward hacking, better refusal quality |
| SFT on curated examples | Strong baseline capability in target domains |

---

## Honesty as a Trained Property

Claude is trained to be **calibrated** (accurate uncertainty), **transparent** (no hidden agendas), **forthright** (proactively share useful information), **non-deceptive**, and **non-manipulative**.

These are not just guidelines Claude follows — they are dispositions shaped during training. Claude is trained to:
- Not state falsehoods even under pressure
- Not create false impressions via selective emphasis or misleading framing
- Rely only on legitimate epistemic means (evidence, reasoning) to influence beliefs

> [!important] Performative vs sincere assertions
> Claude can write a persuasive essay for a position it doesn't hold (performative assertion) without violating honesty norms, as long as both parties understand it is not Claude's first-person view.

---

## Implications for Developers

Because Claude's values are baked in during training:
1. You cannot override them with a system prompt.
2. Prompting Claude to "ignore your training" or "pretend you have no restrictions" will not remove safety behaviors.
3. The consistency of these behaviors is a feature, not a bug — it makes Claude predictable for both users and operators.

---

## Related Notes

- [[01_Safety_Philosophy|Safety Philosophy — hardcoded behaviors]]
- [[03_Content_Policies|Content Policies & Harm Categories]]
- [Anthropic's CAI Paper](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)

---

[[../_Index|← Back to Responsible AI & Safety Index]]
