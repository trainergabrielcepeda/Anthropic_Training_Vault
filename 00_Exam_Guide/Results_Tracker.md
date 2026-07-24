---
tags: [hub, exam-guide, results-tracker]
topic: "00 - Exam Guide"
---

# Results Tracker — Practice Exam History

Tracks every practice-exam attempt over time so you can see which domains are actually ready and which still need review.

> [!info] How this works
> The browser quiz ([[01_Agentic_Architecture_and_Orchestration/Practice_Exam|Launch it from any domain's Practice Exam note]]) writes each attempt as a row into [[../Assets/exam_results.csv|Assets/exam_results.csv]] — a real file in this vault, not browser storage. The table below reads that same file and re-renders every time you open this note.
>
> **First time saving a result:** on the results screen, click **💾 Save Result** — Chrome/Edge will ask you to pick a file once. Navigate to `Assets/` and select the existing `exam_results.csv`. Every save after that is silent (no more prompts, unless the browser drops the permission grant between sessions, in which case you'll be asked to reconfirm).
>
> **Firefox / Safari:** the File System Access API isn't supported, so the button becomes **📋 Copy Row** instead — it copies a ready-made CSV row to your clipboard for you to paste at the end of `Assets/exam_results.csv` by hand.
>
> Verdict thresholds match the quiz's own color coding: **≥80% = ready**, **60–79% = review weak areas**, **<60% = restudy the theory**.

```js-engine
const path = 'Assets/exam_results.csv';
const container = document.createElement('div');

function csvParseLine(line) {
  const out = [];
  let cur = '', inQ = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (inQ) {
      if (c === '"' && line[i + 1] === '"') { cur += '"'; i++; }
      else if (c === '"') inQ = false;
      else cur += c;
    } else if (c === '"') inQ = true;
    else if (c === ',') { out.push(cur); cur = ''; }
    else cur += c;
  }
  out.push(cur);
  return out;
}

let rows = [];
try {
  const text = await app.vault.adapter.read(path);
  const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
  lines.shift(); // header
  rows = lines.map(csvParseLine).map(([date, domain, score, total, pct, timeSeconds]) => ({
    date, domain, score: +score, total: +total, pct: +pct, timeSeconds: +timeSeconds,
  }));
} catch (e) {
  container.textContent = `Could not read ${path}: ${e.message}`;
  return container;
}

if (!rows.length) {
  container.textContent = 'No attempts logged yet. Take a practice exam in the browser quiz and click "Save Result".';
  return container;
}

const byDomain = {};
rows.forEach(r => { (byDomain[r.domain] = byDomain[r.domain] || []).push(r); });

const verdictColor = (pct) => pct >= 80 ? '#a6e3a1' : pct >= 60 ? '#f9e2af' : '#f38ba8';

const summaryHeading = document.createElement('h3');
summaryHeading.textContent = 'Summary by Domain';
container.appendChild(summaryHeading);

const summary = document.createElement('table');
summary.innerHTML = '<tr><th>Domain</th><th>Attempts</th><th>Best</th><th>Last</th></tr>';
Object.entries(byDomain).forEach(([domain, attempts]) => {
  const best = Math.max(...attempts.map(a => a.pct));
  const last = attempts[attempts.length - 1].pct;
  const tr = document.createElement('tr');
  tr.innerHTML = `<td>${domain}</td><td>${attempts.length}</td>` +
    `<td style="color:${verdictColor(best)}">${best}%</td>` +
    `<td style="color:${verdictColor(last)}">${last}%</td>`;
  summary.appendChild(tr);
});
container.appendChild(summary);

const logHeading = document.createElement('h3');
logHeading.textContent = `Full Log (${rows.length} attempt${rows.length === 1 ? '' : 's'})`;
container.appendChild(logHeading);

const log = document.createElement('table');
log.innerHTML = '<tr><th>Date</th><th>Domain</th><th>Score</th><th>%</th><th>Time</th></tr>';
rows.slice().reverse().forEach(r => {
  const d = new Date(r.date);
  const dateStr = isNaN(d) ? r.date : d.toLocaleString();
  const m = Math.floor(r.timeSeconds / 60), s = r.timeSeconds % 60;
  const tr = document.createElement('tr');
  tr.innerHTML = `<td>${dateStr}</td><td>${r.domain}</td><td>${r.score}/${r.total}</td>` +
    `<td style="color:${verdictColor(r.pct)}">${r.pct}%</td><td>${m}:${String(s).padStart(2, '0')}</td>`;
  log.appendChild(tr);
});
container.appendChild(log);

return container;
```

---

[[_Index|← Exam Guide]] | [[../Home|← Home]]
