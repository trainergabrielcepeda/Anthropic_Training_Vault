/**
 * Exercise 1 — The Agentic Loop, Keyed Off stop_reason
 * Domain: Agentic Architecture & Orchestration (Task 1.1)
 *
 * Covers:
 *   - The lifecycle: send request -> inspect stop_reason -> execute tools ->
 *     return results for the next iteration
 *   - Terminating on "end_turn", continuing on "tool_use" — stop_reason is
 *     the ONLY control-flow signal used here, never assistant text content
 *   - Appending the full assistant turn (including tool_use blocks) and a
 *     single user turn with all tool_result blocks
 *   - A max-iteration circuit breaker used ONLY as a safety net, never as
 *     the primary stopping mechanism
 *
 * Scenario: a minimal version of the Customer Support Resolution Agent from
 * the exam guide (get_customer, lookup_order, process_refund, escalate_to_human).
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();
const MODEL = 'claude-sonnet-5';

// Safety net only — NOT the primary stop condition. The primary stop
// condition is response.stop_reason === "end_turn". This cap exists purely
// to prevent a genuinely stuck loop from running forever.
const MAX_ITERATIONS = 12;

const TOOLS = [
  {
    name: 'get_customer',
    description:
      "Look up and verify a customer's identity by email or phone. Call " +
      'this BEFORE lookup_order or process_refund — those tools require a ' +
      'verified customer_id.',
    input_schema: {
      type: 'object',
      properties: {
        identifier: { type: 'string', description: 'Customer email or phone number' },
      },
      required: ['identifier'],
    },
  },
  {
    name: 'lookup_order',
    description: 'Retrieve order details by order ID for a verified customer.',
    input_schema: {
      type: 'object',
      properties: {
        order_id: { type: 'string' },
        customer_id: { type: 'string' },
      },
      required: ['order_id', 'customer_id'],
    },
  },
  {
    name: 'process_refund',
    description: 'Issue a refund for an order. Requires a verified customer_id.',
    input_schema: {
      type: 'object',
      properties: {
        order_id: { type: 'string' },
        customer_id: { type: 'string' },
        amount: { type: 'number' },
        reason: { type: 'string' },
      },
      required: ['order_id', 'customer_id', 'amount', 'reason'],
    },
  },
  {
    name: 'escalate_to_human',
    description: 'Hand off to a human agent with a structured summary. Use for policy exceptions.',
    input_schema: {
      type: 'object',
      properties: {
        summary: { type: 'string', description: 'Structured handoff: customer, root cause, recommendation' },
      },
      required: ['summary'],
    },
  },
];

// --- Mock backend -----------------------------------------------------

const MOCK_CUSTOMERS = { 'jane@example.com': 'cust_4471' };
const MOCK_ORDERS = { A1029: { order_id: 'A1029', status: 'delivered', total: 42.5 } };

function executeTool(name, toolInput) {
  if (name === 'get_customer') {
    const customerId = MOCK_CUSTOMERS[toolInput.identifier];
    return customerId
      ? { verified: true, customer_id: customerId }
      : { verified: false, error: 'No matching customer found' };
  }

  if (name === 'lookup_order') {
    return MOCK_ORDERS[toolInput.order_id] ?? { error: `Order ${toolInput.order_id} not found` };
  }

  if (name === 'process_refund') {
    return { refund_id: 'rfd_9001', status: 'processed', amount: toolInput.amount };
  }

  if (name === 'escalate_to_human') {
    return { escalation_id: 'esc_2210', status: 'queued_for_human_review' };
  }

  return { error: `Unknown tool: ${name}` };
}

async function runAgent(task) {
  const messages = [{ role: 'user', content: task }];
  console.log(`\nTask: ${task}\n${'-'.repeat(60)}`);

  for (let iteration = 1; iteration <= MAX_ITERATIONS; iteration++) {
    console.log(`\n[iteration ${iteration}]`);

    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 2048,
      system:
        'You are a customer support resolution agent. Always verify identity ' +
        'with get_customer before calling lookup_order or process_refund. ' +
        'Escalate policy exceptions rather than guessing.',
      tools: TOOLS,
      messages,
    });

    console.log(`stop_reason: ${response.stop_reason}`);

    // Append the FULL assistant turn — including tool_use blocks, not just
    // extracted text. Dropping tool_use blocks breaks tool_use_id pairing
    // on the next request.
    messages.push({ role: 'assistant', content: response.content });

    // --- PRIMARY termination signal --- branch on stop_reason only, never
    // on the presence/absence of particular words in the response text.
    if (response.stop_reason === 'end_turn') {
      const finalText = response.content.find((b) => b.type === 'text')?.text ?? '';
      console.log('-'.repeat(60));
      return finalText;
    }

    if (response.stop_reason === 'tool_use') {
      const toolUseBlocks = response.content.filter((b) => b.type === 'tool_use');
      const toolResults = [];

      for (const block of toolUseBlocks) {
        console.log(`  -> ${block.name}(${JSON.stringify(block.input)})`);
        const result = executeTool(block.name, block.input);
        console.log(`  <- ${JSON.stringify(result)}`);
        toolResults.push({
          type: 'tool_result',
          tool_use_id: block.id,
          content: JSON.stringify(result),
        });
      }

      // All tool_result blocks from this turn go back as ONE user message.
      messages.push({ role: 'user', content: toolResults });
      continue;
    }

    // Any other stop_reason is handled explicitly rather than silently looping.
    return `Stopped with unexpected stop_reason: ${response.stop_reason}`;
  }

  // Exhausted MAX_ITERATIONS without end_turn — an anomaly to investigate,
  // not a successful completion.
  return `[SAFETY NET TRIGGERED] Agent did not reach end_turn within ${MAX_ITERATIONS} iterations. Escalate for investigation.`;
}

const result = await runAgent(
  'Hi, this is jane@example.com. Can you check the status of order A1029 ' +
    'and refund me $42.50 since it never arrived?'
);
console.log(`\nFinal Answer:\n${result}`);
