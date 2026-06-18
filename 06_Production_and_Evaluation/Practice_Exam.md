---
tags: [practice-exam, production, evaluation]
topic: "06 - Production & Evaluation"
questions: "06_Production_and_Evaluation/Questions.json"
---

# Practice Exam — Production & Evaluation

> [!tip] Open Quiz in Browser
> The button below opens the quiz directly in your browser, pre-loaded on this topic.

```js-engine
const {shell} = require('electron');
const base = app.vault.adapter.basePath.replace(/\\/g, '/');
const url = base.startsWith('/') ? `file://${base}/Assets/quiz.html#5` : `file:///${base}/Assets/quiz.html#5`;
const btn = document.createElement('button');
btn.textContent = '🚀 Launch Practice Exam — Production & Evaluation';
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

[[_Index|← Topic Index]] | [[../05_Agentic_Workflows/Practice_Exam|← Previous Exam]] | [[../Home|← Back to Home]]
