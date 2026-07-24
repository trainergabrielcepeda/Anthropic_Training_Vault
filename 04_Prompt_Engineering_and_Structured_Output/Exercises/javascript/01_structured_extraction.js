/**
 * Exercise 1 — Structured Extraction via tool_use (Task 4.3) + Validation Retry (Task 4.4)
 * Domain: Prompt Engineering & Structured Output
 *
 * Covers:
 *   - An extraction tool schema with required, nullable, and
 *     enum + "other"/detail fields
 *   - Forcing a specific tool via tool_choice so it's guaranteed to run
 *   - Reading the result directly from the tool_use response block
 *   - A semantic validation check (line items vs. stated total) that
 *     schema compliance alone does NOT catch, plus a retry-with-
 *     specific-error-feedback loop
 *
 * Run: node 01_structured_extraction.js
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const EXTRACT_INVOICE_TOOL = {
  name: 'extract_invoice',
  description: 'Record structured fields extracted from an invoice.',
  input_schema: {
    type: 'object',
    properties: {
      vendor_name: { type: 'string' },
      line_items: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            description: { type: 'string' },
            amount: { type: 'number' }
          },
          required: ['description', 'amount']
        }
      },
      stated_total: { type: 'number' },
      // Nullable: not every invoice carries a PO number. Required
      // would pressure the model to fabricate one when absent.
      purchase_order_number: {
        type: ['string', 'null'],
        description: 'PO number, or null if not present in the document.'
      },
      category: {
        type: 'string',
        enum: ['utilities', 'software', 'travel', 'office_supplies', 'other'],
        description: "Best-fit spend category. Use 'other' if none of the fixed values fit."
      },
      category_detail: {
        type: ['string', 'null'],
        description: "Required when category is 'other'; null otherwise."
      }
    },
    required: ['vendor_name', 'line_items', 'stated_total', 'category']
  }
};

// This invoice's line items deliberately don't sum to the stated
// total (960 != 940) — a semantic error tool_use cannot catch on its
// own, used to exercise the retry-with-feedback loop below.
const INVOICE_TEXT = `
INVOICE #7821 — Blue Harbor Consulting
  Strategy workshop (1 day) ......... $700.00
  Follow-up session .................. $260.00
TOTAL DUE: $940.00
`;

async function extractInvoice(messages) {
  const response = await client.messages.create({
    model: 'claude-sonnet-5',
    max_tokens: 1024,
    tools: [EXTRACT_INVOICE_TOOL],
    tool_choice: { type: 'tool', name: 'extract_invoice' },
    messages
  });
  const toolBlock = response.content.find((b) => b.type === 'tool_use');
  return { toolBlock, result: toolBlock.input };
}

function validateSemantics(extraction) {
  const computed = extraction.line_items.reduce((sum, item) => sum + item.amount, 0);
  const stated = extraction.stated_total;
  if (Math.abs(computed - stated) > 0.01) {
    return `Line items sum to ${computed.toFixed(2)}, but stated_total is ${stated.toFixed(2)}. ` +
      `Re-read the document for a line item you may have missed or misread.`;
  }
  return null;
}

async function extractWithRetry(documentText, maxRetries = 2) {
  let messages = [
    { role: 'user', content: `Extract the invoice fields from this document:\n\n${documentText}` }
  ];

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const { toolBlock, result } = await extractInvoice(messages);
    const error = validateSemantics(result);

    if (!error) {
      console.log(`  [attempt ${attempt + 1}] validation passed`);
      return result;
    }

    console.log(`  [attempt ${attempt + 1}] validation FAILED: ${error}`);
    if (attempt === maxRetries) {
      console.log('  [giving up] max retries exhausted');
      return result;
    }

    // Retry-with-error-feedback: echo the assistant's tool call, then
    // a tool_result carrying the SPECIFIC validation error so the
    // model can re-check the same source with a concrete target.
    messages = [
      ...messages,
      { role: 'assistant', content: [toolBlock] },
      {
        role: 'user',
        content: [
          {
            type: 'tool_result',
            tool_use_id: toolBlock.id,
            content: `Validation failed: ${error}`,
            is_error: true
          }
        ]
      }
    ];
  }
}

async function main() {
  console.log('=== Structured Extraction + Semantic Validation Retry ===\n');
  const result = await extractWithRetry(INVOICE_TEXT);
  console.log('\nFinal extraction:');
  console.log(JSON.stringify(result, null, 2));

  console.log('\n--- What to notice ---');
  console.log(`purchase_order_number: ${JSON.stringify(result.purchase_order_number)} (nullable — no fabrication)`);
  console.log(`category: ${result.category}${result.category === 'other' ? ` (detail: ${result.category_detail})` : ''}`);
}

main();
