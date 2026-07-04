const state = {
  shootType: 'couple',
  tab: 'plan',
  categoryFilter: 'all',
  lastPoseId: null,
  planMinutes: 30,
  plan: null,
};

const STORAGE_KEY = 'posing-guide-checklist';

function loadChecklist() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  } catch {
    return {};
  }
}

function saveChecklist(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

let checklist = loadChecklist();

function posesFor(shootType, category) {
  return POSES.filter(p => p.shootType === shootType && (category === 'all' || p.category === category));
}

function categoriesFor(shootType) {
  const cats = [...new Set(POSES.filter(p => p.shootType === shootType).map(p => p.category))];
  return cats;
}

function randomPose(shootType, category, excludeId) {
  let pool = posesFor(shootType, category);
  if (pool.length > 1 && excludeId) {
    pool = pool.filter(p => p.id !== excludeId);
  }
  return pool[Math.floor(Math.random() * pool.length)];
}

function buildPlan(shootType, totalMinutes) {
  const phases = PHASE_PLANS[shootType];
  let elapsed = 0;
  return phases.map(phase => {
    const duration = Math.max(1, Math.round(phase.fraction * totalMinutes));
    const start = elapsed;
    elapsed += duration;
    const pool = POSES.filter(p => p.shootType === shootType && phase.categories.includes(p.category));
    const shuffled = [...pool].sort(() => Math.random() - 0.5);
    const picks = shuffled.slice(0, Math.min(3, shuffled.length));
    return { name: phase.name, start, end: elapsed, poses: picks };
  });
}

function fmtMin(m) {
  return `${m} Min`;
}

function poseImg(pose) {
  return `illustrations/${pose.id}.png`;
}

function render() {
  document.querySelectorAll('.shoot-tab').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.shoot === state.shootType);
  });
  document.querySelectorAll('.nav-tab').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === state.tab);
  });

  const main = document.getElementById('main');
  main.innerHTML = '';

  if (state.tab === 'plan') renderPlan(main);
  else if (state.tab === 'random') renderRandom(main);
  else if (state.tab === 'categories') renderCategories(main);
  else if (state.tab === 'checklist') renderChecklist(main);
}

function renderPlan(main) {
  if (!state.plan) state.plan = buildPlan(state.shootType, state.planMinutes);

  const controls = document.createElement('div');
  controls.className = 'plan-controls';
  controls.innerHTML = `
    <label for="minutes-input">Dauer des Shootings</label>
    <div class="minutes-row">
      <input type="number" id="minutes-input" min="5" max="180" step="5" value="${state.planMinutes}">
      <span>Minuten</span>
      <button id="regen-plan" class="btn-secondary">Neu mischen</button>
    </div>
  `;
  main.appendChild(controls);

  controls.querySelector('#minutes-input').addEventListener('change', (e) => {
    const v = parseInt(e.target.value, 10);
    state.planMinutes = isNaN(v) || v < 5 ? 30 : v;
    state.plan = buildPlan(state.shootType, state.planMinutes);
    render();
  });
  controls.querySelector('#regen-plan').addEventListener('click', () => {
    state.plan = buildPlan(state.shootType, state.planMinutes);
    render();
  });

  const timeline = document.createElement('div');
  timeline.className = 'timeline';
  state.plan.forEach(phase => {
    const block = document.createElement('div');
    block.className = 'phase-block';
    block.innerHTML = `
      <div class="phase-header">
        <span class="phase-time">${fmtMin(phase.start)}–${fmtMin(phase.end)}</span>
        <span class="phase-name">${phase.name}</span>
      </div>
      <div class="phase-poses">
        ${phase.poses.map(p => `
          <div class="phase-pose">
            <img src="${poseImg(p)}" alt="" loading="lazy" onerror="this.style.display='none'">
            <div><strong>${p.title}</strong> — ${p.instruction}</div>
          </div>
        `).join('')}
      </div>
    `;
    timeline.appendChild(block);
  });
  main.appendChild(timeline);
}

