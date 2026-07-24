/**
 * Exercise 1 — Case-Facts Extraction Pattern (JavaScript)
 * Domain: Context Management & Reliability (Task 5.1)
 *
 * A verbose tool result (25+ fields) is trimmed, immediately after the
 * call returns, into a small persistent "case facts" block. That block
 * — not the raw payload — is what gets re-injected into every
 * subsequent prompt, kept outside any summarized conversation history.
 *
 * Run: node 01_case_facts.js
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();
const MODEL = 'claude-haiku-4-5-20251001';

// ─────────────────────────────────────────────
// Simulated backend: a verbose order lookup
// ─────────────────────────────────────────────
function mockLookupOrder(orderId) {
  return {
    order_id: orderId,
    order_date: '2026-07-02',
    promised_delivery: '2026-07-09',
    actual_delivery: '2026-07-14',
    amount_charged: 214.50,
    currency: 'USD',
    customer_id: 'cust_88213',
    customer_email: 'j.rivera@example.com',
    shipping_carrier: 'FastFreight',
    warehouse_code: 'WH-EAST-04',
    picking_batch_id: 'PB-2026-07-02-0091',
    audit_created_ts: '2026-07-02T14:03:11Z',
    audit_updated_ts: '2026-07-14T09:22:47Z',
    payment_method: 'visa_ending_4471',
    payment_processor_ref: 'txn_9f8a2b1c',
    loyalty_points_earned: 21,
    gift_wrap: false,
    internal_routing_notes: 'rerouted via hub 3 due to weather delay',
    sku_list: ['SKU-1123', 'SKU-1124', 'SKU-1125'],
    tax_amount: 17.16,
    fraud_score: 0.02,
    return_window_days: 30,
    // ... a real payload would keep going for another 15-20 fields
  };
}

// ─────────────────────────────────────────────
// Forced extraction: only the fields relevant to THIS conversation
// ─────────────────────────────────────────────
const CASE_FACTS_TOOL = [{
  name: 'record_case_facts',
  description: 'Record only the order facts relevant to a delivery-delay refund conversation. Ignore all other fields.',
  input_schema: {
    type: 'object',
    properties: {
      order_id: { type: 'string' },
      order_date: { type: 'string', description: 'YYYY-MM-DD' },
      promised_delivery: { type: 'string', description: 'YYYY-MM-DD' },
      actual_delivery: { type: 'string', description: 'YYYY-MM-DD' },
      amount_charged: { type: 'number' }
    },
    required: ['order_id', 'order_date', 'promised_delivery', 'actual_delivery', 'amount_charged']
  }
}];

async function extractCaseFacts(rawOrder) {
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 256,
    tools: CASE_FACTS_TOOL,
    tool_choice: { type: 'tool', name: 'record_case_facts' },
    messages: [{
      role: 'user',
      content: `Extract the delivery-delay-relevant case facts from this order record:\n${JSON.stringify(rawOrder)}`
    }]
  });
  return response.content[0].input;
}

function renderCaseFactsBlock(facts, customerAsk, issueStatus) {
  const lines = ['CASE FACTS (persistent — do not summarize):'];
  for (const [key, value] of Object.entries(facts)) {
    lines.push(`- ${key}: ${value}`);
  }
  lines.push(`- customer_ask: ${customerAsk}`);
  lines.push(`- issue_status: ${issueStatus}`);
  return lines.join('\n');
}

// ─────────────────────────────────────────────
// Demonstration
// ─────────────────────────────────────────────
async function main() {
  console.log('=== Step 1: Verbose raw tool result ===');
  const raw = mockLookupOrder('8841203');
  console.log(`${Object.keys(raw).length} fields returned by the tool call.\n`);

  console.log('=== Step 2: Extract only the relevant fields ===');
  const facts = await extractCaseFacts(raw);
  console.log(JSON.stringify(facts, null, 2));

  console.log('\n=== Step 3: Persistent case-facts block ===');
  const block = renderCaseFactsBlock(
    facts,
    '15% partial refund for the 5-day delivery delay',
    'open, awaiting policy check'
  );
  console.log(block);

  console.log('\n=== Step 4: Using the block in a follow-up turn ===');
  const followUp = await client.messages.create({
    model: MODEL,
    max_tokens: 200,
    system: `You are a support agent. Use ONLY the case facts below to answer. Do not invent details not present in the case facts.\n\n${block}`,
    messages: [{ role: 'user', content: 'How many days late was this delivery?' }]
  });
  console.log(followUp.content[0].text);
}

await main();
