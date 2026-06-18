---
tags: [theory, production, evaluation, testing]
topic: "06 - Production & Evaluation"
---

# Evaluation & Testing

## Why Evals Matter

Prompts and models change. Without a systematic evaluation pipeline, you cannot know whether a prompt change improved quality, maintained it, or degraded it.

**Evals answer:** "Does this system do what I want it to do, reliably, across a representative sample of inputs?"

---

## Types of Evaluations

| Type | How It Works | Best For |
| ---- | ------------ | -------- |
| **Exact match** | Compare output to known correct answer | Classification, extraction with deterministic answers |
| **Contains check** | Check if output includes required strings | Format compliance, presence of required elements |
| **LLM-as-judge** | Use Claude to grade output quality | Open-ended generation, reasoning quality |
| **Human eval** | Human raters score outputs | High-stakes tasks, calibrating automated evals |
| **Reference-based** | Compare to a gold-standard reference (ROUGE, BLEU) | Summarization, translation |

---

## Exact Match Eval

```python
def run_classification_eval(test_cases: list[dict]) -> float:
    correct = 0
    for case in test_cases:
        response = claude(
            system=system_prompt,
            user=case["input"]
        )
        prediction = response.strip().upper()
        if prediction == case["expected"]:
            correct += 1
    return correct / len(test_cases)

accuracy = run_classification_eval([
    {"input": "Your app keeps crashing!", "expected": "COMPLAINT"},
    {"input": "How do I reset my password?", "expected": "QUESTION"},
])
print(f"Accuracy: {accuracy:.1%}")
```

---

## LLM-as-Judge

Use a separate Claude call to evaluate the quality of a response. The judge prompt is critical — be explicit about what to score and the rubric.

```python
def llm_judge(question: str, answer: str, criteria: str) -> dict:
    judge_prompt = f"""
You are evaluating an AI assistant's response. Score it on the following criterion:

Criterion: {criteria}

Question: {question}
Answer: {answer}

Respond with a JSON object:
{{
  "score": <integer 1-5>,
  "reasoning": "<one sentence explanation>"
}}
"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": judge_prompt}]
    )
    return json.loads(response.content[0].text)

result = llm_judge(
    question="Explain photosynthesis.",
    answer=model_answer,
    criteria="Factual accuracy — does the answer contain correct information?"
)
print(result)  # {"score": 4, "reasoning": "Accurate but omits the light-dependent reactions."}
```

> [!tip] Use a stronger model as judge
> For important evals, use Sonnet or Opus as the judge even if you use Haiku for production. The judge's quality directly determines eval reliability.

---

## Building an Eval Suite

```python
eval_suite = [
    {
        "id": "test_001",
        "input": "Summarize this document: [...]",
        "criteria": [
            "Covers all main points",
            "Under 100 words",
            "No information fabricated"
        ]
    },
    ...
]

def run_eval_suite(suite: list, system_prompt: str) -> list[dict]:
    results = []
    for case in suite:
        output = run_system(system_prompt, case["input"])
        scores = {
            criterion: llm_judge(case["input"], output, criterion)
            for criterion in case["criteria"]
        }
        results.append({
            "id": case["id"],
            "output": output,
            "scores": scores,
            "avg_score": sum(s["score"] for s in scores.values()) / len(scores)
        })
    return results
```

---

## Regression Testing

Before deploying a prompt change, run the full eval suite on both the old and new prompt:

```python
old_scores = run_eval_suite(suite, old_prompt)
new_scores = run_eval_suite(suite, new_prompt)

for old, new in zip(old_scores, new_scores):
    delta = new["avg_score"] - old["avg_score"]
    if delta < -0.5:
        print(f"REGRESSION on {old['id']}: {delta:+.1f}")
    elif delta > 0.5:
        print(f"IMPROVEMENT on {old['id']}: {delta:+.1f}")
```

---

## Production Monitoring

Beyond offline evals, monitor live traffic:

| Metric | How to Measure |
| ------ | -------------- |
| Latency | Time from request to first token (TTFT) and total |
| Error rate | 4xx/5xx responses per hour |
| Token usage | Input + output tokens per request, trending |
| Refusal rate | Responses containing refusal phrases |
| User satisfaction | Thumbs up/down, CSAT, session continuation rate |

---

## Eval Design Principles

1. **Cover edge cases** — include unusual, ambiguous, and adversarial inputs
2. **Enough samples** — 50+ cases for reliable metrics; 200+ for production confidence
3. **Independent test set** — never optimize prompts against the same cases you use to measure
4. **Multiple criteria** — a single score misses dimension-specific regressions
5. **Version everything** — log the prompt version, model, and eval scores together

---

## Related Notes

- [[01_Caching_and_Batching|Caching & Batching]]
- [[02_Cost_Optimization|Cost Optimization]]
- [[../../02_Prompt_Engineering/Theory/02_Advanced_Techniques|Advanced Techniques — temperature affects eval variance]]

---

[[../_Index|← Back to Production & Evaluation Index]]
