/**
 * Exercise 2 — Few-Shot Prompting for Output Consistency (Task 4.2)
 * Domain: Prompt Engineering & Structured Output
 *
 * BEFORE: detailed written instructions alone, zero-shot, on ambiguous
 *   escalation-decision cases.
 * AFTER: 3 targeted few-shot examples, each with stated reasoning for
 *   why one action was chosen over a plausible alternative.
 * A 4th, novel case (not modeled directly on any example) checks
 * whether the model generalized the underlying decision principle
 * rather than pattern-matching the examples verbatim.
 *
 * Run: node 02_few_shot_consistency.js
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const CASES = [
  'Customer wants a refund for a damaged item and has already attached ' +
    'a photo showing visible damage. Order is within the 30-day return window.',

  "Customer is requesting a refund on a $2,400 order, citing 'it just " +
    "doesn't feel right,' with no damage claim and no policy violation on our side.",

  "Customer's item arrived late due to a carrier delay (not our fault) " +
    'and they are asking for a partial shipping refund, which is explicitly ' +
    'covered by our stated shipping-delay policy.',

  // Novel case, generalization check.
  'Customer received the correct item but says the color looks slightly ' +
    "different from the product photo, and wants a refund citing 'misleading " +
    "listing,' though the product page's stated color matches what shipped."
];

const DETAILED_INSTRUCTIONS_ONLY = `You are a support triage assistant. For each
customer message, decide RESOLVE (handle it now, no human needed) or
ESCALATE (route to a human agent).

Resolve autonomously when the situation is clearly covered by policy and
the evidence is straightforward. Escalate when the situation requires
judgment calls, policy exceptions, or is not clearly covered by policy.

Respond with only RESOLVE or ESCALATE, followed by a colon and a one-line
reason.`;

const FEW_SHOT_SYSTEM = `You are a support triage assistant. For each customer
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

Respond in the same format: DECISION: reasoning, all on one line.`;

async function classifyZeroShot(caseText) {
  const r = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 60,
    system: DETAILED_INSTRUCTIONS_ONLY,
    messages: [{ role: 'user', content: caseText }]
  });
  return r.content[0].text.trim();
}

async function classifyFewShot(caseText) {
  const r = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 80,
    system: FEW_SHOT_SYSTEM,
    messages: [{ role: 'user', content: `Message: "${caseText}"` }]
  });
  return r.content[0].text.trim();
}

async function main() {
  console.log('=== BEFORE: detailed instructions only (zero-shot) ===\n');
  for (const c of CASES) {
    const result = await classifyZeroShot(c);
    console.log(`- ${c.slice(0, 70)}...`);
    console.log(`  -> ${result}\n`);
  }

  console.log('\n=== AFTER: + 3 targeted few-shot examples with reasoning ===\n');
  for (const c of CASES) {
    const result = await classifyFewShot(c);
    console.log(`- ${c.slice(0, 70)}...`);
    console.log(`  -> ${result}\n`);
  }

  console.log(
    'Notice: the 4th case (color mismatch vs. listing) is not modeled directly\n' +
    'on any few-shot example — it tests whether the model learned the underlying\n' +
    'PRINCIPLE (explicit policy coverage vs. a judgment call) rather than matching\n' +
    'examples verbatim.'
  );
}

main();
