"""
Exercise 3 — Few-Shot Prompting for Output Consistency (Task 4.2)
Domain: Prompt Engineering & Structured Output

Covers:
  - BEFORE: detailed written instructions alone still produce
    inconsistent judgments on ambiguous escalation decisions
  - AFTER: 3 targeted few-shot examples, each with reasoning for why
    one action was chosen over a plausible alternative, on the exact
    ambiguous boundary the task cares about
  - Why this generalizes to a NOVEL case that doesn't match any single
    example verbatim, rather than just memorizing the 3 cases shown
"""

import anthropic

client = anthropic.Anthropic()

# Ambiguous support cases sitting on the "resolve autonomously vs.
# escalate to a human" boundary. None of these is a clean textbook
# case — that's the point; this is exactly where instructions alone
# tend to produce inconsistent judgment.
CASES = [
    "Customer wants a refund for a damaged item and has already "
    "attached a photo showing visible damage. Order is within the "
    "30-day return window.",

    "Customer is requesting a refund on a $2,400 order, citing "
    "'it just doesn't feel right,' with no damage claim and no policy "
    "violation on our side.",

    "Customer's item arrived late due to a carrier delay (not our "
    "fault) and they're asking for a partial shipping refund, which "
    "is explicitly covered by our stated shipping-delay policy.",

    # Novel case — deliberately NOT modeled directly on the few-shot
    # examples below, to test generalization rather than pattern
    # matching against a near-identical example.
    "Customer received the correct item but says the color looks "
    "slightly different from the product photo, and wants a refund "
    "citing 'misleading listing,' though the product page's stated "
    "color matches what shipped.",
]

# ─────────────────────────────────────────────
# BEFORE: detailed instructions, zero-shot
# ─────────────────────────────────────────────
DETAILED_INSTRUCTIONS_ONLY = """You are a support triage assistant. For each
customer message, decide RESOLVE (handle it now, no human needed) or
ESCALATE (route to a human agent).

Resolve autonomously when the situation is clearly covered by policy and
the evidence is straightforward. Escalate when the situation requires
judgment calls, policy exceptions, or is not clearly covered by policy.

Respond with only RESOLVE or ESCALATE, followed by a colon and a one-line
reason."""


def classify_zero_shot(case: str) -> str:
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=60,
        system=DETAILED_INSTRUCTIONS_ONLY,
        messages=[{"role": "user", "content": case}],
    )
    return r.content[0].text.strip()


# ─────────────────────────────────────────────
# AFTER: 3 targeted few-shot examples with reasoning
# ─────────────────────────────────────────────
FEW_SHOT_SYSTEM = """You are a support triage assistant. For each customer
message, decide RESOLVE (handle it now, no human needed) or ESCALATE
(route to a human agent).

Examples:

Message: "My package arrived crushed, photo attached showing the box
caved in. Order is 12 days old."
Reasoning: Damage claim, photo evidence provided, well within return
window — this is exactly what the standard replacement policy covers.
No judgment call needed.
Decision: RESOLVE: damage claim with photo evidence, standard policy covers it.

Message: "I'd like a refund on my $1,800 order. Nothing's wrong with
it, I just changed my mind after the return window closed."
Reasoning: No policy violation and no damage — but the return window
has already closed, so granting this refund would require a POLICY
EXCEPTION, which is a judgment call a human should make, especially
at this order value.
Decision: ESCALATE: refund request outside return window, requires policy exception.

Message: "My order was delayed by the carrier and I'd like the
shipping refund your delay policy promises."
Reasoning: This is explicitly named and covered by an existing written
policy (shipping-delay refund) with a clear, checkable trigger (carrier
delay). No exception or judgment call required.
Decision: RESOLVE: shipping-delay refund is explicitly covered by stated policy.

Respond in the same format: DECISION: reasoning, all on one line."""


def classify_few_shot(case: str) -> str:
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=80,
        system=FEW_SHOT_SYSTEM,
        messages=[{"role": "user", "content": f'Message: "{case}"'}],
    )
    return r.content[0].text.strip()


def main():
    print("=== BEFORE: detailed instructions only (zero-shot) ===\n")
    for case in CASES:
        result = classify_zero_shot(case)
        print(f"- {case[:70]}...")
        print(f"  -> {result}\n")

    print("\n=== AFTER: + 3 targeted few-shot examples with reasoning ===\n")
    for case in CASES:
        result = classify_few_shot(case)
        print(f"- {case[:70]}...")
        print(f"  -> {result}\n")

    print(
        "Notice: the 4th case (color mismatch vs. listing) doesn't match any\n"
        "single few-shot example directly — it tests whether the model learned\n"
        "the underlying PRINCIPLE (is this covered by explicit policy, or does\n"
        "it require a judgment call / exception?) rather than pattern-matching\n"
        "the 3 examples verbatim. Run this a few times and compare how often the\n"
        "zero-shot column flips its answer vs. the few-shot column."
    )


if __name__ == "__main__":
    main()
