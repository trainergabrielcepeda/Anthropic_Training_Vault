---
tags: [setup]
---

# Getting Started

Complete these steps before running any exercise in the vault.

---

## 1. Get an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com) and sign in.
2. Navigate to **API Keys** and click **Create Key**.
3. Copy the key — you will not be able to see it again.

> [!warning] Never commit your API key
> Do not paste your key into any file in this vault. Always load it from an environment variable.

---

## 2. Set the Environment Variable

### Linux / macOS

Add this line to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Then reload your shell:

```bash
source ~/.bashrc
```

### Windows (PowerShell)

```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY","sk-ant-...","User")
```

### Verify

```bash
echo $ANTHROPIC_API_KEY
```

---

## 3. Choose a Language and Install the SDK

Go to [[Environment_Setup]] for step-by-step instructions for Python, JavaScript, and TypeScript.

---

## 4. Run a Smoke Test

Once the SDK is installed, run the matching smoke test to confirm everything works.

**Python**

```python
import anthropic
client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=64,
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)
print(msg.content[0].text)
```

**JavaScript / TypeScript**

```javascript
import Anthropic from '@anthropic-ai/sdk';
const client = new Anthropic();
const msg = await client.messages.create({
  model: 'claude-haiku-4-5-20251001',
  max_tokens: 64,
  messages: [{ role: 'user', content: 'Say hello in one sentence.' }]
});
console.log(msg.content[0].text);
```

If you see a greeting printed, your setup is complete. Head to [[../Home|Home]] and pick a topic.
