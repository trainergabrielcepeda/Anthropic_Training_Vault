---
tags: [theory, api]
topic: "01 - Claude Models & API"
---

# API Fundamentals

## The Messages Endpoint

All interactions with Claude go through a single endpoint:

```
POST https://api.anthropic.com/v1/messages
```

### Minimal Request

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "messages": [
    { "role": "user", "content": "What is the capital of France?" }
  ]
}
```

### Full Request Shape

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "You are a helpful assistant.",
  "messages": [
    { "role": "user",      "content": "What is the capital of France?" },
    { "role": "assistant", "content": "The capital of France is Paris." },
    { "role": "user",      "content": "What is its population?" }
  ],
  "temperature": 1.0,
  "top_p": 0.999,
  "stop_sequences": ["\n\nHuman:"],
  "metadata": { "user_id": "user-123" }
}
```

---

## Request Parameters

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `model` | string | Yes | Model ID to use |
| `max_tokens` | integer | Yes | Maximum output tokens. Hard cap on generation length |
| `messages` | array | Yes | Alternating user/assistant turns |
| `system` | string | No | System prompt; sets Claude's persona and instructions |
| `temperature` | float 0–1 | No | Randomness. Default 1. Lower = more deterministic |
| `top_p` | float 0–1 | No | Nucleus sampling. Use either temperature or top_p, not both |
| `stop_sequences` | array | No | Strings that halt generation when encountered |
| `stream` | boolean | No | Enable server-sent event streaming |
| `metadata` | object | No | Arbitrary key-value data attached to the request |

> [!warning] `max_tokens` is not optional
> Unlike some APIs, `max_tokens` is required. If you omit it, the request fails with a 400 error.

---

## Response Structure

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Paris is the capital of France."
    }
  ],
  "model": "claude-sonnet-4-6",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 14,
    "output_tokens": 9
  }
}
```

### `stop_reason` Values

| Value | Meaning |
| ----- | ------- |
| `end_turn` | Claude finished naturally |
| `max_tokens` | Hit the `max_tokens` limit — response may be truncated |
| `stop_sequence` | A `stop_sequences` string was encountered |
| `tool_use` | Claude is invoking a tool; awaiting `tool_result` |

---

## Conversation State

The API is **stateless**. You are responsible for maintaining conversation history. Each request must include the full message array from the beginning of the conversation.

```python
messages = []

# Turn 1
messages.append({"role": "user", "content": "Hello"})
response = client.messages.create(model=..., messages=messages, max_tokens=256)
messages.append({"role": "assistant", "content": response.content[0].text})

# Turn 2
messages.append({"role": "user", "content": "What did I just say?"})
response = client.messages.create(model=..., messages=messages, max_tokens=256)
```

---

## Authentication

Every request requires the header:

```
x-api-key: YOUR_API_KEY
anthropic-version: 2023-06-01
```

The SDK sets both automatically when you instantiate the client.

---

## Error Codes

| HTTP Status | Type | Common Cause |
| ----------- | ---- | ------------ |
| 400 | `invalid_request_error` | Missing `max_tokens`, bad JSON, invalid role sequence |
| 401 | `authentication_error` | Invalid or missing API key |
| 403 | `permission_error` | Key lacks access to the requested model |
| 429 | `rate_limit_error` | Too many requests per minute or day |
| 500 | `api_error` | Transient server error — retry with exponential backoff |
| 529 | `overloaded_error` | Anthropic servers overloaded — retry |

---

## Related Notes

- [[01_Model_Overview|Model Overview]]
- [[03_Tokens_and_Context|Tokens & Context Windows]]
- [[../../03_Tool_Use/Theory/02_Tool_Call_Flow|Tool Call Flow]]

---

[[../_Index|← Back to Claude Models & API Index]]
