---
tags: [theory, production, cost]
topic: "06 - Production & Evaluation"
---

# Cost Optimization

## Cost Components

```
total_cost = input_tokens × input_price_per_MTok
           + output_tokens × output_price_per_MTok
           + cache_write_tokens × cache_write_price
           + cache_read_tokens × cache_read_price
```

Output tokens are typically 3–5× more expensive than input tokens. Cache reads are typically 90% cheaper than standard input.

---

## Model Routing

Not every request needs Opus. Route tasks to the cheapest model that meets quality requirements.

```python
def route_model(task_type: str) -> str:
    routing_table = {
        "classification":   "claude-haiku-4-5-20251001",
        "extraction":       "claude-haiku-4-5-20251001",
        "summarization":    "claude-haiku-4-5-20251001",
        "code_generation":  "claude-sonnet-4-6",
        "complex_analysis": "claude-sonnet-4-6",
        "deep_reasoning":   "claude-opus-4-8",
    }
    return routing_table.get(task_type, "claude-sonnet-4-6")
```

> [!tip] Measure before routing
> Run a sample of your workload through both Haiku and Sonnet. If quality is equivalent, use Haiku. For most classification and extraction tasks, Haiku matches Sonnet quality at a fraction of the cost.

---

## Input Token Reduction

### Trim System Prompts

Every token in every request is billed. Audit your system prompts:
- Remove filler phrases ("As an AI assistant, I will…")
- Remove redundant instructions Claude already follows by default
- Use bullet points instead of paragraphs

### Compress Conversation History

For multi-turn conversations, summarize old turns instead of sending them verbatim:

```python
# Instead of sending 40 turns of history:
if len(messages) > 20:
    summary = summarize_history(messages[:-10])  # summarize older turns
    messages = [system_summary_message(summary)] + messages[-10:]
```

### Chunk Large Documents

Instead of sending a 200-page PDF, retrieve only the relevant pages using semantic search, then send only those chunks. See [[../../05_Agentic_Workflows/Theory/02_Memory_and_State|Memory & State — semantic memory]].

---

## Output Token Reduction

Output tokens are expensive. Instruct Claude to be concise:

```
"Answer in at most two sentences."
"Return JSON only. No explanation."
"List format, no headers, no preamble."
```

Set `max_tokens` conservatively. A classification task rarely needs more than 20 output tokens.

---

## Streaming for Perceived Performance

Streaming does not reduce token cost, but it significantly improves perceived performance because the user sees output as it is generated rather than waiting for the full response.

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

Use streaming for any user-facing interface where response time matters.

---

## Cost Monitoring

Always log `usage` from every response:

```python
response = client.messages.create(...)

log({
    "request_id":     response.id,
    "model":          response.model,
    "input_tokens":   response.usage.input_tokens,
    "output_tokens":  response.usage.output_tokens,
    "cache_read":     getattr(response.usage, "cache_read_input_tokens", 0),
    "cache_write":    getattr(response.usage, "cache_creation_input_tokens", 0),
    "timestamp":      datetime.utcnow().isoformat()
})
```

Aggregate by day, model, and task type to identify optimization opportunities.

---

## Cost Optimization Checklist

- [ ] Route simple tasks to Haiku
- [ ] Enable prompt caching for large, repeated prefixes
- [ ] Use Batch API for workloads that are not time-sensitive
- [ ] Trim system prompts of filler and redundancy
- [ ] Set tight `max_tokens` limits for constrained output tasks
- [ ] Compress conversation history for long sessions
- [ ] Log `usage` on every request for cost attribution

---

## Related Notes

- [[01_Caching_and_Batching|Caching & Batching]]
- [[03_Evaluation_and_Testing|Evaluation & Testing — measuring quality vs cost tradeoffs]]
- [[../../01_Claude_Models_and_API/Theory/01_Model_Overview|Model Overview — model capabilities]]

---

[[../_Index|← Back to Production & Evaluation Index]]
