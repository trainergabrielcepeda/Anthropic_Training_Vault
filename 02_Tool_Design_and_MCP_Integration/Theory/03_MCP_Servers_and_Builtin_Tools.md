---
tags: [theory, mcp, builtin-tools, claude-code]
topic: "02 - Tool Design & MCP Integration"
task: "2.4, 2.5"
---

# MCP Servers & Built-in Tools

> [!important] Exam Tasks 2.4 & 2.5
> 2.4 — Integrate MCP servers into Claude Code and agent workflows.
> 2.5 — Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively.

---

## Part 1 — MCP Server Scoping

MCP (Model Context Protocol) servers plug external tools and data sources into Claude Code and agent workflows. Where you configure a server determines who gets it and how it's shared.

| Scope | File | Shared with team? | Typical use |
| ----- | ---- | ------------------ | ----------- |
| Project-level | `.mcp.json` at the repo root | Yes — checked into version control | Shared team tooling: Jira, internal APIs, the project's own database |
| User-level | `~/.claude.json` | No — personal to your machine | Personal or experimental servers you're trying out, that shouldn't affect teammates or get committed |

> [!example] Project-scoped `.mcp.json`
> ```json
> {
>   "mcpServers": {
>     "github": {
>       "command": "npx",
>       "args": ["-y", "@modelcontextprotocol/server-github"],
>       "env": {
>         "GITHUB_TOKEN": "${GITHUB_TOKEN}"
>       }
>     }
>   }
> }
> ```

### Environment Variable Expansion

`.mcp.json` supports `${VAR_NAME}` expansion, resolved from each developer's own environment at connection time. This is what makes a shared, version-controlled config safe: the file itself never contains a secret, only a reference to one. Every developer who clones the repo gets the same server configuration, but each supplies their own `GITHUB_TOKEN` (or equivalent) locally.

> [!warning] Never hardcode a credential into a committed `.mcp.json`
> If a server needs a secret, reference it with `${...}` expansion. A personal/experimental server that genuinely needs a hardcoded personal token belongs in `~/.claude.json`, not the project file.

### Tool Discovery Is Global Across Configured Servers

At connection time, Claude Code discovers the tools exposed by **every** configured MCP server — project-scoped and user-scoped — and makes them all available simultaneously in the same session. There's no per-turn server selection step; if you have five MCP servers configured, tools from all five are in scope together, alongside your built-in tools. This is part of why tool distribution discipline (see [[02_Error_Handling_and_Tool_Distribution|Error Handling & Tool Distribution]]) matters even more once several MCP servers are wired in — the combined tool count can grow quickly.

### MCP Resources — Reducing Exploratory Tool Calls

Beyond tools, MCP servers can expose **resources**: readable content the agent can pull directly, without a tool-call round trip. A resource is a good fit for anything that functions as a **content catalog** — something an agent would otherwise have to reconstruct through many exploratory calls:

- An issue tracker's full list of open issues with titles/status (instead of one `get_issue` call per issue just to see what exists)
- A documentation site's page hierarchy
- A database's schema (table names, columns, types)

> [!example] Resources vs. tools for the same data
> Without a resource: the agent calls `list_issues`, then calls `get_issue_detail` once per issue just to build a mental map before it can even start reasoning about the actual question ("what issues exist in this project?").
> With a resource: the agent reads an issue-summary catalog directly as context, skipping the exploratory round trips entirely, and only calls a tool once it needs to act on a specific issue.

### Enhancing MCP Tool Descriptions

Claude has built-in tools (like Grep) that are cheap, fast, and familiar from training — which means a poorly-described MCP tool with genuinely superior capabilities (e.g. semantic, ranked, cross-file search) can still lose out to Grep by default, simply because its description doesn't explain *why* it's the better choice for a given query. The fix is the same one from [[01_Tool_Interface_Design|Tool Interface Design]]: write the MCP tool's description to explicitly state its distinct capabilities and output shape, so Claude has a concrete reason to prefer it over a built-in alternative when it actually is the better tool for the job.

