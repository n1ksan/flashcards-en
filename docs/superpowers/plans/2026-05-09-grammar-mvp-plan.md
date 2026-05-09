# План: Grammar MVP (Present Simple)

**Goal:** Добавить раздел «Грамматика» в Mini App — 4-я вкладка нижней навигации, одна тема (Present Simple), полный пайплайн правило → 6 упражнений → итог. Прогресс в CloudStorage, секция в Статистике.

**Спецификация:** [docs/superpowers/specs/2026-05-09-grammar-section-design.md](../specs/2026-05-09-grammar-section-design.md)

## Architecture overview

- Нет роутера — все вкладки `display:flex/none` через `showView()`.
- Грамматика — внутреннее состояние одного view со sub-блоками `#grammar-topics`, `#grammar-lesson`, `#grammar-exercise`, `#grammar-result`. Переключаются через `setGrammarState()`.
- Прогресс грамматики — отдельный JSON в CloudStorage по ключу `grammar_progress`: `{ topicId: { best: int, total: int, attempts: int } }`. Не пересекается с `learnedSet` других наборов.
- Карточки тем визуально совпадают с `.folder-card`; таблица форм и блок упражнений используют новые классы с базовыми токенами темы.

## Tech stack

Без сборки. Чистый HTML/CSS/JS, всё в одном файле [index.html](../../../index.html). Данные грамматики — отдельный JS-файл `data-grammar.js`, экспортирующий `window.GRAMMAR`.

## Files to create / modify

| Файл                                         | Действие | Назначение                                  |
|----------------------------------------------|----------|---------------------------------------------|
| `d:\quizlet\data-grammar.js`                 | создать  | Массив `GRAMMAR` с одной темой Present Simple |
| `d:\quizlet\index.html`                      | менять   | Подключение скрипта, CSS, HTML view, JS     |

---

## Tasks

### Task 1 — Создать `data-grammar.js` с Present Simple

**Файл:** `d:\quizlet\data-grammar.js` (новый)

**Содержимое:**

```js
window.GRAMMAR = [
  {
    id: 'present_simple',
    level: 'A1',
    title: 'Present Simple',
    summary: 'Регулярные действия, факты и привычки',
    rule: 'Present Simple используется для регулярных действий, привычек, общих фактов и расписаний. Часто употребляется с наречиями частоты: always, usually, often, sometimes, never; а также every day / week / year.',
    table: [
      { form: 'I / You / We / They + verb',           ex: 'I work in an office.' },
      { form: 'He / She / It + verb-s',                ex: 'She works in an office.' },
      { form: 'do / does + not + verb (отрицание)',    ex: "He doesn't work here." },
      { form: 'Do / Does + subject + verb? (вопрос)',  ex: 'Do you work here?' },
    ],
    examples: [
      { en: 'I get up at seven every day.',     ru: 'Я встаю в семь каждый день.' },
      { en: 'She speaks three languages.',      ru: 'Она говорит на трёх языках.' },
      { en: "We don't live in London.",         ru: 'Мы не живём в Лондоне.' },
      { en: 'Does he play tennis on Sundays?',  ru: 'Он играет в теннис по воскресеньям?' },
    ],
    exercises: [
      { sentence: 'She ___ to school every day.',     hint: 'go',        answers: ['goes'],                              translation: 'Она ходит в школу каждый день.' },
      { sentence: 'I usually ___ tea in the morning.', hint: 'drink',     answers: ['drink'],                             translation: 'Обычно я пью чай по утрам.' },
      { sentence: 'He ___ work on Sundays.',           hint: 'not work',  answers: ["doesn't work", 'does not work'],     translation: 'Он не работает по воскресеньям.' },
      { sentence: '___ you speak French?',             hint: 'do / does', answers: ['do'],                                translation: 'Ты говоришь по-французски?' },
      { sentence: 'My brother ___ pizza.',             hint: 'love',      answers: ['loves'],                             translation: 'Мой брат любит пиццу.' },
      { sentence: 'They ___ in this city.',            hint: 'not live',  answers: ["don't live", 'do not live'],         translation: 'Они не живут в этом городе.' },
    ],
  },
];
```

