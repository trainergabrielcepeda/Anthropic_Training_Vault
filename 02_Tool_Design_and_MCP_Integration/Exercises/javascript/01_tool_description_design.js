/**
 * Exercise 1 -- Tool Description Quality & Selection Reliability
 * Domain 2, Task 2.1: Design effective tool interfaces with clear
 * descriptions and boundaries.
 *
 * Part A: Two tools with vague, overlapping descriptions give Claude
 *         nothing to disambiguate between them -- routing is unreliable.
 * Part B: The same capability split into three purpose-specific tools with
 *         differentiated names/descriptions -- routes consistently.
 */

import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const MODEL = "claude-sonnet-5";

const SAMPLE_DOC =
  "Q3 2026 Financial Summary. Revenue grew 12% quarter over quarter to " +
  "$4.2M. The board concluded that international expansion drove the " +
  "majority of new growth, though the underlying regional breakdown shows " +
  "growth was concentrated almost entirely in the APAC region.";

// ── Part A: Ambiguous, overlapping tools ──────────────────────────────
const AMBIGUOUS_TOOLS = [
  {
    name: "analyze_content",
    description: "Analyzes content and provides insights.",
    input_schema: {
      type: "object",
      properties: { text: { type: "string" } },
      required: ["text"],
    },
  },
  {
    name: "analyze_document",
    description: "Analyzes a document and returns information.",
    input_schema: {
      type: "object",
      properties: { text: { type: "string" } },
      required: ["text"],
    },
  },
];

// ── Part B: Purpose-specific tools with differentiated descriptions ───
const DIFFERENTIATED_TOOLS = [
  {
    name: "summarize_content",
    description:
      "Condense a long text into a short summary of its main points. Use " +
      "when the user asks to summarize, give an overview of, or list key " +
      "takeaways from a document. Input: raw text. Output: a 3-5 bullet " +
      "summary. Do NOT use this to pull out a single specific figure (use " +
      "extract_data_points) or to check whether a claim is supported by " +
      "the text (use verify_claim_against_source).",
    input_schema: {
      type: "object",
      properties: {
        text: { type: "string", description: "The full document text to summarize." },
      },
      required: ["text"],
    },
  },
  {
    name: "extract_data_points",
    description:
      "Pull one or more specific, named data points (numbers, dates, " +
      "names, figures) out of a document. Use when the user asks for a " +
      "precise value such as 'total revenue', 'filing date', or 'CEO " +
      "name'. Input: raw text plus the field to extract, e.g. field='total " +
      "revenue'. Output: the exact value found, or null if not present. " +
      "Do NOT use this for open-ended summarization or claim verification.",
    input_schema: {
      type: "object",
      properties: {
        text: { type: "string", description: "The full document text to search." },
        field: { type: "string", description: "The specific data point to extract, e.g. 'total revenue'." },
      },
      required: ["text", "field"],
    },
  },
  {
    name: "verify_claim_against_source",
    description:
      "Check whether a specific claim or conclusion is actually supported " +
      "by the evidence in a document. Use when the user asks 'does X " +
      "follow from this', 'is this claim accurate', or 'fact-check this " +
      "against the source'. Input: raw text plus the claim to check. " +
      "Output: supported / contradicted / not addressed, with the " +
      "supporting excerpt. Do NOT use this for general summarization or " +
      "simple data extraction.",
    input_schema: {
      type: "object",
      properties: {
        text: { type: "string", description: "The full document text to check against." },
        claim: { type: "string", description: "The specific claim or conclusion to verify." },
      },
      required: ["text", "claim"],
    },
  },
];

const TEST_QUERIES = [
  "Summarize the three main points of this quarterly report.",
  "Pull out the exact total revenue figure stated in this report.",
  "Does the conclusion about international expansion actually follow from the regional breakdown described?",
];

async function showRouting(tools, label) {
  console.log(`\n=== ${label} ===`);
  for (const query of TEST_QUERIES) {
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 300,
      tools,
      tool_choice: { type: "any" }, // force a tool call so routing is always visible
      messages: [{ role: "user", content: `${query}\n\nDocument:\n${SAMPLE_DOC}` }],
    });
    const toolUse = response.content.find((b) => b.type === "tool_use");
    console.log(`  Query: ${query}`);
    console.log(`    -> routed to: ${toolUse ? toolUse.name : "NONE"}`);
  }
}

async function main() {
  await showRouting(AMBIGUOUS_TOOLS, "Part A: Ambiguous tools (analyze_content vs analyze_document)");
  await showRouting(DIFFERENTIATED_TOOLS, "Part B: Differentiated, purpose-specific tools");
  console.log(
    "\nNote: Part A's routing may be inconsistent or arbitrary from run to " +
      "run -- that unpredictability IS the bug the description rewrite in " +
      "Part B is meant to fix."
  );
}

main();
