/**
 * Exercise 1 — Basic Messages API (TypeScript)
 * Topic: Claude Models & API
 *
 * Run: npx ts-node 01_basic_messages.ts
 */

import Anthropic from '@anthropic-ai/sdk';
import type { Message, MessageParam } from '@anthropic-ai/sdk/resources/messages';

const client = new Anthropic(); // reads ANTHROPIC_API_KEY from environment


// ─────────────────────────────────────────────
// Part 1: Typed Single-Turn Message
// ─────────────────────────────────────────────
async function part1TypedMessage(): Promise<void> {
  console.log('\n=== Part 1: Typed Single-Turn Message ===');

  const response: Message = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 256,
    messages: [
      { role: 'user', content: 'What is the speed of light in metres per second?' }
    ]
  });

  // TypeScript knows the shape of response — use .content[0]
  const firstBlock = response.content[0];
  if (firstBlock.type === 'text') {
    console.log(`Answer: ${firstBlock.text}`);
  }

  console.log(`Stop reason  : ${response.stop_reason}`);
  console.log(`Input tokens : ${response.usage.input_tokens}`);
  console.log(`Output tokens: ${response.usage.output_tokens}`);
}


// ─────────────────────────────────────────────
// Part 2: Typed Multi-Turn
// ─────────────────────────────────────────────
async function part2TypedMultiTurn(): Promise<void> {
  console.log('\n=== Part 2: Typed Multi-Turn ===');

  const messages: MessageParam[] = [];

  async function chat(userInput: string): Promise<string> {
    messages.push({ role: 'user', content: userInput });

    const response = await client.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 256,
      system: 'You are a concise science tutor. Keep answers to two sentences.',
      messages
    });

    const block = response.content[0];
    const reply = block.type === 'text' ? block.text : '';
    messages.push({ role: 'assistant', content: reply });
    return reply;
  }

  console.log('User: What is a photon?');
  console.log(`Claude: ${await chat('What is a photon?')}`);

  console.log('\nUser: Does it have mass?');
  console.log(`Claude: ${await chat('Does it have mass?')}`);
}


// ─────────────────────────────────────────────
// Part 3: Model Comparison with Typed Results
// ─────────────────────────────────────────────
interface ModelResult {
  model: string;
  text: string;
  totalTokens: number;
}

async function part3ModelComparison(): Promise<void> {
  console.log('\n=== Part 3: Model Comparison ===');

  const prompt = 'In one sentence, what is quantum computing?';
  const models = ['claude-haiku-4-5-20251001', 'claude-sonnet-4-6'] as const;

  const results: ModelResult[] = await Promise.all(
    models.map(async (model) => {
      const response = await client.messages.create({
        model,
        max_tokens: 128,
        messages: [{ role: 'user', content: prompt }]
      });
      const block = response.content[0];
      return {
        model,
        text: block.type === 'text' ? block.text : '',
        totalTokens: response.usage.input_tokens + response.usage.output_tokens
      };
    })
  );

  for (const result of results) {
    console.log(`\n${result.model} (${result.totalTokens} tokens)`);
    console.log(result.text);
  }
}


// ─────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────
await part1TypedMessage();
await part2TypedMultiTurn();
await part3ModelComparison();