**Проверка:** открыть файл в браузере через DevTools → `window.GRAMMAR[0].exercises.length` должно вернуть `6`.

---

### Task 2 — Подключить `data-grammar.js`

**Файл:** [d:\quizlet\index.html](../../../index.html), строка 11

**Старое:**

```html
<script src="data-thematic.js"></script>
<script src="data-b2.js"></script>
<script src="data-idioms.js"></script>
```

**Новое:**

```html
<script src="data-thematic.js"></script>
<script src="data-b2.js"></script>
<script src="data-idioms.js"></script>
<script src="data-grammar.js"></script>
```

---

### Task 3 — Добавить CSS для раздела грамматики

**Файл:** [d:\quizlet\index.html](../../../index.html), вставить **перед** `</style>` (строка 191).

**Что вставить:**

```css
  /* ── GRAMMAR ── */
  #view-grammar { width:100%; min-height:100vh; display:none; flex-direction:column; align-items:center; }
  .grammar-main { width:100%; max-width:600px; padding:20px 16px 90px; display:flex; flex-direction:column; gap:14px; }
  .grammar-back-btn { background:none; border:none; color:var(--muted); font-size:14px; cursor:pointer; padding:6px 10px; border-radius:8px; align-self:flex-start; -webkit-tap-highlight-color:transparent; }
  .grammar-back-btn:active { background:var(--surface); }

  .level-group-title { font-size:11px; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:.6px; margin-top:6px; }

  .topic-card { background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:14px 15px; display:flex; align-items:center; gap:12px; cursor:pointer; transition:all .2s; -webkit-tap-highlight-color:transparent; }
  .topic-card:active { transform:scale(.98); }
  .topic-card.done { border-color:rgba(46,204,113,.4); background:rgba(46,204,113,.06); }
  .topic-info { flex:1; min-width:0; }
  .topic-title { font-size:15px; font-weight:700; margin-bottom:3px; }
  .topic-summary { font-size:12px; color:var(--muted); }
  .topic-score { font-size:11px; color:var(--muted); margin-top:5px; }
  .topic-score.done { color:var(--green); font-weight:600; }
  .level-badge { font-size:10px; font-weight:700; padding:3px 8px; border-radius:100px; flex-shrink:0; }
  .level-A1 { background:rgba(46,204,113,.15); color:var(--green); }
  .level-A2 { background:rgba(79,110,247,.15); color:var(--accent); }
  .level-B1 { background:rgba(155,89,182,.15); color:#b277e0; }
  .level-B2 { background:rgba(243,156,18,.15); color:var(--yellow); }

  .lesson-card { background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:18px 16px; display:flex; flex-direction:column; gap:14px; }
  .lesson-title-row { display:flex; align-items:center; gap:10px; }
  .lesson-title { font-size:20px; font-weight:700; flex:1; }
  .lesson-rule { font-size:14px; line-height:1.55; color:var(--text); }
  .lesson-section-title { font-size:12px; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:.5px; margin-top:4px; }
  .lesson-table { display:flex; flex-direction:column; gap:6px; }
  .lesson-table-row { background:var(--bg); border:1px solid var(--border); border-radius:10px; padding:10px 12px; font-size:13px; }
  .lesson-table-row .lt-form { font-weight:600; color:var(--text); }
  .lesson-table-row .lt-ex { color:var(--muted); font-style:italic; margin-top:3px; font-size:12px; }
  .lesson-examples { display:flex; flex-direction:column; gap:8px; }
  .lesson-example { background:var(--bg); border-left:3px solid var(--accent); border-radius:8px; padding:8px 12px; }
  .lesson-example-en { font-size:14px; font-weight:600; }
  .lesson-example-ru { font-size:12px; color:var(--muted); margin-top:2px; }
  .lesson-start-btn { padding:13px; border-radius:var(--radius); border:none; background:var(--accent); color:var(--acc-t); font-size:15px; font-weight:700; cursor:pointer; transition:all .2s; -webkit-tap-highlight-color:transparent; }
  .lesson-start-btn:active { transform:scale(.97); }

  .ex-card { background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:18px 16px; display:flex; flex-direction:column; gap:12px; }
  .ex-sentence { font-size:18px; font-weight:600; line-height:1.45; text-align:center; }
  .ex-sentence .blank { display:inline-block; min-width:80px; border-bottom:2px dashed var(--muted); padding:0 6px; color:var(--accent); }
  .ex-hint { font-size:13px; color:var(--muted); text-align:center; font-style:italic; }
  .ex-translation { font-size:12px; color:var(--muted); text-align:center; }
  .ex-input { width:100%; padding:12px 14px; border-radius:12px; border:2px solid var(--border); background:var(--bg); color:var(--text); font-size:15px; outline:none; transition:border-color .2s; }
  .ex-input:focus { border-color:var(--accent); }
  .ex-input.correct { border-color:var(--green); background:rgba(46,204,113,.08); }
  .ex-input.wrong   { border-color:var(--red);   background:rgba(231,76,60,.08); }
  .ex-feedback { font-size:13px; padding:8px 12px; border-radius:10px; display:none; }
  .ex-feedback.show { display:block; }
  .ex-feedback.correct { background:rgba(46,204,113,.1); color:var(--green); border:1px solid rgba(46,204,113,.3); }
  .ex-feedback.wrong   { background:rgba(231,76,60,.1);  color:var(--red);   border:1px solid rgba(231,76,60,.3); }
  .ex-actions { display:flex; gap:8px; }
  .ex-btn { flex:1; padding:12px; border-radius:var(--radius); border:none; font-size:14px; font-weight:700; cursor:pointer; transition:all .2s; -webkit-tap-highlight-color:transparent; }
  .ex-btn:active { transform:scale(.97); }
  .ex-btn.primary { background:var(--accent); color:var(--acc-t); }
  .ex-btn.secondary { background:var(--bg); color:var(--text); border:1px solid var(--border); }

  .ex-progress-row { display:flex; align-items:center; gap:10px; }
  .ex-progress-bar { flex:1; height:6px; background:var(--surface); border-radius:3px; overflow:hidden; border:1px solid var(--border); }
  .ex-progress-fill { height:100%; background:var(--accent); border-radius:3px; transition:width .4s ease; }
  .ex-progress-label { font-size:12px; color:var(--muted); min-width:48px; text-align:right; }

  .grammar-result { background:var(--surface); border:1px solid var(--border); border-radius:24px; padding:32px 24px; text-align:center; display:flex; flex-direction:column; gap:16px; }
  .gr-emoji { font-size:48px; }
  .gr-title { font-size:20px; font-weight:700; }
  .gr-score { font-size:48px; font-weight:700; color:var(--accent); line-height:1; }
  .gr-score-lbl { font-size:13px; color:var(--muted); }
  .gr-actions { display:flex; flex-direction:column; gap:10px; }
```

