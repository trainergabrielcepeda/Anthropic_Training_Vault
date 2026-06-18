---
tags: [practice-exam, prompting]
topic: "02 - Prompt Engineering"
questions: "02_Prompt_Engineering/Questions.json"
---

# Practice Exam — Prompt Engineering

> [!tip] Open Quiz in Browser
> The button below opens the quiz directly in your browser, pre-loaded on this topic.

```js-engine
const {shell} = require('electron');
const base = app.vault.adapter.basePath.replace(/\\/g, '/');
const url = base.startsWith('/') ? `file://${base}/Assets/quiz.html#1` : `file:///${base}/Assets/quiz.html#1`;
const btn = document.createElement('button');
btn.textContent = '🚀 Launch Practice Exam — Prompt Engineering';
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

[[_Index|← Topic Index]] | [[../01_Claude_Models_and_API/Practice_Exam|← Previous Exam]] | [[../03_Tool_Use/Practice_Exam|Next: Tool Use Exam →]]
