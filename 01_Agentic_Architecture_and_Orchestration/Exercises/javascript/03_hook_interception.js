/**
 * Exercise 3 — Hook-Style Tool Call Interception & Result Normalization
 * Domain: Agentic Architecture & Orchestration (Task 1.5, plus the
 * enforcement half of Task 1.4)
 *
 * Covers:
 *   - A PreToolUse-style hook: inspects an outgoing tool call BEFORE it
 *     executes and can block it — used here to enforce "refunds over $500
 *     require human approval" as a deterministic guarantee, not a prompt
 *     suggestion the model might skip.
 *   - A PostToolUse-style hook: inspects a tool's RESULT after execution
 *     but before it re-enters the model's context — used here to
 *     normalize heterogeneous formats (a Unix timestamp and a numeric
 *     HTTP-style status code) into one consistent shape.
 *
 * IMPORTANT — how this maps to the Claude Agent SDK in production:
 *   This file implements both hooks as plain functions called from a
 *   manual agentic loop, because these exercises target the raw Anthropic
 *   SDK. In the Claude Agent SDK, this exact pattern is a first-class
 *   feature: a `PreToolUse` hook can return a "deny" decision to block a
 *   tool call before it runs, and a `PostToolUse` hook can rewrite the
 *   tool result before Claude ever sees it. Reach for hooks (here or in
 *   the SDK) instead of a system-prompt instruction whenever the rule
 *   must hold deterministically — a prompt instruction is probabilistic
 *   and has a non-zero chance of being skipped.
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();
const MODEL = 'claude-sonnet-5';
const REFUND_APPROVAL_THRESHOLD = 500;

const TOOLS = [
  {
    name: 'process_refund',
    description: 'Issue a refund for an order.',
    input_schema: {
      type: 'object',
      properties: { order_id: { type: 'string' }, amount: { type: 'number' } },
      required: ['order_id', 'amount'],
    },
  },
  {
    name: 'escalate_to_human',
    description: 'Hand off to a human agent for cases exceeding autonomous authority.',
    input_schema: {
      type: 'object',
      properties: { summary: { type: 'string' } },
      required: ['summary'],
    },
  },
  {
    name: 'lookup_order',
    description: 'Retrieve order details, including status and last-update time.',
    input_schema: {
      type: 'object',
      properties: { order_id: { type: 'string' } },
      required: ['order_id'],
    },
  },
];

// --- Mock backend: deliberately returns heterogeneous formats, as if it
// were fronting two different legacy systems behind one MCP tool. ---------

function mockLookupOrder(orderId) {
  if (orderId === 'A1029') {
    return { order_id: 'A1029', status_code: 200, last_updated: 1732492800 }; // Unix ts, numeric status
  }
  return { order_id: orderId, status_code: 404, last_updated: null };
}

function mockProcessRefund(orderId, amount) {
  return { refund_id: 'rfd_9001', order_id: orderId, amount, status_code: 200 };
}

// --- Hook 1 (PreToolUse-style): outgoing tool call interception ---------

/**
 * Runs BEFORE a tool executes. Returning an object means "blocked" — the
 * tool is never called, and the returned object becomes the tool_result
 * instead, redirecting the model toward an allowed alternative.
 */
function preToolUseHook(toolName, toolInput) {
  if (toolName === 'process_refund' && (toolInput.amount ?? 0) > REFUND_APPROVAL_THRESHOLD) {
    return {
      is_error: true,
      // "message" here is the blocked-tool payload; it is separate from the
      // tool_result wrapper's own "content" field set in runAgent().
      message:
        `BLOCKED by policy hook: refunds over $${REFUND_APPROVAL_THRESHOLD} require ` +
        'human approval. Call escalate_to_human with a structured summary ' +
        '(customer, order, amount, reason) instead.',
    };
  }
  return null; // not blocked
}

// --- Hook 2 (PostToolUse-style): result normalization --------------------

/**
 * Runs AFTER a tool executes, BEFORE the result is appended to the
 * conversation. Normalizes heterogeneous formats from the (mock) backend
 * so the model always reasons over one consistent shape.
 */
function postToolUseHook(_toolName, rawResult) {
  const result = { ...rawResult };

  const statusMap = { 200: 'success', 404: 'not_found', 409: 'conflict', 500: 'error' };
  if (typeof result.status_code === 'number') {
    result.status = statusMap[result.status_code] ?? 'unknown';
    delete result.status_code;
  }

  if (typeof result.last_updated === 'number') {
    result.last_updated = new Date(result.last_updated * 1000).toISOString();
  }

  return result;
}

function executeToolWithHooks(name, toolInput) {
  const blocked = preToolUseHook(name, toolInput);
  if (blocked !== null) {
    console.log(`  [PreToolUse hook] blocked ${name}(${JSON.stringify(toolInput)})`);
    return blocked;
  }

  let raw;
  if (name === 'process_refund') {
    raw = mockProcessRefund(toolInput.order_id, toolInput.amount);
  } else if (name === 'lookup_order') {
    raw = mockLookupOrder(toolInput.order_id);
  } else if (name === 'escalate_to_human') {
    raw = { escalation_id: 'esc_2210', status_code: 200 };
  } else {
    raw = { error: `Unknown tool: ${name}` };
  }

  const normalized = postToolUseHook(name, raw);
  console.log(`  [PostToolUse hook] ${name} raw=${JSON.stringify(raw)} -> normalized=${JSON.stringify(normalized)}`);
  return normalized;
}

async function runAgent(task) {
  const messages = [{ role: 'user', content: task }];
  console.log(`Task: ${task}\n${'-'.repeat(60)}`);

  for (let i = 0; i < 6; i++) {
    // safety-net cap; primary stop is still stop_reason
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 1024,
      system:
        'You are a support agent. Look up orders before acting on them. ' +
        'If a refund is blocked by policy, escalate to a human with a ' +
        'structured summary instead of retrying.',
      tools: TOOLS,
      messages,
    });
    messages.push({ role: 'assistant', content: response.content });

    if (response.stop_reason === 'end_turn') {
      return response.content.find((b) => b.type === 'text')?.text ?? '';
    }

    if (response.stop_reason === 'tool_use') {
      const toolResults = [];
      for (const block of response.content) {
        if (block.type === 'tool_use') {
          console.log(`\n-> ${block.name}(${JSON.stringify(block.input)})`);
          const result = executeToolWithHooks(block.name, block.input);
          toolResults.push({
            type: 'tool_result',
            tool_use_id: block.id,
            content: JSON.stringify(result),
            is_error: Boolean(result.is_error),
          });
        }
      }
      messages.push({ role: 'user', content: toolResults });
      continue;
    }

    return `Unexpected stop_reason: ${response.stop_reason}`;
  }

  return '[SAFETY NET TRIGGERED] exceeded max turns';
}

console.log('=== Case 1: refund within policy ===');
console.log(await runAgent('Look up order A1029 and refund $50 for a late delivery.'));

console.log('\n\n=== Case 2: refund blocked by policy hook ===');
console.log(await runAgent('Look up order A1029 and refund $750 — customer wants a full refund.'));
