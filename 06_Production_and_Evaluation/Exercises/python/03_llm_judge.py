"""
Exercise 3 — LLM-as-Judge Evaluation
Topic: Production & Evaluation

Covers:
  - Designing a judge prompt with a scoring rubric
  - Running an eval suite with multiple criteria
  - Detecting regressions between two system prompts
"""

import json
import anthropic

client = anthropic.Anthropic()


# ─────────────────────────────────────────────
# System Under Test
# ─────────────────────────────────────────────
PROMPT_V1 = "You are a helpful assistant. Answer the user's question."
PROMPT_V2 = (
    "You are a helpful assistant. Answer the user's question clearly and concisely. "
    "Use bullet points when listing multiple items. Limit responses to 3 sentences max."
)

TEST_QUESTIONS = [
    "What are the benefits of exercise?",
    "How does a computer CPU work?",
    "What should I know before traveling to Japan?",
]


def generate_answer(system_prompt: str, question: str) -> str:
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=system_prompt,
        messages=[{"role": "user", "content": question}]
    )
    return r.content[0].text


# ─────────────────────────────────────────────
# LLM-as-Judge
# ─────────────────────────────────────────────
def llm_judge(question: str, answer: str, criterion: str) -> dict:
    judge_prompt = f"""You are evaluating an AI assistant's response.

Criterion: {criterion}

Question asked: {question}

Answer to evaluate:
{answer}

Score the answer on this criterion from 1 to 5:
1 = Very poor
2 = Below average
3 = Adequate
4 = Good
5 = Excellent

Respond with a JSON object only:
{{"score": <integer 1-5>, "reasoning": "<one sentence>"}}"""

    r = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=128,
        messages=[{"role": "user", "content": judge_prompt}]
    )
    try:
        return json.loads(r.content[0].text)
    except json.JSONDecodeError:
        return {"score": 0, "reasoning": "Judge failed to produce valid JSON"}


CRITERIA = [
    "Factual accuracy — does the answer contain correct information?",
    "Conciseness — is the answer appropriately brief without omitting key points?",
    "Clarity — is the answer easy to understand?",
]


# ─────────────────────────────────────────────
# Run Eval Suite
# ─────────────────────────────────────────────
def run_eval(system_prompt: str, label: str) -> list[dict]:
    print(f"\n{'─'*50}")
    print(f"Evaluating: {label}")
    print('─'*50)
    results = []

    for question in TEST_QUESTIONS:
        answer = generate_answer(system_prompt, question)
        scores = {}
        for criterion in CRITERIA:
            judgment = llm_judge(question, answer, criterion)
            scores[criterion[:30]] = judgment

        avg = sum(j["score"] for j in scores.values()) / len(scores)
        results.append({"question": question, "answer": answer, "scores": scores, "avg": avg})

        print(f"\nQ: {question[:60]}")
        print(f"   Avg score: {avg:.1f}/5")
        for c, j in scores.items():
            print(f"   {c}: {j['score']}/5 — {j['reasoning'][:60]}")

    return results


# ─────────────────────────────────────────────
# Regression Detection
# ─────────────────────────────────────────────
def detect_regressions(v1_results: list, v2_results: list):
    print("\n\n=== Regression Report: V1 vs V2 ===")
    print(f"{'Question':<45} {'V1 avg':>8} {'V2 avg':>8} {'Delta':>8}")
    print("─" * 75)

    for r1, r2 in zip(v1_results, v2_results):
        delta = r2["avg"] - r1["avg"]
        flag = "▲ IMPROVED" if delta > 0.3 else ("▼ REGRESSION" if delta < -0.3 else "  unchanged")
        q = r1["question"][:44]
        print(f"{q:<45} {r1['avg']:>8.1f} {r2['avg']:>8.1f} {delta:>+7.1f}  {flag}")


if __name__ == "__main__":
    v1_results = run_eval(PROMPT_V1, "Prompt V1 (generic)")
    v2_results = run_eval(PROMPT_V2, "Prompt V2 (structured)")
    detect_regressions(v1_results, v2_results)