**Куда:** между строкой `190` (`.round-btn:active { transform:scale(.97); }`) и закрывающим `</style>`.

---

### Task 4 — Добавить HTML-блок `#view-grammar`

**Файл:** [d:\quizlet\index.html](../../../index.html), вставить **перед** комментарием `<!-- ══════════ STATS VIEW ══════════ -->` (строка ~344).

**Что вставить:**

```html
<!-- ══════════ GRAMMAR VIEW ══════════ -->
<div id="view-grammar">
  <header>
    <div class="logo">📚 Грамматика</div>
  </header>
  <div class="grammar-main" id="grammar-main">

    <!-- State: topics list -->
    <div id="grammar-topics" style="display:flex; flex-direction:column; gap:12px;">
      <div class="section-title">Выберите тему</div>
      <div id="grammar-topics-list" style="display:flex; flex-direction:column; gap:10px;"></div>
    </div>

    <!-- State: lesson (rule + examples) -->
    <div id="grammar-lesson" style="display:none; flex-direction:column; gap:12px;">
      <button class="grammar-back-btn" onclick="setGrammarState('topics')">‹ К списку тем</button>
      <div class="lesson-card">
        <div class="lesson-title-row">
          <div class="lesson-title" id="lesson-title">—</div>
          <span class="level-badge" id="lesson-level">A1</span>
        </div>
        <div class="lesson-rule" id="lesson-rule">—</div>
        <div class="lesson-section-title">Формы</div>
        <div class="lesson-table" id="lesson-table"></div>
        <div class="lesson-section-title">Примеры</div>
        <div class="lesson-examples" id="lesson-examples"></div>
        <button class="lesson-start-btn" onclick="startGrammarExercises()">▶ Начать упражнения</button>
      </div>
    </div>

    <!-- State: exercise -->
    <div id="grammar-exercise" style="display:none; flex-direction:column; gap:12px;">
      <button class="grammar-back-btn" onclick="setGrammarState('lesson')">‹ К правилу</button>
      <div class="ex-progress-row">
        <div class="ex-progress-bar"><div class="ex-progress-fill" id="ex-progress-fill" style="width:0%"></div></div>
        <div class="ex-progress-label" id="ex-progress-label">0 / 0</div>
      </div>
      <div class="ex-card">
        <div class="ex-sentence" id="ex-sentence">—</div>
        <div class="ex-hint" id="ex-hint">—</div>
        <input type="text" class="ex-input" id="ex-input"
               placeholder="Введите ответ"
               autocapitalize="off" autocorrect="off" autocomplete="off" spellcheck="false">
        <div class="ex-feedback" id="ex-feedback"></div>
        <div class="ex-translation" id="ex-translation"></div>
        <div class="ex-actions">
          <button class="ex-btn primary" id="ex-action-btn" onclick="onExerciseAction()">Проверить</button>
        </div>
      </div>
    </div>

    <!-- State: result -->
    <div id="grammar-result" style="display:none; flex-direction:column; gap:12px;">
      <div class="grammar-result">
        <div class="gr-emoji" id="gr-emoji">🎉</div>
        <div class="gr-title" id="gr-title">Отлично!</div>
        <div>
          <div class="gr-score" id="gr-score">0 / 0</div>
          <div class="gr-score-lbl">правильных ответов</div>
        </div>
        <div class="gr-actions">
          <button class="ex-btn primary" onclick="startGrammarExercises()">↺ Пройти заново</button>
          <button class="ex-btn secondary" onclick="setGrammarState('lesson')">📖 К правилу</button>
          <button class="ex-btn secondary" onclick="setGrammarState('topics')">‹ К списку тем</button>
        </div>
      </div>
    </div>

  </div>
</div>
```

