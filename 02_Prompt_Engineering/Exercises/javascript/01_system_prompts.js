/**
 * Exercise 1 — System Prompts (JavaScript)
 * Topic: Prompt Engineering
 *
 * Run: node 01_system_prompts.js
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();
const QUESTION = 'Can you help me understand compound interest?';

// Part 1: Compare no system prompt vs with system prompt
async function compareSystems() {
  console.log('\n=== System Prompt Comparison ===\n');

  const withoutSystem = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 200,
    messages: [{ role: 'user', content: QUESTION }]
  });

  console.log('WITHOUT system prompt:');
  console.log(withoutSystem.content[0].text);

  const withSystem = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 200,
    system: 'You are a financial advisor speaking to a 10-year-old. Use simple words and a fun analogy. Answer in exactly 3 sentences.',
    messages: [{ role: 'user', content: QUESTION }]
  });

  console.log('\nWITH persona system prompt:');
  console.log(withSystem.content[0].text);
}

// Part 2: Format constraints
async function formatConstraints() {
  console.log('\n=== Format Constraints ===\n');

  const formats = {
    'Bullet list': 'Respond with a markdown bullet list only. No intro, no conclusion.',
    'One sentence': 'Respond in exactly one sentence.',
  };

  for (const [name, instruction] of Object.entries(formats)) {
    const r = await client.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 150,
      system: instruction,
      messages: [{ role: 'user', content: QUESTION }]
    });
    console.log(`[${name}]: ${r.content[0].text}\n`);
  }
}

// Part 3: Assistant prefilling
async function prefilling() {
  console.log('\n=== Assistant Prefilling ===\n');

  const r = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 256,
    messages: [
      { role: 'user', content: 'Explain compound interest.' },
      { role: 'assistant', content: '{' }  // prefill
    ]
  });

  console.log('Prefilled JSON:');
  console.log('{' + r.content[0].text);
}

await compareSystems();
await formatConstraints();
await prefilling();