### Community Servers vs. Custom Servers

For standard, widely-used integrations (Jira, GitHub, Slack, Postgres, etc.), prefer an existing, maintained community MCP server over writing your own. Reserve custom MCP server development for genuinely team-specific workflows that no community server covers — internal APIs, proprietary data formats, or business logic unique to your organization. Building a custom server for something a community server already does well is unnecessary maintenance burden with no compensating benefit.

---

## Part 2 — Built-in Tool Selection

Claude Code ships with a fixed set of built-in tools for interacting with a local filesystem and shell. Choosing the right one for the job — rather than defaulting to the most familiar — is itself a tested skill.

| Tool | Matches on | Use for |
| ---- | ---------- | ------- |
| **Grep** | File **contents** | Finding function definitions, error message strings, import statements, all callers of a symbol |
| **Glob** | File **paths / names** | Finding files by naming pattern or extension, e.g. `**/*.test.tsx` |
| **Read** | Whole file | Loading a file's full content into context |
| **Write** | Whole file | Creating a new file, or replacing a file's entire content |
| **Edit** | A unique text anchor within a file | Targeted, surgical modification without touching the rest of the file |
| **Bash** | Shell commands | Anything not covered by the above — running builds, tests, git operations |

### Grep vs. Glob — Content vs. Path

These are frequently confused because both are "search" tools, but they answer different questions:

- **Grep** answers *"which files contain this text?"* — e.g. every file that calls `formatCurrency(`.
- **Glob** answers *"which files have this name/path pattern?"* — e.g. every file matching `**/*.test.tsx`, regardless of what's inside them.

Using Grep to hunt for files by extension (searching file contents for a literal string like `.test.tsx`) works by accident at best; Glob is the tool built for path-pattern matching and will be both faster and more reliable.

### Edit vs. Read+Write

Edit requires the anchor text you give it to be **unique** within the file — that's what makes it safe for targeted changes without accidentally touching unrelated occurrences. When Edit reports that your anchor isn't unique (it matches multiple locations), the correct fallback is **not** to force a blunt `replace_all`, and not to reach for a shell-level `sed` workaround. Use Read to load the full file, construct the complete updated content, and use Write to save it back in one shot.

> [!tip] Edit failing on non-uniqueness is a signal, not just an obstacle
> A non-unique anchor often means your surrounding context wasn't specific enough — sometimes the better fix is to include a few more lines of surrounding context in the anchor so Edit *can* pinpoint the one location you meant, keeping the surgical Edit approach instead of falling back to a full-file rewrite.

### Building Codebase Understanding Incrementally

For an unfamiliar codebase, reading every file up front doesn't scale and wastes context on irrelevant material. The efficient pattern is incremental:

1. **Grep** for entry points — a function name, a route definition, an error message seen in logs.
2. **Read** just the files that match, to see how they're structured and what they import.
3. Follow imports to the next relevant file, repeating Grep → Read as needed, rather than reading the whole tree upfront.

**Tracing usage across wrapper modules:** a function is sometimes re-exported under a different name by a wrapper module (`export { formatCurrency as formatMoney }`). A single Grep for the original name will miss every call site that uses the wrapper's name instead. The reliable approach: Grep for the function's definition first to find where it's exported and under what names, then Grep separately for each of those exported names across the codebase.

---

## Related Notes

- [[01_Tool_Interface_Design|Tool Interface Design]]
- [[02_Error_Handling_and_Tool_Distribution|Error Handling & Tool Distribution]]
- [[../../03_Claude_Code_Configuration_and_Workflows/_Index|Claude Code Configuration & Workflows]] — where `.claude/commands/`, `CLAUDE.md`, and other project-level configuration live
- [[../../00_Exam_Guide/Exam_Scenarios|Exam Scenarios — Scenario 4: Developer Productivity with Claude]]

---

[[../_Index|← Back to Domain 2 Index]]
