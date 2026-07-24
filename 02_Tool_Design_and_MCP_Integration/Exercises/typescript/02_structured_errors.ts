/**
 * Exercise 2 -- Structured MCP-Style Error Responses
 * Domain 2, Task 2.2: Implement structured error responses for MCP tools.
 *
 * Demonstrates the MCP `isError` pattern with a typed discriminated union:
 * a tool result is EITHER a success payload OR structured error metadata
 * (errorCategory, isRetryable, message), never an undifferentiated string.
 *
 * Note: the Anthropic Messages API also has its own top-level `is_error`
 * boolean on a `tool_result` content block. That is a DIFFERENT, API-level
 * signal ("this tool call failed") from the `isError` field inside our own
 * JSON payload ("here is structured detail about why"). MCP tools
 * typically set both.
 */

import Anthropic from "@anthropic-ai/sdk";
import type { Tool, MessageParam } from "@anthropic-ai/sdk/resources/messages";

const client = new Anthropic();
const MODEL = "claude-sonnet-5";

type ErrorCategory = "transient" | "validation" | "business" | "permission";

interface ToolError {
  isError: true;
  errorCategory: ErrorCategory;
  isRetryable: boolean;
  message: string;
}

interface RefundSuccess {
  isError: false;
  orderId: string;
  refundedAmount: number;
  status: "completed";
}

type RefundResult = ToolError | RefundSuccess;

function processRefund(orderId: string, amount: number): RefundResult {
  // Validation error -- bad input; retrying with the same args never helps
  if (amount <= 0) {
    return {
      isError: true,
      errorCategory: "validation",
      isRetryable: false,
      message: `Refund amount must be positive; received ${amount}.`,
    };
  }

  // Business error -- policy violation, not a system fault, not retryable
  if (amount > 500) {
    return {
      isError: true,
      errorCategory: "business",
      isRetryable: false,
      message:
        "Refunds over $500 require manager approval and cannot be " +
        "processed automatically. Escalate to a human agent.",
    };
  }

  // Permission error -- the caller isn't authorized for this action
  if (orderId.startsWith("LOCKED-")) {
    return {
      isError: true,
      errorCategory: "permission",
      isRetryable: false,
      message: `Order ${orderId} is locked pending fraud review; refunds are disabled.`,
    };
  }

  // Transient error -- simulate a flaky downstream payment service
  if (Math.random() < 0.3) {
    return {
      isError: true,
      errorCategory: "transient",
      isRetryable: true,
      message: "Payment service timed out after 10s. Safe to retry.",
    };
  }

  // Success -- NOT an error. Distinguish this from a valid-but-empty
  // result: never mark "no matches" as isError.
  return { isError: false, orderId, refundedAmount: amount, status: "completed" };
}

type Decision =
  | { action: "retry" }
  | { action: "return_to_caller"; content: RefundResult }
  | { action: "escalate"; content: RefundResult };

function handleToolResult(result: RefundResult): Decision {
  if (!result.isError) return { action: "return_to_caller", content: result };

  switch (result.errorCategory) {
    case "transient":
      if (result.isRetryable) {
        console.log(`    [recovery] transient -- retrying locally: ${result.message}`);
        return { action: "retry" };
      }
      return { action: "return_to_caller", content: result };
    case "validation":
      console.log(`    [recovery] validation -- needs corrected input: ${result.message}`);
      return { action: "return_to_caller", content: result };
    case "business":
      console.log(`    [recovery] business rule violation -- surface as-is: ${result.message}`);
      return { action: "return_to_caller", content: result };
    case "permission":
      console.log(`    [recovery] permission denied -- escalate, do not retry: ${result.message}`);
      return { action: "escalate", content: result };
  }
}

function runRefundWithRecovery(
  orderId: string,
  amount: number,
  maxLocalRetries = 2
): { decision: Decision; attempts: number } {
  let attempts = 0;
  while (true) {
    attempts += 1;
    const result = processRefund(orderId, amount);
    const decision = handleToolResult(result);
    if (decision.action === "retry" && attempts <= maxLocalRetries) continue;
    return { decision, attempts };
  }
}

// ── Part 1: Pure client-side recovery logic (no API call needed) ──────
function part1LocalRecoveryDemo(): void {
  console.log("\n=== Part 1: Client-side recovery branching on errorCategory ===");
  const cases: Array<[string, number]> = [
    ["ORD-1001", 45.0],
    ["ORD-1002", -10.0],
    ["ORD-1003", 750.0],
    ["LOCKED-9001", 20.0],
  ];
  for (const [orderId, amount] of cases) {
    console.log(`\nRefund request: order=${orderId} amount=${amount}`);
    const { decision, attempts } = runRefundWithRecovery(orderId, amount);
    console.log(`  Final action: ${decision.action} (after ${attempts} attempt(s))`);
    if ("content" in decision) console.log(`  Payload: ${JSON.stringify(decision.content, null, 2)}`);
  }
}

// ── Part 2: Wiring the structured error into a real Claude conversation ──
const REFUND_TOOL: Tool[] = [
  {
    name: "process_refund",
    description:
      "Process a refund for a given order. Returns a structured error " +
      "(with errorCategory and isRetryable) if the refund cannot be " +
      "completed -- explain the reason to the user based on that " +
      "structured detail rather than a generic failure message.",
    input_schema: {
      type: "object",
      properties: { order_id: { type: "string" }, amount: { type: "number" } },
      required: ["order_id", "amount"],
    },
  },
];

async function part2ClaudeSeesStructuredError(): Promise<void> {
  console.log("\n=== Part 2: Structured error surfaced through a real tool_result ===");
  const messages: MessageParam[] = [
    { role: "user", content: "Please refund $750 on order ORD-2002." },
  ];

  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 400,
    tools: REFUND_TOOL,
    messages,
  });
  const toolBlock = response.content.find((b) => b.type === "tool_use");
  if (!toolBlock || toolBlock.type !== "tool_use") throw new Error("Expected a tool_use block");
  messages.push({ role: "assistant", content: response.content });

  const input = toolBlock.input as { order_id: string; amount: number };
  const result = processRefund(input.order_id, input.amount);

  messages.push({
    role: "user",
    content: [
      {
        type: "tool_result",
        tool_use_id: toolBlock.id,
        content: JSON.stringify(result),
        is_error: result.isError,
      },
    ],
  });

  const final = await client.messages.create({
    model: MODEL,
    max_tokens: 400,
    tools: REFUND_TOOL,
    messages,
  });
  for (const block of final.content) {
    if (block.type === "text") console.log(`  Claude's response to the user:\n  ${block.text}`);
  }
}

async function main(): Promise<void> {
  part1LocalRecoveryDemo();
  await part2ClaudeSeesStructuredError();
}

main();