---

### Task 5 — Добавить 4-ю кнопку в `<nav id="bottom-nav">`

**Файл:** [d:\quizlet\index.html](../../../index.html), строки 353–366.

**Старое:**

```html
<nav id="bottom-nav">
  <button class="nav-item active" id="nav-folders" onclick="switchTab('folders')">
    <span class="nav-icon">📁</span>
    <span class="nav-label">Папки</span>
  </button>
  <button class="nav-item" id="nav-cards" onclick="switchTab('cards')">
    <span class="nav-icon">🃏</span>
    <span class="nav-label">Карточки</span>
  </button>
  <button class="nav-item" id="nav-stats" onclick="switchTab('stats')">
    <span class="nav-icon">📊</span>
    <span class="nav-label">Статистика</span>
  </button>
</nav>
```

**Новое:**

```html
<nav id="bottom-nav">
  <button class="nav-item active" id="nav-folders" onclick="switchTab('folders')">
    <span class="nav-icon">📁</span>
    <span class="nav-label">Папки</span>
  </button>
  <button class="nav-item" id="nav-cards" onclick="switchTab('cards')">
    <span class="nav-icon">🃏</span>
    <span class="nav-label">Карточки</span>
  </button>
  <button class="nav-item" id="nav-grammar" onclick="switchTab('grammar')">
    <span class="nav-icon">📚</span>
    <span class="nav-label">Грамматика</span>
  </button>
  <button class="nav-item" id="nav-stats" onclick="switchTab('stats')">
    <span class="nav-icon">📊</span>
    <span class="nav-label">Статистика</span>
  </button>
</nav>
```

