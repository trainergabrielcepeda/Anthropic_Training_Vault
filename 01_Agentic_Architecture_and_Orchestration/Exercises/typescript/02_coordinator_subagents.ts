/**
 * Exercise 2 — Coordinator Dispatching to Parallel Subagents
 * Domain: Agentic Architecture & Orchestration (Tasks 1.2, 1.3)
 *
 * Covers:
 *   - Hub-and-spoke: a coordinator dispatches to 2+ subagents and is the
 *     only thing that talks to each of them (they never talk to each other)
 *   - Explicit context passing — each subagent gets a fully self-contained
 *     prompt. There is NO shared conversation history and NO shared memory
 *     between the separate messages.create() calls below.
 *   - Parallel dispatch of independent subagent work via Promise.all,
 *     standing in for the harness executing multiple tool_use blocks at once
 *   - Coordinator synthesis + a gap-check / re-delegation pass
 *
 * IMPORTANT — how this maps to the Claude Agent SDK in production:
 *   This file uses plain, separate `client.messages.create()` calls with
 *   distinct system prompts and distinct (scoped) tool sets to SIMULATE
 *   subagents, because these exercises target the raw Anthropic SDK. In a
 *   real Claude Agent SDK deployment, this exact pattern is implemented
 *   with the built-in `Task` tool: the coordinator's `allowedTools` must
 *   include `"Task"`, and each subagent "role" below (web-search,
 *   doc-analysis) would instead be a typed `AgentDefinition` (description +
 *   system prompt + scoped tools) registered on the coordinator's `agents`
 *   config. Spawning them in parallel means emitting multiple `Task`
 *   tool_use blocks in a SINGLE coordinator turn — the concurrent dispatch
 *   below (Promise.all) is the same idea, implemented at the raw-API level.
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();
const COORDINATOR_MODEL = 'claude-opus-4-8'; // coordinator/orchestrator role
const SUBAGENT_MODEL = 'claude-haiku-4-5-20251001'; // fast, scoped, low-cost subagent work

interface SubagentJob {
  role: string;
  systemPrompt: string;
  userPrompt: string;
}

interface SubagentResult {
  role: string;
  output: string;
}

/**
 * A "subagent" is just a separate, isolated messages.create() call.
 * Nothing here is shared with the coordinator's own conversation history
 * or with any other subagent call — that isolation is deliberate (Task
 * 1.3: "no automatic inheritance, no shared memory between invocations").
 * Every fact the subagent needs must be in userPrompt.
 */
async function callSubagent(role: string, systemPrompt: string, userPrompt: string): Promise<SubagentResult> {
  const response = await client.messages.create({
    model: SUBAGENT_MODEL,
    max_tokens: 1024,
    system: systemPrompt,
    messages: [{ role: 'user', content: userPrompt }],
  });
  const textBlock = response.content.find((b) => b.type === 'text');
  const output = textBlock && textBlock.type === 'text' ? textBlock.text : '';
  return { role, output };
}

/** Runs all jobs concurrently — models "multiple Task calls in one
 * coordinator response" so independent subtasks run at the same time. */
async function dispatchSubagentsInParallel(jobs: SubagentJob[]): Promise<SubagentResult[]> {
  return Promise.all(jobs.map((j) => callSubagent(j.role, j.systemPrompt, j.userPrompt)));
}

