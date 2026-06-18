/**
 * quiz_engine.js — Interactive quiz module for Obsidian JS Engine plugin
 * Requires: JS Engine by mProjectsCode (community plugin)
 *
 * Call from a js-engine code block:
 *   const m = await engine.importJs('Assets/quiz_engine.js');
 *   await m.run({ app, engine, component, context });
 *
 * The calling note must have this frontmatter key:
 *   questions: "XX_Folder/Questions.json"
 *
 * Questions.json schema:
 *   { "topic": "...", "questions": [{ "question": "...", "options": ["correct", "wrong", ...], "correct": 0, "explanation": "..." }] }
 *   "correct" is the zero-based index of the correct option. Options are shuffled on render.
 */

export async function run({ app, engine, component, context }) {
    const root = document.createElement('div');
    root.style.cssText = 'font-family: inherit; box-sizing: border-box;';

    // ── Load question bank ────────────────────────────────────────────
    const qPath = context.metadata?.frontmatter?.questions;
    if (!qPath) {
        renderError(root, 'Frontmatter key missing. Add:  questions: "XX_Topic/Questions.json"  to this note\'s frontmatter.');
        return root;
    }
    const qFile = app.vault.getAbstractFileByPath(qPath);
    if (!qFile) {
        renderError(root, `File not found in vault: ${qPath}`);
        return root;
    }
    let data;
    try {
        data = JSON.parse(await app.vault.read(qFile));
    } catch (e) {
        renderError(root, `JSON parse error in ${qPath}: ${e.message}`);
        return root;
    }
    if (!Array.isArray(data.questions) || data.questions.length === 0) {
        renderError(root, `No questions found in ${qPath}`);
        return root;
    }

    // ── Quiz state ────────────────────────────────────────────────────
    let bank = shuffle([...data.questions]);
    let current = 0;
    let score = 0;

    renderQuestion();
    return root;

    // ── Question renderer ─────────────────────────────────────────────
    function renderQuestion() {
        root.innerHTML = '';

        if (current >= bank.length) {
            renderResults();
            return;
        }

        const q = bank[current];
        const shuffledOpts = shuffle(
            q.options.map((text, i) => ({ text, isCorrect: i === q.correct }))
        );
        let answered = false;
        const LABELS = ['A', 'B', 'C', 'D'];

        const wrap = el('div', 'max-width: 680px;');

        // Progress header
        const header = el('div', 'display: flex; justify-content: space-between; font-size: 0.81em; color: var(--text-muted); margin-bottom: 5px;');
        header.append(
            el('span', '', `Question ${current + 1} / ${bank.length}`),
            el('span', '', `Score: ${score} / ${current}`)
        );

        // Progress bar
        const track = el('div', 'height: 3px; background: var(--background-modifier-border); border-radius: 2px; margin-bottom: 1.3em;');
        track.appendChild(el('div', `height: 100%; width: ${(current / bank.length * 100).toFixed(1)}%; background: var(--interactive-accent); border-radius: 2px;`));

        // Question text
        const qText = el('p', 'font-weight: 600; font-size: 1.03em; line-height: 1.55; margin: 0 0 1.1em; color: var(--text-normal);', q.question);

        // Options
        const optList = el('div', 'display: flex; flex-direction: column; gap: 7px;');
        const buttons = [];

        shuffledOpts.forEach((opt, i) => {
            const btn = document.createElement('button');
            btnStyle(btn, 'idle');

            const lbl = el('span', 'font-weight: 700; min-width: 22px; flex-shrink: 0; color: var(--interactive-accent);', LABELS[i] + '.');
            const txt = el('span', 'line-height: 1.45; text-align: left;', opt.text);
            btn.append(lbl, txt);

            btn.addEventListener('mouseenter', () => { if (!answered) btnStyle(btn, 'hover'); });
            btn.addEventListener('mouseleave', () => { if (!answered) btnStyle(btn, 'idle'); });

            btn.addEventListener('click', () => {
                if (answered) return;
                answered = true;
                buttons.forEach(b => { b.style.cursor = 'default'; b.style.pointerEvents = 'none'; });

                if (opt.isCorrect) {
                    score++;
                    btnStyle(btn, 'correct');
                    lbl.style.color = '#22c55e';
                } else {
                    btnStyle(btn, 'wrong');
                    lbl.style.color = '#ef4444';
                    // Reveal the correct answer
                    buttons.forEach((b, bi) => {
                        if (shuffledOpts[bi].isCorrect) {
                            btnStyle(b, 'correct');
                            b.querySelector('span').style.color = '#22c55e';
                        }
                    });
                }

                // Explanation
                const expBox = el('div', 'margin-top: 13px; padding: 12px 16px; border-left: 3px solid var(--interactive-accent); background: var(--background-secondary); border-radius: 0 7px 7px 0; font-size: 0.9em; line-height: 1.5; color: var(--text-normal);');
                const badge = document.createElement('strong');
                badge.style.color = opt.isCorrect ? '#22c55e' : '#ef4444';
                badge.textContent = opt.isCorrect ? '✓ Correct.  ' : '✗ Incorrect.  ';
                expBox.append(badge, document.createTextNode(q.explanation));

                // Next / Results button
                const isLast = current + 1 >= bank.length;
                const nextBtn = document.createElement('button');
                nextBtn.textContent = isLast ? 'See Results →' : 'Next Question →';
                btnStyle(nextBtn, 'next');
                nextBtn.addEventListener('mouseenter', () => nextBtn.style.opacity = '0.85');
                nextBtn.addEventListener('mouseleave', () => nextBtn.style.opacity = '1');
                nextBtn.addEventListener('click', () => { current++; renderQuestion(); });

                wrap.append(expBox, nextBtn);
            });

            buttons.push(btn);
            optList.appendChild(btn);
        });

        wrap.append(header, track, qText, optList);
        root.appendChild(wrap);
    }

    // ── Results renderer ──────────────────────────────────────────────
    function renderResults() {
        root.innerHTML = '';
        const n = bank.length;
        const pct = Math.round(score / n * 100);
        const [msg, color] =
            pct >= 80 ? ['Ready for the exam', '#22c55e'] :
            pct >= 60 ? ['Review weak areas, then retry', '#f59e0b'] :
                        ['Study the theory notes, then retry', '#ef4444'];

        const wrap = el('div', 'text-align: center; padding: 2.8em 1em; max-width: 440px; margin: 0 auto;');

        const scoreEl = el('div', `font-size: 3.2em; font-weight: 800; line-height: 1; color: ${color};`, `${score} / ${n}`);
        const pctEl   = el('div', 'font-size: 1.1em; color: var(--text-muted); margin-top: 6px;', `${pct}%`);
        const msgEl   = el('div', `font-size: 0.97em; font-weight: 600; color: ${color}; margin: 12px 0 28px;`, msg);

        const retryBtn = document.createElement('button');
        retryBtn.textContent = 'Retry ↺';
        btnStyle(retryBtn, 'next');
        retryBtn.addEventListener('mouseenter', () => retryBtn.style.opacity = '0.85');
        retryBtn.addEventListener('mouseleave', () => retryBtn.style.opacity = '1');
        retryBtn.addEventListener('click', () => {
            bank = shuffle([...data.questions]);
            current = 0;
            score = 0;
            renderQuestion();
        });

        wrap.append(scoreEl, pctEl, msgEl, retryBtn);
        root.appendChild(wrap);
    }

    // ── DOM helpers ───────────────────────────────────────────────────
    function el(tag, style, text) {
        const e = document.createElement(tag);
        if (style) e.style.cssText = style;
        if (text != null) e.textContent = text;
        return e;
    }

    function renderError(container, msg) {
        const e = el('div',
            'padding: 1em; color: #ef4444; background: var(--background-secondary); border-radius: 6px; border-left: 3px solid #ef4444; font-size: 0.9em;',
            '⚠ Quiz engine: ' + msg
        );
        container.appendChild(e);
    }

    function btnStyle(btn, state) {
        const base = 'display: flex; align-items: flex-start; gap: 10px; width: 100%; padding: 10px 14px; text-align: left; font-size: 0.93em; border-radius: 7px; font-family: inherit; transition: border-color 0.1s;';
        switch (state) {
            case 'idle':
                btn.style.cssText = base + 'cursor: pointer; border: 1px solid var(--background-modifier-border); background: var(--background-secondary); color: var(--text-normal);';
                break;
            case 'hover':
                btn.style.cssText = base + 'cursor: pointer; border: 1px solid var(--interactive-accent); background: var(--background-secondary); color: var(--text-normal);';
                break;
            case 'correct':
                btn.style.cssText = base + 'cursor: default; border: 1px solid #22c55e; background: rgba(34,197,94,0.10); color: var(--text-normal);';
                break;
            case 'wrong':
                btn.style.cssText = base + 'cursor: default; border: 1px solid #ef4444; background: rgba(239,68,68,0.10); color: var(--text-normal);';
                break;
            case 'next':
                btn.style.cssText = 'display: inline-block; margin-top: 14px; padding: 9px 20px; background: var(--interactive-accent); color: var(--text-on-accent); border: none; border-radius: 7px; cursor: pointer; font-size: 0.93em; font-weight: 600; font-family: inherit;';
                break;
        }
    }

    function shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }
}
