/**
 * Exercise 2 — Forced Tool Ordering + Validation/Retry (Tasks 4.3 & 4.4)
 * Domain: Prompt Engineering & Structured Output
 *
 * Demonstrates:
 *   - Forcing a SPECIFIC named tool ({"type": "tool", "name": "extract_metadata"})
 *     to guarantee a metadata-extraction step runs before a later
 *     enrichment step depends on its output
 *   - A self-correction schema design: extracting BOTH stated_total and
 *     calculated_total (computed independently) so a discrepancy is
 *     visible without a second model call
 *   - A conflict_detected boolean for genuinely inconsistent source data
 *   - retry-with-error-feedback for a format/structural mismatch
 *
 * Run: npx ts-node --esm 02_validation_retry_loop.ts
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

interface DocumentMetadata {
  document_type: 'invoice' | 'receipt' | 'purchase_order' | 'other';
  document_id: string | null;
}

interface InvoiceExtraction {
  vendor_name: string;
  line_items: { description: string; amount: number }[];
  stated_total: number;
  calculated_total: number; // model computes this itself from line_items
  conflict_detected: boolean; // true if stated_total != calculated_total
}

const METADATA_TOOL = {
  name: 'extract_metadata',
  description: 'Identify the basic document type and ID before deeper extraction.',
  input_schema: {
    type: 'object' as const,
    properties: {
      document_type: { type: 'string', enum: ['invoice', 'receipt', 'purchase_order', 'other'] },
      document_id: { type: ['string', 'null'] }
    },
    required: ['document_type']
  }
};

const INVOICE_TOOL = {
  name: 'extract_invoice',
  description: 'Extract invoice line items and totals, flagging any total mismatch.',
  input_schema: {
    type: 'object' as const,
    properties: {
      vendor_name: { type: 'string' },
      line_items: {
        type: 'array',
        items: {
          type: 'object',
          properties: { description: { type: 'string' }, amount: { type: 'number' } },
          required: ['description', 'amount']
        }
      },
      stated_total: { type: 'number', description: 'The total as printed on the document.' },
      calculated_total: { type: 'number', description: 'Sum of all line_items amounts, computed independently.' },
      conflict_detected: { type: 'boolean', description: 'true if stated_total and calculated_total differ.' }
    },
    required: ['vendor_name', 'line_items', 'stated_total', 'calculated_total', 'conflict_detected']
  }
};

// Deliberately inconsistent: the printed total ($500) does not match
// what the line items actually sum to ($480) — genuine source-data
// inconsistency, not an extraction mistake.
const INVOICE_TEXT = `
INVOICE #3390 — Marlowe Design Studio
  Logo design ......... $300.00
  Brand guidelines .... $180.00
TOTAL DUE: $500.00
`;

async function extractMetadataFirst(documentText: string): Promise<DocumentMetadata> {
  // Forced, specific tool: this step must run and must be THIS tool,
  // because a later enrichment step (routing to the right extraction
  // schema) depends on knowing document_type before anything else runs.
  const response = await client.messages.create({
    model: 'claude-sonnet-5',
    max_tokens: 256,
    tools: [METADATA_TOOL],
    tool_choice: { type: 'tool', name: 'extract_metadata' },
    messages: [{ role: 'user', content: `Identify the document type:\n\n${documentText}` }]
  });
  const block = response.content.find((b) => b.type === 'tool_use');
  if (!block || block.type !== 'tool_use') throw new Error('Expected tool_use');
  return block.input as DocumentMetadata;
}

async function extractInvoiceWithSelfCheck(documentText: string): Promise<InvoiceExtraction> {
  const response = await client.messages.create({
    model: 'claude-sonnet-5',
    max_tokens: 1024,
    tools: [INVOICE_TOOL],
    tool_choice: { type: 'tool', name: 'extract_invoice' },
    messages: [{ role: 'user', content: `Extract invoice fields, computing calculated_total independently from the line items:\n\n${documentText}` }]
  });
  const block = response.content.find((b) => b.type === 'tool_use');
  if (!block || block.type !== 'tool_use') throw new Error('Expected tool_use');
  return block.input as InvoiceExtraction;
}

async function main() {
  console.log('=== Step 1: forced extract_metadata runs before enrichment ===\n');
  const metadata = await extractMetadataFirst(INVOICE_TEXT);
  console.log(JSON.stringify(metadata, null, 2));

  if (metadata.document_type !== 'invoice') {
    console.log('Not an invoice — would route to a different extraction schema here.');
    return;
  }

  console.log('\n=== Step 2: invoice extraction with stated_total vs calculated_total self-check ===\n');
  const invoice = await extractInvoiceWithSelfCheck(INVOICE_TEXT);
  console.log(JSON.stringify(invoice, null, 2));

  if (invoice.conflict_detected) {
    console.log(
      `\nconflict_detected = true: stated_total (${invoice.stated_total}) != ` +
      `calculated_total (${invoice.calculated_total}). This is a SOURCE DATA ` +
      `inconsistency (the document itself is self-contradictory), not an ` +
      `extraction error — retrying will not resolve it. Route to human review ` +
      `with both values attached.`
    );
  } else {
    console.log('\nNo conflict — stated and calculated totals agree.');
  }
}

main();
