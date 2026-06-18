---
tags: [setup]
---

# Language Environment Setup

Detailed setup instructions for each supported language. All exercises in this vault use the official Anthropic SDK.

---

## Python

**Requirements:** Python 3.8+

```bash
# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate          # Windows

# Install the SDK
pip install anthropic
```

Every exercise folder contains a `requirements.txt`. To install it:

```bash
pip install -r requirements.txt
```

Verify:

```bash
python -c "import anthropic; print(anthropic.__version__)"
```

---

## JavaScript

**Requirements:** Node.js 18+

```bash
# Check your Node version
node --version

# Install the SDK globally (or per-project — see each exercise folder)
npm install @anthropic-ai/sdk
```

Exercises use ES modules. Each folder contains a `package.json` with `"type": "module"` already set.

Run an exercise:

```bash
node 01_basic_messages.js
```

---

## TypeScript

**Requirements:** Node.js 18+, TypeScript 5+

```bash
# Install TypeScript globally if you don't have it
npm install -g typescript ts-node

# Each exercise folder has its own package.json and tsconfig.json
cd Exercises/typescript
npm install
```

Run a TypeScript exercise:

```bash
npx ts-node 01_basic_messages.ts
```

Or compile first:

```bash
tsc && node dist/01_basic_messages.js
```

---

## Environment Variables Across Languages

All three SDKs automatically read `ANTHROPIC_API_KEY` from the environment. You never need to pass the key in code.

If you prefer a `.env` file during local development, use `python-dotenv` (Python) or `dotenv` (Node):

**Python**

```python
from dotenv import load_dotenv
load_dotenv()  # reads .env in the current directory
import anthropic
client = anthropic.Anthropic()
```

**JavaScript / TypeScript**

```javascript
import 'dotenv/config';
import Anthropic from '@anthropic-ai/sdk';
const client = new Anthropic();
```

> [!warning] .env files are gitignored
> The vault `.gitignore` already excludes `.env` and `.env.*`. Do not remove those entries.

---

## Model IDs Reference

| Alias | Full Model ID | Best For |
| ----- | ------------- | -------- |
| Haiku | `claude-haiku-4-5-20251001` | Fast, low-cost tasks |
| Sonnet | `claude-sonnet-4-6` | Balanced performance |
| Opus | `claude-opus-4-8` | Complex reasoning |

Use the full model ID in code. Aliases are for reference only.
