---
tags: [hub, navigation]
---

# Claude Certified Architect – Foundations (CCAR-F) — Training Vault

Use this vault as your single study hub. Each domain folder contains theory notes, hands-on exercises, and a practice exam you can take locally — mapped 1:1 to the five domains on Anthropic's official exam blueprint.

> [!tip] First time here?
> Haven't cloned the vault yet? Read the [[README]] first — it covers Obsidian installation, plugin setup, and Claude Code. Once the vault is running, come back here, skim [[00_Exam_Guide/_Index|the Exam Guide]] to see exactly what's tested, then follow [[00_Setup/Getting_Started]] to configure your API key and language SDKs.

> [!important] This exam is not what you think it is
> This is **not** a "what is Claude / prompt basics / AI safety" exam. It's an architecture exam: it assumes you can already write a prompt and tests whether you can build production systems that hold together — agentic loops, subagent orchestration, MCP tool design, Claude Code configuration, structured output, and context/reliability engineering. Read [[00_Exam_Guide/Out_of_Scope_Topics|what's explicitly out of scope]] before you burn study time on the wrong things.

---

## Start with the Exam Guide

| | |
| - | - |
| [[00_Exam_Guide/Exam_Overview\|Exam Overview]] | Format, scoring, fees, retake/renewal policy, domain weights |
| [[00_Exam_Guide/Exam_Scenarios\|The 6 Official Scenarios]] | The fixed scenario bank (4 of 6 appear on any given exam) that every question is anchored to |
| [[00_Exam_Guide/Official_Sample_Questions\|Official Sample Questions]] | 12 real, published items with explanations — the clearest signal of the exam's actual reasoning style |
| [[00_Exam_Guide/Out_of_Scope_Topics\|In-Scope vs. Out-of-Scope]] | Stop studying the wrong things |
| [[00_Exam_Guide/Results_Tracker\|Results Tracker]] | Your practice-exam history, scored per domain |

---

## Domains

| # | Domain | Weight | Theory | Exercises | Practice Exam |
| - | ------ | ------ | ------ | --------- | ------------- |
| 1 | [[01_Agentic_Architecture_and_Orchestration/_Index\|Agentic Architecture & Orchestration]] | **27%** | [[01_Agentic_Architecture_and_Orchestration/Theory/01_Agentic_Loops_and_Tool_Execution\|Agentic Loops]] · [[01_Agentic_Architecture_and_Orchestration/Theory/02_Multi_Agent_Orchestration\|Multi-Agent Orchestration]] · [[01_Agentic_Architecture_and_Orchestration/Theory/03_Workflow_Control_and_Session_Management\|Workflow Control & Sessions]] | [[01_Agentic_Architecture_and_Orchestration/Exercises/Setup\|Setup]] | [[01_Agentic_Architecture_and_Orchestration/Practice_Exam\|Start]] |
| 2 | [[02_Tool_Design_and_MCP_Integration/_Index\|Tool Design & MCP Integration]] | **18%** | [[02_Tool_Design_and_MCP_Integration/Theory/01_Tool_Interface_Design\|Tool Interface Design]] · [[02_Tool_Design_and_MCP_Integration/Theory/02_Error_Handling_and_Tool_Distribution\|Error Handling & Distribution]] · [[02_Tool_Design_and_MCP_Integration/Theory/03_MCP_Servers_and_Builtin_Tools\|MCP Servers & Built-in Tools]] | [[02_Tool_Design_and_MCP_Integration/Exercises/Setup\|Setup]] | [[02_Tool_Design_and_MCP_Integration/Practice_Exam\|Start]] |
| 3 | [[03_Claude_Code_Configuration_and_Workflows/_Index\|Claude Code Configuration & Workflows]] | **20%** | [[03_Claude_Code_Configuration_and_Workflows/Theory/01_CLAUDE_md_and_Configuration\|CLAUDE.md & Configuration]] · [[03_Claude_Code_Configuration_and_Workflows/Theory/02_Commands_Skills_and_Plan_Mode\|Commands, Skills & Plan Mode]] · [[03_Claude_Code_Configuration_and_Workflows/Theory/03_Iterative_Refinement_and_CICD\|Iterative Refinement & CI/CD]] | [[03_Claude_Code_Configuration_and_Workflows/Exercises/Setup\|Setup]] | [[03_Claude_Code_Configuration_and_Workflows/Practice_Exam\|Start]] |
| 4 | [[04_Prompt_Engineering_and_Structured_Output/_Index\|Prompt Engineering & Structured Output]] | **20%** | [[04_Prompt_Engineering_and_Structured_Output/Theory/01_Precision_and_Few_Shot_Prompting\|Precision & Few-Shot Prompting]] · [[04_Prompt_Engineering_and_Structured_Output/Theory/02_Structured_Output_and_Validation\|Structured Output & Validation]] · [[04_Prompt_Engineering_and_Structured_Output/Theory/03_Batch_Processing_and_Multi_Pass_Review\|Batch Processing & Multi-Pass Review]] | [[04_Prompt_Engineering_and_Structured_Output/Exercises/Setup\|Setup]] | [[04_Prompt_Engineering_and_Structured_Output/Practice_Exam\|Start]] |
| 5 | [[05_Context_Management_and_Reliability/_Index\|Context Management & Reliability]] | **15%** | [[05_Context_Management_and_Reliability/Theory/01_Context_Preservation_and_Escalation\|Context Preservation & Escalation]] · [[05_Context_Management_and_Reliability/Theory/02_Error_Propagation_and_Codebase_Context\|Error Propagation & Codebase Context]] · [[05_Context_Management_and_Reliability/Theory/03_Human_Review_and_Provenance\|Human Review & Provenance]] | [[05_Context_Management_and_Reliability/Exercises/Setup\|Setup]] | [[05_Context_Management_and_Reliability/Practice_Exam\|Start]] |

Domain numbering and weights above match Anthropic's official blueprint exactly (see [[00_Exam_Guide/Exam_Overview|Exam Overview]]) — they sum to 100%.

---

## Exam Facts Cheat Sheet

| | |
| - | - |
| Credential | Claude Certified Architect – Foundations (CCAR-F) |
| Items | 60, drawn from 4 of [[00_Exam_Guide/Exam_Scenarios\|6 fixed scenarios]] |
| Time | 120 minutes |
| Passing score | 720 / 1000 (criterion-referenced, not curved) |
| Fee | $125 USD |
| Delivery | Proctored — online or Pearson VUE test center |
| Validity | 12 months, free renewal assessment if taken on time |

Full detail in [[00_Exam_Guide/Exam_Overview|Exam Overview]].

---

## Quick Links

- [[00_Setup/Getting_Started|Environment Setup]]
- [[00_Setup/Environment_Setup|Language-Specific Setup]]
- [Anthropic Documentation](https://docs.anthropic.com)
- [Claude API Reference](https://docs.anthropic.com/en/api)
- [Claude Certified Architect – Foundations, official certification page](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification)