function renderRandom(main) {
  const cats = categoriesFor(state.shootType);

  const filterRow = document.createElement('div');
  filterRow.className = 'chip-row';
  filterRow.innerHTML = `<button class="chip ${state.categoryFilter === 'all' ? 'active' : ''}" data-cat="all">Alle</button>` +
    cats.map(c => `<button class="chip ${state.categoryFilter === c ? 'active' : ''}" data-cat="${c}">${CATEGORY_LABELS[c]}</button>`).join('');
  main.appendChild(filterRow);

  filterRow.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      state.categoryFilter = chip.dataset.cat;
      state.lastPoseId = null;
      render();
    });
  });

  const card = document.createElement('div');
  card.className = 'pose-card';
  const pose = randomPose(state.shootType, state.categoryFilter, state.lastPoseId);
  if (pose) {
    card.innerHTML = `
      <img class="pose-illustration" src="${poseImg(pose)}" alt="" loading="lazy" onerror="this.style.display='none'">
      <div class="pose-category">${CATEGORY_LABELS[pose.category]}</div>
      <h2>${pose.title}</h2>
      <p class="pose-instruction">${pose.instruction}</p>
      ${pose.tip ? `<p class="pose-tip">💡 ${pose.tip}</p>` : ''}
    `;
    state.lastPoseId = pose.id;
  } else {
    card.innerHTML = '<p>Keine Posen in dieser Kategorie.</p>';
  }
  main.appendChild(card);

  const btn = document.createElement('button');
  btn.className = 'btn-primary btn-big';
  btn.textContent = 'Neue Pose';
  btn.addEventListener('click', render);
  main.appendChild(btn);
}

function renderCategories(main) {
  const cats = categoriesFor(state.shootType);
  cats.forEach(cat => {
    const section = document.createElement('div');
    section.className = 'category-section';
    const poses = posesFor(state.shootType, cat);
    section.innerHTML = `
      <h3>${CATEGORY_LABELS[cat]}</h3>
      <div class="pose-list">
        ${poses.map(p => `
          <details class="pose-item">
            <summary>${p.title}</summary>
            <img class="pose-illustration" src="${poseImg(p)}" alt="" loading="lazy" onerror="this.style.display='none'">
            <p class="pose-instruction">${p.instruction}</p>
            ${p.tip ? `<p class="pose-tip">💡 ${p.tip}</p>` : ''}
          </details>
        `).join('')}
      </div>
    `;
    main.appendChild(section);
  });
}

function renderChecklist(main) {
  const key = state.shootType;
  if (!checklist[key]) checklist[key] = {};

  const resetBtn = document.createElement('button');
  resetBtn.className = 'btn-secondary';
  resetBtn.textContent = 'Neues Shooting (Haken zurücksetzen)';
  resetBtn.addEventListener('click', () => {
    checklist[key] = {};
    saveChecklist(checklist);
    render();
  });
  main.appendChild(resetBtn);

  const cats = categoriesFor(state.shootType);
  cats.forEach(cat => {
    const section = document.createElement('div');
    section.className = 'category-section';
    const poses = posesFor(state.shootType, cat);
    section.innerHTML = `
      <h3>${CATEGORY_LABELS[cat]}</h3>
      <div class="check-list">
        ${poses.map(p => `
          <label class="check-item">
            <input type="checkbox" data-id="${p.id}" ${checklist[key][p.id] ? 'checked' : ''}>
            <span>${p.title}</span>
          </label>
        `).join('')}
      </div>
    `;
    main.appendChild(section);
  });

  main.querySelectorAll('input[type="checkbox"]').forEach(cb => {
    cb.addEventListener('change', () => {
      checklist[key][cb.dataset.id] = cb.checked;
      saveChecklist(checklist);
    });
  });
}

document.querySelectorAll('.shoot-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    state.shootType = btn.dataset.shoot;
    state.categoryFilter = 'all';
    state.lastPoseId = null;
    state.plan = null;
    render();
  });
});

document.querySelectorAll('.nav-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    state.tab = btn.dataset.tab;
    render();
  });
});

render();
