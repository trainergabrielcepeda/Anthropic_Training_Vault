# Anthropic CAA Architect Foundations — Training Vault

An Obsidian vault with structured study materials to prepare for the **Anthropic Certified AI Associate (CAA)** certification exam.

> **Start here if you haven't opened Obsidian yet.** This file covers cloning the repo, installing plugins, and connecting Claude Code. Once the vault is loaded in Obsidian, open **`Home.md`** — that's your study hub with topic navigation, exam weights, and links to all notes and exercises.

## What's Inside

This vault covers the core domains tested in the CAA exam, including:

- Claude model capabilities, limitations, and appropriate use cases
- Responsible AI principles and Anthropic's safety philosophy
- Prompt engineering best practices
- API usage and integration patterns
- Constitutional AI and RLHF concepts
- Evaluating and mitigating AI risks

## Getting Started

### Prerequisites

- [Obsidian](https://obsidian.md/) (free desktop app)
- Git

### Setup

1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd Anthropic_Training_Vault
   ```

2. Open the vault in Obsidian:
   - Launch Obsidian
   - Click **Open folder as vault**
   - Select the cloned directory

3. Enable community plugins:
   - Go to **Settings → Community plugins**
   - Turn off **Restricted mode** if prompted
   - Click **Turn on community plugins**

4. The vault includes three pre-configured plugins. Install each one via **Settings → Community plugins → Browse**, search by name, and click **Install** then **Enable**.

5. After enabling all three plugins, restart Obsidian to ensure they initialize correctly.

| Plugin | Purpose |
| ------ | ------- |
| **Git** | Syncs the vault with this repository — use it to pull updates and push your notes |
| **Terminal** | Opens a terminal panel inside Obsidian for running CLI commands |
| **Local REST API with MCP** | Exposes a local API so Claude Code and other AI tools can read and write your vault |

### Plugin Setup Details

#### Git
- On first use, go to **Settings → Git** and confirm your name and email match your Git config.
- Use the Git panel (ribbon icon or `Ctrl+P` → "Git: Open source control view") to pull, commit, and push.

#### Terminal
- Open a terminal via the ribbon icon or `Ctrl+P` → "Open terminal".
- The default shell on Linux/macOS is `/bin/sh`; you can change it in **Settings → Terminal → Profiles**.

#### Local REST API with MCP
- On first enable, the plugin generates an API key automatically — no manual configuration needed.
- Your API key is stored in `.obsidian/plugins/obsidian-local-rest-api/data.json`, which is gitignored and never shared.
- Enable the **HTTP server** in **Settings → Local REST API** — the plugin supports both HTTPS (port 27124) and HTTP (port 27123). Use HTTP to avoid self-signed certificate errors with Claude Code.
- The API is only accessible from your machine.
- To connect Claude Code, run `claude mcp add` and point it at the MCP endpoint shown in **Settings → Local REST API**.

## Using Claude Code with the Vault

Claude Code is Anthropic's official CLI that lets you work with Claude directly from a terminal. Combined with the Local REST API plugin, Claude can read and write notes in your vault.

### Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

You need Node.js 18+ installed. Verify with `node --version`.

### Start Claude Code inside the vault

Open a terminal (the Obsidian Terminal plugin or any system terminal), navigate to the vault root, and launch Claude Code:

```bash
cd /path/to/Anthropic_Training_Vault
claude
```

Claude Code will start in interactive mode. It uses the current directory as its working directory, so it can read and edit your vault notes directly.

### Connect Claude Code to the Local REST API (MCP)

This step lets Claude interact with Obsidian live — opening notes, searching, and writing back — through the MCP protocol.

1. Make sure the **Local REST API with MCP** plugin is running in Obsidian.
2. Find your API key in Obsidian: **Settings → Local REST API → API Key**.
3. In a terminal inside the vault, run the command below — replace `YOUR_API_KEY` with the key from step 2:
   ```bash
   claude mcp add --transport http obsidian-vault http://127.0.0.1:27123/mcp --header "Authorization: Bearer YOUR_API_KEY"
   ```
   > **Note:** Use `http://` (port 27123), not `https://` (port 27124). The HTTPS endpoint uses a self-signed certificate that Claude Code rejects.
4. Verify the connection:
   ```bash
   claude mcp list
   ```
   You should see `obsidian-vault` listed as an active MCP server.

After this, you can ask Claude things like "summarize all my notes on prompt engineering" or "create a new note about Constitutional AI" and it will act directly on your vault.

### Useful Claude Code commands

| Command | What it does |
| ------- | ------------ |
| `claude` | Start interactive session in the vault directory |
| `claude "your question"` | One-shot question, no interactive session |
| `claude mcp list` | Show connected MCP servers |
| `/help` | Show all available slash commands inside a session |
| `/quit` | Exit Claude Code |

## Contributing

1. Fork the repo and create a branch for your changes.
2. Add or update notes in the relevant section folder.
3. Open a pull request with a clear description of what you added or changed.

Please keep notes factually accurate and cite official Anthropic documentation where possible.

## Resources

- [Anthropic Documentation](https://docs.anthropic.com)
- [Claude Model Overview](https://www.anthropic.com/claude)
- [Anthropic Responsible Scaling Policy](https://www.anthropic.com/news/anthropics-responsible-scaling-policy)

## License

Study materials in this vault are intended for educational use. All Anthropic trademarks and product names remain the property of Anthropic.