---

### Task 6 — Расширить `showView()` и `switchTab()`

**Файл:** [d:\quizlet\index.html](../../../index.html), функция `showView` (строки 453–457).

**Старое:**

```js
function showView(view) {
  document.getElementById('view-home').style.display  = view === 'folders' ? 'flex' : 'none';
  document.getElementById('view-study').style.display = view === 'cards'   ? 'flex' : 'none';
  document.getElementById('view-stats').style.display = view === 'stats'   ? 'flex' : 'none';
}
```

**Новое:**

```js
function showView(view) {
  document.getElementById('view-home').style.display    = view === 'folders' ? 'flex' : 'none';
  document.getElementById('view-study').style.display   = view === 'cards'   ? 'flex' : 'none';
  document.getElementById('view-grammar').style.display = view === 'grammar' ? 'flex' : 'none';
  document.getElementById('view-stats').style.display   = view === 'stats'   ? 'flex' : 'none';
}
```

В функции `switchTab` (строки 459–478) — после блока `else if (tab === 'cards')` добавить новую ветку перед `else if (tab === 'stats')`.

**Старое:**

```js
  } else if (tab === 'cards') {
    if (studyActive) { showView('cards'); }
    else { startStudy(); }
  } else if (tab === 'stats') {
    showView('stats');
    loadStats();
  }
```

**Новое:**

```js
  } else if (tab === 'cards') {
    if (studyActive) { showView('cards'); }
    else { startStudy(); }
  } else if (tab === 'grammar') {
    showView('grammar');
    openGrammar();
  } else if (tab === 'stats') {
    showView('stats');
    loadStats();
  }
```

---

### Task 7 — Добавить JS-логику грамматики

**Файл:** [d:\quizlet\index.html](../../../index.html), вставить **перед** строкой `document.addEventListener('keydown',e=>{` (строка ~813).

**Что вставить:**

