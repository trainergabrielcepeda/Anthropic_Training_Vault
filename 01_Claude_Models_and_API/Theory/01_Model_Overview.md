---
tags: [theory, models]
topic: "01 - Claude Models & API"
---

# Model Overview

## The Claude Model Family

Anthropic releases Claude in three capability tiers. Each tier is optimized for a different point on the cost-speed-intelligence tradeoff curve.

| Tier | Current Model ID | Strengths | Typical Use Cases |
| ---- | ---------------- | --------- | ----------------- |
| **Haiku** | `claude-haiku-4-5-20251001` | Fastest, cheapest | Classification, extraction, high-volume tasks, real-time chat |
| **Sonnet** | `claude-sonnet-4-6` | Balanced | Most production workloads, coding assistance, analysis |
| **Opus** | `claude-opus-4-8` | Most capable | Complex reasoning, research, nuanced generation |

> [!tip] Exam tip
> Expect questions that give you a scenario (e.g., "classify 10,000 support tickets per day") and ask which model tier is most appropriate. The answer almost always turns on cost and latency requirements, not raw capability.

---

## Model Selection Decision Tree

```
Is latency < 500ms required?
├── Yes → Haiku
└── No
    Does the task require deep reasoning or 200k+ context?
    ├── Yes → Opus
    └── No → Sonnet
```

---

## Context Windows

| Model | Input Context | Output Limit |
| ----- | ------------- | ------------ |
| Haiku 4.5 | 200,000 tokens | 8,192 tokens |
| Sonnet 4.6 | 200,000 tokens | 64,000 tokens |
| Opus 4.8 | 200,000 tokens | 32,000 tokens |

> [!note] Input vs output pricing
> Input and output tokens are priced differently. Output tokens are typically 3–5× more expensive than input tokens. Design prompts to produce concise, focused outputs.

---

## Multimodal Capabilities

All current Claude models support:
- **Images** — JPEG, PNG, GIF, WebP up to 5MB per image, up to 20 images per request
- **Documents** — PDF support (text and images within PDFs)
- **Plain text** — any UTF-8 text content

Vision is passed as a `content` block with `type: "image"` alongside a `source` specifying the media type and base64 data (or a URL).

---

## Model Versioning

Anthropic uses a `model-version-YYYYMMDD` naming pattern for dated snapshots. Using a dated snapshot ensures stability; using an undated alias (e.g., `claude-sonnet-4-6`) always points to the latest release of that tier.

> [!warning] Alias behavior in production
> For production deployments, pin to a dated snapshot to avoid unexpected behavior changes when Anthropic releases a new version of a tier.

---

## Related Notes

- [[02_API_Fundamentals|API Fundamentals]]
- [[03_Tokens_and_Context|Tokens & Context Windows]]
- [[../../00_Setup/Environment_Setup|Model IDs in your setup]]

---

[[../_Index|← Back to Claude Models & API Index]]
