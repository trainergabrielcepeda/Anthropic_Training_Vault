/**
 * Exercise 3 -- tool_choice Modes & Tool Distribution
 * Domain 2, Task 2.3: Distribute tools appropriately across agents and
 * configure tool choice.
 *
 * Demonstrates the three tool_choice modes:
 *   { type: "auto" }                       -- Claude decides whether/which tool to call (default)
 *   { type: "any" }                        -- Claude must call SOME tool, but picks which one
 *   { type: "tool", name: "..." }          -- Claude must call this EXACT tool
 *
 * Scenario: a small, SCOPED document-processing pipeline (3 tools, not 18 --
 * see Theory/02_Error_Handling_and_Tool_Distribution.md). extract_metadata
 * must always run first (forced), the next step is chosen freely in a
 * follow-up turn ("auto"), and a final classification step must produce a
 * tool call rather than prose ("any").
 */

import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const MODEL = "claude-sonnet-5";

const TOOLS = [
  {
    name: "extract_metadata",
    description:
      "Extract title, author, and date from a raw document. Always run " +
      "this first on any new document, before translation or classification.",
    input_schema: {
      type: "object",
      properties: { text: { type: "string" } },
      required: ["text"],
    },
  },
  {
    name: "translate_text",
    description: "Translate document text into another language. Use only after metadata has already been extracted.",
    input_schema: {
      type: "object",
      properties: { text: { type: "string" }, target_language: { type: "string" } },
      required: ["text", "target_language"],
    },
  },
  {
    name: "classify_topic",
    description: "Classify a document's primary topic into one of a fixed set of categories.",
    input_schema: {
      type: "object",
      properties: {
        text: { type: "string" },
        category: { type: "string", enum: ["finance", "legal", "engineering", "marketing", "other"] },
      },
      required: ["text", "category"],
    },
  },
];

const DOCUMENT =
  "Q3 2026 Financial Summary\nBy J. Alvarez, Finance Dept, 2026-10-01\n\n" +
  "Revenue grew 12% quarter over quarter to $4.2M, driven primarily by " +
  "international expansion in the APAC region.";

function mockExecute(name, toolInput) {
  return JSON.stringify({ tool: name, received: toolInput });
}

async function step1ForcedToolChoice() {
  console.log("\n=== Step 1: forced tool_choice ({ type: 'tool', name: 'extract_metadata' }) ===");
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 300,
    tools: TOOLS,
    tool_choice: { type: "tool", name: "extract_metadata" },
    messages: [{ role: "user", content: DOCUMENT }],
  });
  const block = response.content.find((b) => b.type === "tool_use");
  console.log(`  Forced call: ${block.name}(${JSON.stringify(block.input)})`);
  return { response, block };
}

async function step2AutoFollowup(firstResponse, metadataBlock) {
  console.log("\n=== Step 2: tool_choice 'auto' for the follow-up turn ===");
  const messages = [
    { role: "user", content: DOCUMENT },
    { role: "assistant", content: firstResponse.content },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: metadataBlock.id,
          content: mockExecute(metadataBlock.name, metadataBlock.input),
        },
      ],
    },
  ];
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 300,
    tools: TOOLS,
    tool_choice: { type: "auto" },
    messages,
  });
  console.log(`  stop_reason: ${response.stop_reason}`);
  for (const b of response.content) {
    if (b.type === "tool_use") console.log(`  Claude chose: ${b.name}(${JSON.stringify(b.input)})`);
    else if (b.type === "text") console.log(`  Claude said: ${b.text.slice(0, 150)}`);
  }
}

async function step3AnyGuaranteesToolCall() {
  console.log("\n=== Step 3: tool_choice 'any' ===");
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 300,
    tools: TOOLS,
    tool_choice: { type: "any" },
    messages: [
      { role: "user", content: `This document is clearly about finance. Classify it.\n\n${DOCUMENT}` },
    ],
  });
  const block = response.content.find((b) => b.type === "tool_use");
  if (block) console.log(`  Guaranteed tool call: ${block.name}(${JSON.stringify(block.input)})`);
  else console.log("  Unexpected: no tool_use block returned despite tool_choice='any'");
}

async function main() {
  const { response, block } = await step1ForcedToolChoice();
  await step2AutoFollowup(response, block);
  await step3AnyGuaranteesToolCall();
}

main();
