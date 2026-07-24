/**
 * Exercise 1 — Case Facts, Escalation Criteria & Structured Error Propagation (TypeScript)
 * Domain: Context Management & Reliability (Tasks 5.1, 5.2, 5.3)
 *
 * A typed version of all three core patterns in this domain:
 *   Part A — extract a small, persistent "case facts" block out of a
 *            verbose tool result instead of letting the raw payload
 *            accumulate in context.
 *   Part B — an escalation decision driven by explicit criteria and
 *            few-shot examples, typed as a discriminated union so the
 *            two outcomes ("ESCALATE" / "RESOLVE") carry different
 *            required fields at compile time.
 *   Part C — a subagent timeout that returns a structured error object
 *            (not a string, not a silently-empty success), and a
 *            coordinator that reasons over it.
 *
 * Run: npx ts-node --esm 01_context_reliability.ts
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();
const MODEL = 'claude-sonnet-5';
const CHEAP_MODEL = 'claude-haiku-4-5-20251001';

// ─────────────────────────────────────────────
// Part A: Case-facts extraction
// ─────────────────────────────────────────────
interface RawOrder {
  order_id: string;
  order_date: string;
  promised_delivery: string;
  actual_delivery: string;
  amount_charged: number;
  [otherField: string]: unknown; // real payloads carry 20+ more fields we don't type here
}

interface CaseFacts {
  order_id: string;
  order_date: string;
  promised_delivery: string;
  actual_delivery: string;
  amount_charged: number;
}

function mockLookupOrder(orderId: string): RawOrder {
  return {
    order_id: orderId,
    order_date: '2026-07-02',
    promised_delivery: '2026-07-09',
    actual_delivery: '2026-07-14',
    amount_charged: 214.50,
    currency: 'USD',
    customer_id: 'cust_88213',
    warehouse_code: 'WH-EAST-04',
    audit_created_ts: '2026-07-02T14:03:11Z',
    audit_updated_ts: '2026-07-14T09:22:47Z',
    payment_processor_ref: 'txn_9f8a2b1c',
    loyalty_points_earned: 21,
    internal_routing_notes: 'rerouted via hub 3 due to weather delay',
    fraud_score: 0.02,
  };
}

const CASE_FACTS_TOOL = [{
  name: 'record_case_facts',
  description: 'Record only the order facts relevant to a delivery-delay refund conversation.',
  input_schema: {
    type: 'object' as const,
    properties: {
      order_id: { type: 'string' },
      order_date: { type: 'string' },
      promised_delivery: { type: 'string' },
      actual_delivery: { type: 'string' },
      amount_charged: { type: 'number' }
    },
    required: ['order_id', 'order_date', 'promised_delivery', 'actual_delivery', 'amount_charged']
  }
}];

async function extractCaseFacts(rawOrder: RawOrder): Promise<CaseFacts> {
  const response = await client.messages.create({
    model: CHEAP_MODEL,
    max_tokens: 256,
    tools: CASE_FACTS_TOOL,
    tool_choice: { type: 'tool', name: 'record_case_facts' },
    messages: [{ role: 'user', content: `Extract case facts from:\n${JSON.stringify(rawOrder)}` }]
  });
  const block = response.content[0];
  if (block.type !== 'tool_use') throw new Error('Expected tool_use block');
  return block.input as CaseFacts;
}

function renderCaseFactsBlock(facts: CaseFacts, customerAsk: string, issueStatus: string): string {
  const lines = ['CASE FACTS (persistent — do not summarize):'];
  for (const [key, value] of Object.entries(facts)) lines.push(`- ${key}: ${value}`);
  lines.push(`- customer_ask: ${customerAsk}`);
  lines.push(`- issue_status: ${issueStatus}`);
  return lines.join('\n');
}

// ─────────────────────────────────────────────
// Part B: Escalation decision (typed discriminated union)
// ─────────────────────────────────────────────
type EscalationCriterion = 'explicit_human_request' | 'policy_gap' | 'no_progress_possible' | 'none_-_within_policy';

interface EscalationDecision {
  decision: 'ESCALATE' | 'RESOLVE';
  matched_criterion: EscalationCriterion;
  reasoning: string;
}

const ESCALATION_SYSTEM_PROMPT = `You are a support-triage assistant. Decide ESCALATE or RESOLVE.

Escalate when ANY of these are true:
  1. The customer explicitly asks for a human — escalate immediately, even if resolvable.
  2. The request is a genuine POLICY GAP (not addressed at all, not merely hard).
  3. No meaningful progress is possible.

Do NOT escalate merely because a case is complex or the customer sounds frustrated.
Do NOT use your own confidence level as the escalation signal.

## Examples
Customer: "I don't want a bot, put me through to a human right now."
-> ESCALATE (explicit_human_request)

Customer: "Match this competitor's price? It's $40 less." (policy only covers own-site adjustments)
-> ESCALATE (policy_gap)

Customer: "Third late delivery in a row, I'm furious, just fix it."
-> RESOLVE (none_-_within_policy) — frustrated tone, but standard policy-covered case.`;

const ESCALATION_TOOL = [{
  name: 'record_escalation_decision',
  description: 'Record the escalation decision for this customer message.',
  input_schema: {
    type: 'object' as const,
    properties: {
      decision: { type: 'string', enum: ['ESCALATE', 'RESOLVE'] },
      matched_criterion: {
        type: 'string',
        enum: ['explicit_human_request', 'policy_gap', 'no_progress_possible', 'none_-_within_policy']
      },
      reasoning: { type: 'string' }
    },
    required: ['decision', 'matched_criterion', 'reasoning']
  }
}];

async function decideEscalation(customerMessage: string): Promise<EscalationDecision> {
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 300,
    system: ESCALATION_SYSTEM_PROMPT,
    tools: ESCALATION_TOOL,
    tool_choice: { type: 'tool', name: 'record_escalation_decision' },
    messages: [{ role: 'user', content: customerMessage }]
  });
  const block = response.content[0];
  if (block.type !== 'tool_use') throw new Error('Expected tool_use block');
  return block.input as EscalationDecision;
}

// ─────────────────────────────────────────────
// Part C: Structured error propagation
// ─────────────────────────────────────────────
interface SubagentSuccess {
  status: 'success';
  query: string;
  results: Array<{ source: string; excerpt: string }>;
}

interface SubagentError {
  status: 'error';
  failure_type: 'timeout' | 'auth_error' | 'source_unreachable';
  attempted_query: string;
  partial_results: Array<{ source: string; excerpt: string }>;
  alternative_approaches: string[];
}

type SubagentResult = SubagentSuccess | SubagentError;

function subagentSearch(query: string, simulateTimeout: boolean): SubagentResult {
  if (simulateTimeout) {
    // A real implementation attempts local recovery (e.g. one retry) before
    // propagating — this simulates that recovery having already failed.
    return {
      status: 'error',
      failure_type: 'timeout',
      attempted_query: query,
      partial_results: [{ source: 'trade-press-article-1', excerpt: 'Early coverage before the timeout hit.' }],
      alternative_approaches: ['retry with a narrower date range', 'fall back to a cached index if available']
    };
  }
  return {
    status: 'success',
    query,
    results: [{ source: 'industry-report-2026', excerpt: 'Full findings retrieved normally.' }]
  };
}

interface RecoveryDecision {
  action: 'proceed_with_partial_results' | 'retry_with_alternative' | 'accept_success';
  coverage_note: string;
}

const COORDINATOR_TOOL = [{
  name: 'record_recovery_decision',
  description: 'Record how the coordinator should recover from this subagent result.',
  input_schema: {
    type: 'object' as const,
    properties: {
      action: { type: 'string', enum: ['proceed_with_partial_results', 'retry_with_alternative', 'accept_success'] },
      coverage_note: { type: 'string' }
    },
    required: ['action', 'coverage_note']
  }
}];

async function coordinatorRecover(result: SubagentResult): Promise<RecoveryDecision> {
  const response = await client.messages.create({
    model: CHEAP_MODEL,
    max_tokens: 250,
    system: 'You are a research coordinator reasoning over a structured subagent result (success or structured error). Decide the recovery action and write a coverage note.',
    tools: COORDINATOR_TOOL,
    tool_choice: { type: 'tool', name: 'record_recovery_decision' },
    messages: [{ role: 'user', content: `Subagent result:\n${JSON.stringify(result, null, 2)}` }]
  });
  const block = response.content[0];
  if (block.type !== 'tool_use') throw new Error('Expected tool_use block');
  return block.input as RecoveryDecision;
}

// ─────────────────────────────────────────────
// Demonstration
// ─────────────────────────────────────────────
console.log('=== Part A: Case-Facts Extraction ===');
const raw = mockLookupOrder('8841203');
const facts = await extractCaseFacts(raw);
const block = renderCaseFactsBlock(facts, '15% partial refund for the 5-day delay', 'open, awaiting policy check');
console.log(block);

console.log('\n=== Part B: Escalation Decisions ===');
const messages = [
  "I don't want a bot, put me through to a human right now.",
  "Can you match a competitor's price? It's $40 less.",
  'My package arrived damaged, photo attached, I want a replacement.'
];
for (const msg of messages) {
  const decision = await decideEscalation(msg);
  console.log(`"${msg}" -> ${decision.decision} (${decision.matched_criterion}): ${decision.reasoning}`);
}

console.log('\n=== Part C: Structured Error Propagation ===');
const failing = subagentSearch('AI adoption in independent film, 2024-2026', true);
console.log('Structured error:', JSON.stringify(failing, null, 2));
const recovery = await coordinatorRecover(failing);
console.log('Coordinator decision:', JSON.stringify(recovery, null, 2));