```js
// ── GRAMMAR ──────────────────────────────────────────────────────────────────
const LEVELS = ['A1','A2','B1','B2'];
let grammarProgress = {};   // { topicId: { best, total, attempts } }
let currentGrammarTopic = null;
let exerciseIdx = 0;
let exerciseCorrect = 0;
let exerciseChecked = false;

function loadGrammarProgress(cb) {
  storage.get('grammar_progress', val => {
    grammarProgress = val ? JSON.parse(val) : {};
    if (cb) cb();
  });
}
function saveGrammarProgress() {
  storage.set('grammar_progress', JSON.stringify(grammarProgress));
}

function openGrammar() {
  loadGrammarProgress(() => {
    setGrammarState('topics');
    renderTopicList();
  });
}

function setGrammarState(state) {
  ['topics','lesson','exercise','result'].forEach(s => {
    const el = document.getElementById(`grammar-${s}`);
    if (el) el.style.display = (s === state) ? 'flex' : 'none';
  });
}

function renderTopicList() {
  const list = document.getElementById('grammar-topics-list');
  list.innerHTML = '';
  const topics = window.GRAMMAR || [];

  for (const level of LEVELS) {
    const topicsAtLevel = topics.filter(t => t.level === level);
    if (!topicsAtLevel.length) continue;
    const groupTitle = document.createElement('div');
    groupTitle.className = 'level-group-title';
    groupTitle.textContent = level;
    list.appendChild(groupTitle);

    for (const topic of topicsAtLevel) {
      const prog = grammarProgress[topic.id];
      const total = topic.exercises.length;
      const best  = prog ? prog.best : null;
      const isDone = prog && prog.best === total;
      const card = document.createElement('div');
      card.className = 'topic-card' + (isDone ? ' done' : '');
      card.onclick = () => openTopic(topic);
      card.innerHTML = `
        <div class="topic-info">
          <div class="topic-title">${topic.title}</div>
          <div class="topic-summary">${topic.summary}</div>
          <div class="topic-score ${isDone ? 'done' : ''}">${
            best === null ? `${total} упр.`
                          : `Лучший: ${best} / ${total}${isDone ? ' ✓' : ''}`
          }</div>
        </div>
        <span class="level-badge level-${topic.level}">${topic.level}</span>
      `;
      list.appendChild(card);
    }
  }
}

function openTopic(topic) {
  currentGrammarTopic = topic;
  document.getElementById('lesson-title').textContent = topic.title;
  const lvlEl = document.getElementById('lesson-level');
  lvlEl.textContent = topic.level;
  lvlEl.className = `level-badge level-${topic.level}`;
  document.getElementById('lesson-rule').textContent = topic.rule;

  const tableEl = document.getElementById('lesson-table');
  tableEl.innerHTML = '';
  topic.table.forEach(row => {
    const r = document.createElement('div');
    r.className = 'lesson-table-row';
    r.innerHTML = `<div class="lt-form">${row.form}</div><div class="lt-ex">${row.ex}</div>`;
    tableEl.appendChild(r);
  });

  const exEl = document.getElementById('lesson-examples');
  exEl.innerHTML = '';
  topic.examples.forEach(ex => {
    const e = document.createElement('div');
    e.className = 'lesson-example';
    e.innerHTML = `<div class="lesson-example-en">${ex.en}</div><div class="lesson-example-ru">${ex.ru}</div>`;
    exEl.appendChild(e);
  });

  setGrammarState('lesson');
}

function startGrammarExercises() {
  if (!currentGrammarTopic) return;
  exerciseIdx = 0;
  exerciseCorrect = 0;
  exerciseChecked = false;
  setGrammarState('exercise');
  renderExercise();
}

function renderExercise() {
  const t = currentGrammarTopic;
  if (!t) return;
  const ex = t.exercises[exerciseIdx];
  const total = t.exercises.length;
  const pos = exerciseIdx + 1;

  document.getElementById('ex-progress-fill').style.width = `${(pos/total)*100}%`;
  document.getElementById('ex-progress-label').textContent = `${pos} / ${total}`;
  document.getElementById('ex-sentence').innerHTML = ex.sentence.replace(/___/g, '<span class="blank">___</span>');
  document.getElementById('ex-hint').textContent = `подсказка: ${ex.hint}`;
  document.getElementById('ex-translation').textContent = '';
  const input = document.getElementById('ex-input');
  input.value = '';
  input.disabled = false;
  input.className = 'ex-input';
  setTimeout(() => input.focus(), 50);
  const fb = document.getElementById('ex-feedback');
  fb.className = 'ex-feedback';
  fb.textContent = '';
  document.getElementById('ex-action-btn').textContent = 'Проверить';
  exerciseChecked = false;
}

function normalizeAnswer(s) {
  return (s || '').trim().toLowerCase().replace(/[''ʼ]/g, "'").replace(/\s+/g, ' ');
}

function checkExerciseAnswer() {
  const t = currentGrammarTopic;
  const ex = t.exercises[exerciseIdx];
  const input = document.getElementById('ex-input');
  const userAns = normalizeAnswer(input.value);
  if (!userAns) return;
  const isCorrect = ex.answers.some(a => normalizeAnswer(a) === userAns);

  input.disabled = true;
  input.classList.add(isCorrect ? 'correct' : 'wrong');
  const fb = document.getElementById('ex-feedback');
  fb.classList.add('show', isCorrect ? 'correct' : 'wrong');
  fb.textContent = isCorrect
    ? '✓ Правильно!'
    : `✗ Правильный ответ: ${ex.answers[0]}`;
  document.getElementById('ex-translation').textContent = ex.translation;

  if (isCorrect) exerciseCorrect++;
  if (tg?.HapticFeedback) tg.HapticFeedback.notificationOccurred(isCorrect ? 'success' : 'error');
  document.getElementById('ex-action-btn').textContent =
    (exerciseIdx === t.exercises.length - 1) ? 'Завершить' : 'Следующее →';
  exerciseChecked = true;
}

function onExerciseAction() {
  if (!exerciseChecked) { checkExerciseAnswer(); return; }
  const t = currentGrammarTopic;
  if (exerciseIdx === t.exercises.length - 1) { finishGrammarExercises(); return; }
  exerciseIdx++;
  renderExercise();
}

function finishGrammarExercises() {
  const t = currentGrammarTopic;
  const total = t.exercises.length;
  const prev = grammarProgress[t.id] || { best: 0, total, attempts: 0 };
  grammarProgress[t.id] = {
    best:     Math.max(prev.best, exerciseCorrect),
    total:    total,
    attempts: prev.attempts + 1,
  };
  saveGrammarProgress();

  const isPerfect = exerciseCorrect === total;
  document.getElementById('gr-emoji').textContent = isPerfect ? '🏆' : (exerciseCorrect >= Math.ceil(total*0.6) ? '✅' : '💪');
  document.getElementById('gr-title').textContent = isPerfect ? 'Идеально!' : 'Хорошая работа!';
  document.getElementById('gr-score').textContent = `${exerciseCorrect} / ${total}`;
  setGrammarState('result');
}

document.addEventListener('keydown', e => {
  if (currentTab !== 'grammar') return;
  const exView = document.getElementById('grammar-exercise');
  if (exView && exView.style.display !== 'none' && e.key === 'Enter') {
    onExerciseAction();
  }
});
```

