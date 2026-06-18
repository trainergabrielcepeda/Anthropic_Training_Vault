---
tags: [practice-exam, agents]
topic: "05 - Agentic Workflows"
questions: "05_Agentic_Workflows/Questions.json"
---

# Practice Exam — Agentic Workflows

> [!tip] Open Quiz in Browser
> The button below opens the quiz directly in your browser, pre-loaded on this topic.

```js-engine
const {shell} = require('electron');
const base = app.vault.adapter.basePath.replace(/\\/g, '/');
const url = base.startsWith('/') ? `file://${base}/Assets/quiz.html#4` : `file:///${base}/Assets/quiz.html#4`;
const btn = document.createElement('button');
btn.textContent = '🚀 Launch Practice Exam — Agentic Workflows';
btn.style.cssText = 'padding:9px 22px;background:var(--interactive-accent);color:var(--text-on-accent);border:none;border-radius:6px;cursor:pointer;font-size:0.93em;font-weight:600;font-family:inherit;';
btn.onmouseenter = () => btn.style.opacity = '0.8';
btn.onmouseleave = () => btn.style.opacity = '1';
btn.onclick = () => shell.openExternal(url);
return btn;
```

> [!note] Editing Questions
> Questions are stored in [[Questions.json]] inside this folder.
> Add, remove, or modify entries there, then run the build script from the vault root:
> ```
> python3 build_quiz.py
> ```
> The quiz rebuilds instantly — refresh the browser tab to see your changes.

---

[[_Index|← Topic Index]] | [[../04_Responsible_AI/Practice_Exam|← Previous Exam]] | [[../06_Production_and_Evaluation/Practice_Exam|Next: Production & Evaluation Exam →]]
