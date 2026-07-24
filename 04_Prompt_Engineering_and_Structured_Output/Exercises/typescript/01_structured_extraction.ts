/**
 * Exercise 1 — Structured Extraction via tool_use (Task 4.3)
 * Domain: Prompt Engineering & Structured Output
 *
 * Demonstrates:
 *   - A JSON schema with required, optional/nullable, and
 *     enum + "other"/detail fields, mapped to a TypeScript interface
 *   - tool_choice: "any" — used here because we expose TWO different
 *     extraction schemas and don't know in advance which document
 *     type we're looking at; "any" guarantees a tool call without
 *     forcing a specific (possibly wrong) schema
 *   - Reading the extraction straight from the tool_use response block
 *
 * Run: npx ts-node --esm 01_structured_extraction.ts
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

// Nullable due_date and an enum+detail category — mirrors the schema
// shape recommended in Theory/02_Structured_Output_and_Validation.md.
interface ReceiptExtraction {
  vendor_name: string;
  purchase_date: string;
  line_items: { description: string; amount: number }[];
  stated_total: number;
  due_date: string | null;
  category: 'utilities' | 'software' | 'travel' | 'office_supplies' | 'other';
  category_detail: string | null;
}

interface ContractExtraction {
  party_a: string;
  party_b: string;
  effective_date: string;
  term_months: number | null; // nullable — some contracts are indefinite
  renewal_type: 'automatic' | 'manual' | 'none' | 'unclear';
}

const RECEIPT_TOOL = {
  name: 'extract_receipt',
  description: 'Record structured fields extracted from a purchase receipt.',
  input_schema: {
    type: 'object' as const,
    properties: {
      vendor_name: { type: 'string' },
      purchase_date: { type: 'string', description: 'ISO 8601 date (YYYY-MM-DD).' },
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
      due_date: {
        type: ['string', 'null'],
        description: 'ISO 8601 date, or null if the receipt has no due date.'
      },
      category: {
        type: 'string',
        enum: ['utilities', 'software', 'travel', 'office_supplies', 'other']
      },
      category_detail: { type: ['string', 'null'] }
    },
    required: ['vendor_name', 'purchase_date', 'line_items', 'stated_total', 'category']
  }
};

const CONTRACT_TOOL = {
  name: 'extract_contract',
  description: 'Record structured fields extracted from a services contract.',
  input_schema: {
    type: 'object' as const,
    properties: {
      party_a: { type: 'string' },
      party_b: { type: 'string' },
      effective_date: { type: 'string' },
      // nullable: some contracts run indefinitely with no fixed term
      term_months: { type: ['number', 'null'] },
      renewal_type: {
        type: 'string',
        // "unclear" as an explicit enum value rather than a forced guess
        enum: ['automatic', 'manual', 'none', 'unclear']
      }
    },
    required: ['party_a', 'party_b', 'effective_date', 'renewal_type']
  }
};

const UNKNOWN_DOCUMENT = `
RECEIPT — Northwind Cloud Hosting
Date: 2026-05-14
Items:
  - Monthly hosting plan .......... $49.00
  - Extra storage add-on .......... $12.00
Total: $61.00
Payment due within 15 days.
`;

async function extractUnknownDocument(documentText: string): Promise<ReceiptExtraction | ContractExtraction> {
  const response = await client.messages.create({
    model: 'claude-sonnet-5',
    max_tokens: 1024,
    tools: [RECEIPT_TOOL, CONTRACT_TOOL],
    // We don't know ahead of time whether this is a receipt or a
    // contract, so we can't force a specific tool name. "any" still
    // guarantees SOME tool call — i.e. guaranteed structured output —
    // while letting the model pick the schema that actually fits.
    tool_choice: { type: 'any' },
    messages: [{ role: 'user', content: `Extract structured data from this document:\n\n${documentText}` }]
  });

  const toolBlock = response.content.find((b) => b.type === 'tool_use');
  if (!toolBlock || toolBlock.type !== 'tool_use') throw new Error('Expected a tool_use block');

  console.log(`Model selected tool: ${toolBlock.name}`);
  return toolBlock.input as ReceiptExtraction | ContractExtraction;
}

async function main() {
  console.log('=== tool_choice: "any" — schema unknown in advance ===\n');
  const result = await extractUnknownDocument(UNKNOWN_DOCUMENT);
  console.log(JSON.stringify(result, null, 2));
}

main();