---

### Task 8 — Добавить грамматику в Stats-view

**Файл:** [d:\quizlet\index.html](../../../index.html), функция `loadStats` (строки 480–492) и `renderStats` (строки 494–537).

**В `loadStats`** — рядом с существующими `storage.get` добавить параллельный fetch `grammar_progress`. **Старая** функция:

```js
function loadStats() {
  const content = document.getElementById('stats-content');
  content.innerHTML = '<div style="text-align:center;color:var(--muted);padding:40px 0">⏳</div>';
  let loaded = 0;
  const results = {};
  const sets = Object.keys(SETS_META);
  sets.forEach(id => {
    storage.get(SETS_META[id].storageKey, val => {
      results[id] = val ? JSON.parse(val).length : 0;
      if (++loaded === sets.length) renderStats(results);
    });
  });
}
```

**Новая:**

```js
function loadStats() {
  const content = document.getElementById('stats-content');
  content.innerHTML = '<div style="text-align:center;color:var(--muted);padding:40px 0">⏳</div>';
  let loaded = 0;
  const results = {};
  const sets = Object.keys(SETS_META);
  const totalCalls = sets.length + 1;
  let grammarData = {};

  sets.forEach(id => {
    storage.get(SETS_META[id].storageKey, val => {
      results[id] = val ? JSON.parse(val).length : 0;
      if (++loaded === totalCalls) renderStats(results, grammarData);
    });
  });
  storage.get('grammar_progress', val => {
    grammarData = val ? JSON.parse(val) : {};
    if (++loaded === totalCalls) renderStats(results, grammarData);
  });
}
```

**В `renderStats`** — добавить блок грамматики **перед** закрывающей строкой `document.getElementById('stats-content').innerHTML = html;` (строка 536). Также изменить сигнатуру.

**Старое начало:**

```js
function renderStats(results) {
```

**Новое начало:**

```js
function renderStats(results, grammarData) {
```

**Перед** `document.getElementById('stats-content').innerHTML = html;` (строка 536) **вставить:**

```js
  // Grammar section
  const grammarTopics = window.GRAMMAR || [];
  if (grammarTopics.length) {
    const doneCount = grammarTopics.filter(t => {
      const p = grammarData[t.id];
      return p && p.best === t.exercises.length;
    }).length;
    const grPct = grammarTopics.length ? Math.round((doneCount / grammarTopics.length) * 100) : 0;
    const grBarColor = grPct === 100 ? 'var(--green)' : 'var(--accent)';
    html += `
      <div class="section-title">Грамматика</div>
      <div class="set-stat-card">
        <div class="set-stat-header">
          <span class="set-stat-icon">📚</span>
          <div class="set-stat-info">
            <div class="set-stat-name">Темы грамматики</div>
            <div class="set-stat-nums">${doneCount} / ${grammarTopics.length} тем пройдено</div>
          </div>
          <div class="set-stat-pct ${grPct===100?'done':''}">${grPct}%</div>
        </div>
        <div class="set-stat-bar-wrap">
          <div class="set-stat-bar-fill" style="width:${grPct}%;background:${grBarColor}"></div>
        </div>
      </div>`;
  }
```

