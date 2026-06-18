---
tags: [exercises, typescript, production, evaluation]
module: "06 - Production & Evaluation"
language: TypeScript
---

# TypeScript Exercises — Production & Evaluation

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/06_Production_and_Evaluation/Exercises/typescript)

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

> **Coming soon.** TypeScript exercises will add type safety to production patterns:

| Planned file | Topic |
|---|---|
| `01_prompt_caching.ts` | Typed `CacheControlEphemeral` block, usage stat comparison |
| `02_batching.ts` | Typed `MessageBatch` polling loop |
| `03_llm_judge.ts` | Generic `EvalResult<T>` interface for typed evaluation output |

In the meantime, see the [[../python/README|Python exercises]] for the full implementation.

## How to Run (once files exist)

```bash
npm install
npx ts-node --esm 01_prompt_caching.ts

# Or via script
./run.sh
.\run.ps1
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
