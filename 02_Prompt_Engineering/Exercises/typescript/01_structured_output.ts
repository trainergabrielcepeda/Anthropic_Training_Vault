/**
 * Exercise 1 — Structured Output (TypeScript)
 * Topic: Prompt Engineering
 *
 * Demonstrates forcing JSON output via prefilling and via tool use.
 * Run: npx ts-node 01_structured_output.ts
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

interface ArticleSummary {
  title: string;
  main_topic: string;
  key_points: string[];
  sentiment: 'positive' | 'neutral' | 'negative';
  word_count_estimate: number;
}

const ARTICLE = `
Scientists announced yesterday that a new species of deep-sea fish has been discovered
in the Pacific Ocean at depths below 3,000 meters. The creature, which is bioluminescent,
uses light patterns to communicate with others of its kind. Researchers from the Woods Hole
Oceanographic Institution spent three years studying the fish using remote-controlled submarines.
The discovery is considered a significant breakthrough in marine biology and could help
scientists better understand how life adapts to extreme environments.
`;

// ─────────────────────────────────────────────
// Method 1: JSON via assistant prefilling
// ─────────────────────────────────────────────
async function extractViaPrefilling(): Promise<ArticleSummary> {
  const response = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 512,
    system: 'Extract structured data from articles. Return a valid JSON object only.',
    messages: [
      {
        role: 'user',
        content: `Article: ${ARTICLE}\n\nExtract: title, main_topic, key_points (array), sentiment, word_count_estimate`
      },
      { role: 'assistant', content: '{' }  // prefill forces JSON
    ]
  });

  const block = response.content[0];
  const json = block.type === 'text' ? '{' + block.text : '{}';
  return JSON.parse(json) as ArticleSummary;
}

// ─────────────────────────────────────────────
// Method 2: JSON via forced tool use (preferred)
// ─────────────────────────────────────────────
async function extractViaTool(): Promise<ArticleSummary> {
  const response = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 512,
    tools: [{
      name: 'record_summary',
      description: 'Record the extracted article summary.',
      input_schema: {
        type: 'object' as const,
        properties: {
          title:               { type: 'string' },
          main_topic:          { type: 'string' },
          key_points:          { type: 'array', items: { type: 'string' } },
          sentiment:           { type: 'string', enum: ['positive', 'neutral', 'negative'] },
          word_count_estimate: { type: 'number' }
        },
        required: ['title', 'main_topic', 'key_points', 'sentiment', 'word_count_estimate']
      }
    }],
    tool_choice: { type: 'tool', name: 'record_summary' },
    messages: [{ role: 'user', content: `Extract data from: ${ARTICLE}` }]
  });

  const toolBlock = response.content[0];
  if (toolBlock.type !== 'tool_use') throw new Error('Expected tool_use block');
  return toolBlock.input as ArticleSummary;
}

// ─────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────
console.log('=== Method 1: Prefilling ===');
const result1 = await extractViaPrefilling();
console.log(JSON.stringify(result1, null, 2));

console.log('\n=== Method 2: Forced Tool Use ===');
const result2 = await extractViaTool();
console.log(JSON.stringify(result2, null, 2));

console.log('\nBoth methods produce typed ArticleSummary objects.');
