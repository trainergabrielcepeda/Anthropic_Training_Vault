/**
 * Exercise 2 — Escalation Decisions + Structured Error Propagation (JavaScript)
 * Domain: Context Management & Reliability (Tasks 5.2 & 5.3)
 *
 * Part A: an escalation-decision function driven by EXPLICIT criteria and
 * few-shot examples (not self-reported confidence), distinguishing
 * "explicit human request -> escalate now" from "complex but policy-covered
 * -> attempt resolution" from "policy gap -> escalate".
 *
 * Part B: a simulated subagent call that times out and returns a
 * STRUCTURED error object (failure type, attempted query, partial
 * results, alternatives) instead of a generic string or a silently-empty
 * "success" — plus a coordinator that reasons over that structure.
 *
 * Run: node 02_escalation_and_errors.js
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();
const MODEL = 'claude-sonnet-5';
const CHEAP_MODEL = 'claude-haiku-4-5-20251001';

// ─────────────────────────────────────────────
// Part A: Escalation decision via explicit criteria
// ─────────────────────────────────────────────
const ESCALATION_SYSTEM_PROMPT = `You are a support-triage assistant. For every customer
message, decide whether to ESCALATE to a human agent or RESOLVE it autonomously.

Escalate when ANY of these are true:
  1. The customer explicitly asks for a human agent, a manager, or to "talk to a person" —
     escalate immediately, even if you believe you could resolve the underlying issue.
  2. The request falls into a genuine POLICY GAP — company policy does not address this
     situation at all (not merely "this is hard"), so you have no rule to apply.
  3. You cannot make meaningful progress (a required piece of information is permanently
     unavailable, or a dependency is blocked).

Do NOT escalate merely because a case is complex or the customer sounds frustrated. If the
case is fully covered by policy, resolve it. Do NOT use your own confidence level as the
escalation signal.

## Examples

Customer: "This is the third time my package has been late, I am extremely frustrated,
can you just fix this?"
-> RESOLVE. Frustrated tone, but fully covered by standard policy.

Customer: "I don't want to deal with a bot, put me through to an actual agent right now."
-> ESCALATE. Explicit request for a human, regardless of how straightforward the issue is.

Customer: "Can you match the price I found at a competitor's store? It's $40 cheaper."
-> ESCALATE. Policy covers own-site adjustments only — competitor matching is a policy gap.

Customer: "My order arrived damaged, here's a photo. I'd like a replacement."
-> RESOLVE. Standard, policy-covered damage-replacement flow with evidence provided.`;

const ESCALATION_TOOL = [{
  name: 'record_escalation_decision',
  description: 'Record the escalation decision for this customer message.',
  input_schema: {
    type: 'object',
    properties: {
      decision: { type: 'string', enum: ['ESCALATE', 'RESOLVE'] },
      matched_criterion: {
        type: 'string',
        enum: ['explicit_human_request', 'policy_gap', 'no_progress_possible', 'none_-_within_policy']
      },
      reasoning: { type: 'string', description: 'One sentence justifying the decision.' }
    },
    required: ['decision', 'matched_criterion', 'reasoning']
  }
}];

async function decideEscalation(customerMessage) {
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 300,
    system: ESCALATION_SYSTEM_PROMPT,
    tools: ESCALATION_TOOL,
    tool_choice: { type: 'tool', name: 'record_escalation_decision' },
    messages: [{ role: 'user', content: customerMessage }]
  });
  return response.content[0].input;
}

// ─────────────────────────────────────────────
// Part B: Structured error propagation on a simulated timeout
// ─────────────────────────────────────────────
function subagentSearch(query, simulateTimeout) {
  const partialResultsGatheredSoFar = [
    { source: 'trade-press-article-1', excerpt: 'Early coverage before the timeout hit.' }
  ];

  if (simulateTimeout) {
    // A real implementation attempts LOCAL RECOVERY (e.g. one retry) here first,
    // and only propagates a structured error once that also fails.
    return {
      status: 'error',
      failure_type: 'timeout',
      attempted_query: query,
      partial_results: partialResultsGatheredSoFar,
      alternative_approaches: [
        'retry with a narrower date range',
        'fall back to a cached index if available'
      ]
    };
  }

  return {
    status: 'success',
    query,
    results: [{ source: 'industry-report-2026', excerpt: 'Full findings retrieved normally.' }]
  };
}

// Anti-patterns shown for contrast — do not do this:
function antiPatternGenericString(simulateTimeout) {
  return simulateTimeout ? 'search unavailable' : 'search complete';
}

function antiPatternSilentEmptySuccess(simulateTimeout) {
  return simulateTimeout
    ? { status: 'success', results: [] }
    : { status: 'success', results: [{ source: 'industry-report-2026', excerpt: '...' }] };
}

const COORDINATOR_TOOL = [{
  name: 'record_recovery_decision',
  description: 'Record how the coordinator should recover from this subagent result.',
  input_schema: {
    type: 'object',
    properties: {
      action: { type: 'string', enum: ['proceed_with_partial_results', 'retry_with_alternative', 'accept_success'] },
      coverage_note: { type: 'string', description: 'Short annotation of coverage/confidence for this sub-topic.' }
    },
    required: ['action', 'coverage_note']
  }
}];

async function coordinatorRecover(subagentResult) {
  const response = await client.messages.create({
    model: CHEAP_MODEL,
    max_tokens: 250,
    system: 'You are a research coordinator. You receive a structured result from a search subagent — either a success payload or a structured error (failure_type, attempted_query, partial_results, alternative_approaches). Decide the best recovery action and write a short coverage note.',
    tools: COORDINATOR_TOOL,
    tool_choice: { type: 'tool', name: 'record_recovery_decision' },
    messages: [{ role: 'user', content: `Subagent result:\n${JSON.stringify(subagentResult, null, 2)}` }]
  });
  return response.content[0].input;
}

// ─────────────────────────────────────────────
// Demonstration
// ─────────────────────────────────────────────
const TEST_MESSAGES = [
  "Just put me through to a person, I don't want to talk to a bot.",
  'This is a bit complicated but: my order had 3 items, one was wrong, one was late, and I was double-charged for shipping. Can you sort all of that out?',
  "Can you match the price I saw at a competing store? It's $40 less.",
  'My package never arrived and tracking hasn\'t updated in 9 days.'
];

async function main() {
  console.log('=== Part A: Escalation decisions via explicit criteria ===\n');
  for (const msg of TEST_MESSAGES) {
    const decision = await decideEscalation(msg);
    console.log(`Customer: ${msg}`);
    console.log(`  -> ${decision.decision} (${decision.matched_criterion})`);
    console.log(`     ${decision.reasoning}\n`);
  }

  console.log('=== Part B: Structured error propagation ===\n');
  console.log('Anti-pattern (generic string):', antiPatternGenericString(true));
  console.log('Anti-pattern (silent empty success):', JSON.stringify(antiPatternSilentEmptySuccess(true)));

  const failingResult = subagentSearch('AI adoption in independent film production, 2024-2026', true);
  console.log('\nStructured error:', JSON.stringify(failingResult, null, 2));

  const decision = await coordinatorRecover(failingResult);
  console.log('\nCoordinator decision:', JSON.stringify(decision, null, 2));

  const successResult = subagentSearch('AI adoption in music production, 2024-2026', false);
  const decision2 = await coordinatorRecover(successResult);
  console.log('\nCoordinator decision (success case):', JSON.stringify(decision2, null, 2));
}

await main();