---

### Task 9 — Smoke-тест в браузере

**Команды (PowerShell):**

```powershell
Start-Process "d:\quizlet\index.html"
```

**Что проверить вручную:**

1. Открывается главный экран с 3 папками наборов.
2. В нижней навигации **4** кнопки: 📁 / 🃏 / 📚 / 📊.
3. Нажатие 📚 «Грамматика» → виден заголовок «📚 Грамматика», секция «A1», карточка `Present Simple` с бейджем `A1` и текстом «6 упр.».
4. Тап по карточке темы → видно правило, таблица из 4 строк, 4 примера, кнопка «▶ Начать упражнения».
5. Нажать «‹ К списку тем» → возврат в список, кнопка работает.
6. Нажать «Начать упражнения» → виден прогресс `1 / 6`, предложение с пропуском, подсказка `(go)`, поле ввода в фокусе.
7. Ввести `goes` → «Проверить» → зелёная подсветка, фидбэк «✓ Правильно!», перевод снизу, кнопка стала «Следующее →».
8. Дойти до конца, специально один раз ошибиться → красная подсветка, показан правильный ответ.
9. На последнем упражнении → кнопка «Завершить» → экран результата с эмодзи, счётом `N / 6`, тремя кнопками.
10. Нажать «↺ Пройти заново» → начинаются упражнения сначала.
11. Перейти на 📊 Статистика → внизу секция «Грамматика: 0 или 1 / 1 тем пройдено» (зависит от прохождения).
12. Перезагрузить страницу — прогресс сохранился (для localStorage; в Telegram WebView — CloudStorage).
13. На вкладке упражнения нажать Enter — это должно срабатывать как «Проверить» / «Следующее».

**Если что-то сломано** — открыть DevTools Console (F12), искать ошибки, поправить, повторить тест. Не идти к коммиту, пока пункты 1–13 не пройдут.

---

### Task 10 — Коммит и пуш

**Команды (PowerShell):**

```powershell
git status
git add index.html data-grammar.js docs/superpowers/specs/2026-05-09-grammar-section-design.md docs/superpowers/plans/2026-05-09-grammar-mvp-plan.md
git commit -m @'
Add grammar section MVP with Present Simple

New 4th bottom-nav tab "Грамматика" with three states: topic list,
lesson (rule + forms table + examples), and 6 fill-in-the-blank
exercises with answer normalization and inline feedback. Progress
stored under grammar_progress key; topics shown in Stats view.
MVP ships only Present Simple to validate the UX before authoring
the remaining 17 topics.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
'@
git push
```

**После пуша:** перезапустить бота (чтобы `?v=...` обновился), проверить в Telegram → /start → «Открыть Flashcards».

---

## Quality gates self-check

- [x] **Spec coverage:** новая вкладка ✓, состояния `topics/lesson/exercise/result` ✓, нормализация ответов ✓, прогресс по ключу `grammar_progress` ✓, секция в Статистике ✓, MVP=1 тема ✓.
- [x] **Placeholder scan:** ни одного «TBD»/«appropriate»/«добавь обработку» — везде полный код.
- [x] **Type consistency:** `currentGrammarTopic` / `exerciseIdx` / `exerciseCorrect` / `grammarProgress` упоминаются согласованно во всех функциях; HTML-ID совпадают между шаблоном и JS.
- [x] **Each step executable:** для каждого изменения указан файл, точные старые/новые куски и место вставки; есть smoke-тест с 13 проверками; команды git готовы к копи-пасту.