function coordinatorDecompose(goal: string): SubagentJob[] {
  return [
    {
      role: 'web-researcher',
      systemPrompt:
        'You are a focused web research subagent. Given a topic, produce ' +
        '2-3 concrete, plausible findings a web search would surface, each ' +
        'tagged with a made-up but realistic source URL. This is a training ' +
        'exercise — invent plausible findings, do not claim to have ' +
        'actually searched the web.',
      userPrompt:
        `Research goal (from the coordinator): ${goal}\n\n` +
        'Focus specifically on recent (last 12 months) developments. ' +
        'Report findings as a bulleted list with a source URL per bullet.',
    },
    {
      role: 'doc-analyzer',
      systemPrompt:
        'You are a document analysis subagent. Given a topic, summarize ' +
        'what a set of internal knowledge-base documents would likely say ' +
        'about it, citing a made-up but realistic document name and page ' +
        'number per claim. This is a training exercise — invent plausible citations.',
      userPrompt:
        `Research goal (from the coordinator): ${goal}\n\n` +
        'Focus specifically on historical context and prior internal ' +
        'analysis. Report findings as a bulleted list with [doc_name.pdf, p.N] citations.',
    },
  ];
}

/** The coordinator is the only thing that sees every subagent's output and
 * produces the final synthesis — subagents never see each other's work. */
async function coordinatorSynthesize(goal: string, subagentResults: SubagentResult[]): Promise<string> {
  const findingsBlock = subagentResults.map((r) => `### ${r.role} findings\n${r.output}`).join('\n\n');

  const response = await client.messages.create({
    model: COORDINATOR_MODEL,
    max_tokens: 1024,
    system:
      'You are a research coordinator. Synthesize the subagent findings ' +
      'below into one coherent, cited answer to the original goal. ' +
      "Preserve each claim's source attribution.",
    messages: [{ role: 'user', content: `Original goal: ${goal}\n\n${findingsBlock}` }],
  });
  const textBlock = response.content.find((b) => b.type === 'text');
  return textBlock && textBlock.type === 'text' ? textBlock.text : '';
}

/** Models "coordinator evaluates synthesis output for gaps and re-delegates
 * with a targeted query" — guarding against decomposition that was too
 * narrow (Task 1.2). Returns null when coverage looks adequate. */
async function coordinatorCheckCoverageGaps(goal: string, synthesis: string): Promise<string | null> {
  const response = await client.messages.create({
    model: COORDINATOR_MODEL,
    max_tokens: 256,
    system:
      'You audit research syntheses for coverage gaps relative to the ' +
      'stated goal. Reply with a single short follow-up research query for ' +
      'the most significant gap, or the single word NONE if coverage looks adequate.',
    messages: [{ role: 'user', content: `Goal: ${goal}\n\nSynthesis:\n${synthesis}` }],
  });
  const textBlock = response.content.find((b) => b.type === 'text');
  const text = (textBlock && textBlock.type === 'text' ? textBlock.text : 'NONE').trim();
  return text.toUpperCase().startsWith('NONE') ? null : text;
}

async function runCoordinator(goal: string): Promise<string> {
  console.log(`Goal: ${goal}\n${'-'.repeat(60)}`);

  const jobs = coordinatorDecompose(goal);
  console.log(`Dispatching ${jobs.length} subagents in parallel: ${jobs.map((j) => j.role)}`);
  const results = await dispatchSubagentsInParallel(jobs);
  for (const r of results) {
    console.log(`\n--- ${r.role} output ---\n${r.output}`);
  }

  let synthesis = await coordinatorSynthesize(goal, results);
  console.log(`\n--- Initial synthesis ---\n${synthesis}`);

  const gapQuery = await coordinatorCheckCoverageGaps(goal, synthesis);
  if (gapQuery) {
    console.log(`\nCoverage gap detected — re-delegating: ${gapQuery}`);
    const followUp = await callSubagent(
      'web-researcher-followup',
      jobs[0].systemPrompt,
      `Follow-up research goal (from the coordinator): ${gapQuery}`
    );
    synthesis = await coordinatorSynthesize(goal, [...results, followUp]);
    console.log(`\n--- Revised synthesis ---\n${synthesis}`);
  } else {
    console.log('\nNo coverage gaps detected.');
  }

  return synthesis;
}

const final = await runCoordinator('What is the current state of on-device (edge) LLM inference?');
console.log(`\n${'='.repeat(60)}\nFinal synthesized answer:\n${final}`);
