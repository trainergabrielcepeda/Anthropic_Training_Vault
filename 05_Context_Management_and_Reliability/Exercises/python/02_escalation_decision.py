"""
Exercise 2 — Escalation Decisions via Explicit Criteria (not self-reported confidence)
Domain: Context Management & Reliability (Task 5.2)

Problem this demonstrates:
  Two tempting-but-unreliable escalation mechanisms are self-reported
  confidence scores and sentiment analysis — neither one measures the
  thing that actually matters (does this fall within documented policy
  and available tools?). This exercise implements the reliable
  alternative: an escalation-decision function driven by EXPLICIT
  criteria plus few-shot examples in the system prompt, using forced
  tool use so the decision is a typed, machine-checkable object rather
  than free text.

  It correctly distinguishes:
    - "customer explicitly asked for a human"        -> escalate immediately
    - "complex but covered by policy, agent can act"  -> attempt resolution
    - "policy gap — request isn't covered at all"     -> escalate
"""

import anthropic

client = anthropic.Anthropic()

MODEL = "claude-sonnet-5"  # judgment call between resolve/escalate warrants the stronger model

ESCALATION_SYSTEM_PROMPT = """You are a support-triage assistant. For every customer
message, decide whether to ESCALATE to a human agent or RESOLVE it autonomously.

Escalate when ANY of these are true:
  1. The customer explicitly asks for a human agent, a manager, or to "talk to a person" —
     escalate immediately, even if you believe you could resolve the underlying issue.
  2. The request falls into a genuine POLICY GAP — company policy does not address this
     situation at all (not merely "this is hard"), so you have no rule to apply.
  3. You cannot make meaningful progress (e.g., a required piece of information is
     permanently unavailable, or a dependency is blocked).

Do NOT escalate merely because a case is complex, multi-step, or the customer sounds
frustrated. If the case is fully covered by policy, resolve it — acknowledge frustration
if present, but only escalate if the customer reiterates a preference for a human.

Do NOT use your own confidence level as the escalation signal. Base the decision only
on the three criteria above.

## Examples

Customer: "This is the third time my package has been late, I am extremely frustrated,
can you just fix this?"
-> RESOLVE. Frustrated tone, but the request (repeated late delivery, refund/credit) is
fully covered by standard policy. Acknowledge frustration, then resolve.

Customer: "I don't want to deal with a bot, put me through to an actual agent right now."
-> ESCALATE. Explicit request for a human — escalate immediately regardless of how
straightforward the underlying issue is.

Customer: "Can you match the price I found at a competitor's store? It's $40 cheaper."
-> ESCALATE. Policy defines rules for adjustments on items bought at our own site, but is
silent on competitor price matching entirely. This is a policy gap, not just a hard case.

Customer: "My order arrived damaged, here's a photo. I'd like a replacement."
-> RESOLVE. Standard, policy-covered damage-replacement flow with evidence provided.
"""

ESCALATION_TOOL = [{
    "name": "record_escalation_decision",
    "description": "Record the escalation decision for this customer message.",
    "input_schema": {
        "type": "object",
        "properties": {
            "decision": {"type": "string", "enum": ["ESCALATE", "RESOLVE"]},
            "matched_criterion": {
                "type": "string",
                "enum": [
                    "explicit_human_request",
                    "policy_gap",
                    "no_progress_possible",
                    "none_-_within_policy",
                ]
            },
            "reasoning": {"type": "string", "description": "One sentence justifying the decision."}
        },
        "required": ["decision", "matched_criterion", "reasoning"]
    }
}]


def decide_escalation(customer_message: str) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=ESCALATION_SYSTEM_PROMPT,
        tools=ESCALATION_TOOL,
        tool_choice={"type": "tool", "name": "record_escalation_decision"},
        messages=[{"role": "user", "content": customer_message}]
    )
    tool_block = response.content[0]
    return tool_block.input


# ─────────────────────────────────────────────
# Anti-pattern shown for contrast (NOT used for the real decision)
# ─────────────────────────────────────────────
def unreliable_self_reported_confidence(customer_message: str) -> int:
    """DO NOT USE THIS FOR ROUTING. Included only to show why it's unreliable:
    an agent that is confidently wrong on a hard, undocumented-policy case will
    self-report high confidence and never trigger escalation."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=20,
        system="Rate your confidence (1-10) in handling this support request. Reply with only the number.",
        messages=[{"role": "user", "content": customer_message}]
    )
    try:
        return int(response.content[0].text.strip())
    except ValueError:
        return -1


# ─────────────────────────────────────────────
# Demonstration
# ─────────────────────────────────────────────
TEST_MESSAGES = [
    "Just put me through to a person, I don't want to talk to a bot.",
    "This is a bit complicated but: my order had 3 items, one was wrong, one was late, "
    "and I was double-charged for shipping. Can you sort all of that out?",
    "Can you match the price I saw at a competing store? It's $40 less.",
    "My package never arrived and tracking hasn't updated in 9 days.",
]


def main():
    for msg in TEST_MESSAGES:
        print(f"Customer: {msg}")
        decision = decide_escalation(msg)
        print(f"  -> decision: {decision['decision']} ({decision['matched_criterion']})")
        print(f"     reasoning: {decision['reasoning']}\n")

    print("--- For contrast: the unreliable self-reported-confidence approach ---")
    for msg in TEST_MESSAGES:
        score = unreliable_self_reported_confidence(msg)
        print(f"Customer: {msg[:60]}...  self-reported confidence: {score}/10")
    print(
        "\nNote how self-reported confidence does not reliably track the policy-gap case "
        "(competitor price matching) — the model may rate itself confident there too, "
        "which is exactly why explicit criteria, not confidence, should drive routing."
    )


if __name__ == "__main__":
    main()
