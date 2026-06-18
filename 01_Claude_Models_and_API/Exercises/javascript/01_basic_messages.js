/**
 * Exercise 1 — Basic Messages API (JavaScript)
 * Topic: Claude Models & API
 *
 * Run: node 01_basic_messages.js
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic(); // reads ANTHROPIC_API_KEY from environment


// ─────────────────────────────────────────────
// Part 1: Single-Turn Message
// ─────────────────────────────────────────────
async function part1SingleTurn() {
  console.log('\n=== Part 1: Single-Turn Message ===');

  const response = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 256,
    messages: [
      { role: 'user', content: 'What is the speed of light in metres per second?' }
    ]
  });

  console.log(`Response ID  : ${response.id}`);
  console.log(`Model        : ${response.model}`);
  console.log(`Stop reason  : ${response.stop_reason}`);
  console.log(`Input tokens : ${response.usage.input_tokens}`);
  console.log(`Output tokens: ${response.usage.output_tokens}`);
  console.log(`\nContent:\n${response.content[0].text}`);
}


// ─────────────────────────────────────────────
// Part 2: Multi-Turn Conversation
// ─────────────────────────────────────────────
async function part2MultiTurn() {
  console.log('\n=== Part 2: Multi-Turn Conversation ===');

  const messages = [];

  async function chat(userInput) {
    messages.push({ role: 'user', content: userInput });
    const response = await client.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 256,
      system: 'You are a concise science tutor. Keep answers to two sentences.',
      messages
    });
    const reply = response.content[0].text;
    messages.push({ role: 'assistant', content: reply });
    return reply;
  }

  console.log('User: What is a black hole?');
  console.log(`Claude: ${await chat('What is a black hole?')}`);

  console.log('\nUser: How does Hawking radiation escape it?');
  console.log(`Claude: ${await chat('How does Hawking radiation escape it?')}`);

  console.log('\nUser: Who predicted it?');
  console.log(`Claude: ${await chat('Who predicted it?')}`);
}


// ─────────────────────────────────────────────
// Part 3: Streaming
// ─────────────────────────────────────────────
async function part3Streaming() {
  console.log('\n=== Part 3: Streaming ===');
  process.stdout.write('Response: ');

  const stream = client.messages.stream({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 256,
    messages: [{ role: 'user', content: 'Explain gravity in two sentences.' }]
  });

  for await (const event of stream) {
    if (
      event.type === 'content_block_delta' &&
      event.delta.type === 'text_delta'
    ) {
      process.stdout.write(event.delta.text);
    }
  }

  const finalMessage = await stream.finalMessage();
  console.log(`\n\nTotal tokens: ${finalMessage.usage.input_tokens + finalMessage.usage.output_tokens}`);
}


// ─────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────
await part1SingleTurn();
await part2MultiTurn();
await part3Streaming();
