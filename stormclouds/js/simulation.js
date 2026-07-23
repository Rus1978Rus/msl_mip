/*
 * StormClouds — simulation engine.
 *
 * Clouds (each carrying a code fragment) drift on the "wind", collide,
 * exchange charge and drop their fragment into a "storm cell". Once the
 * cell's charge reaches a threshold, lightning strikes: the buffered
 * fragments are assembled and actually executed via StormLang.runProgram(),
 * and the result goes to the discharge log.
 *
 * Depends on js/interpreter.js (global StormLang) and the index.html markup.
 */
(function () {
  'use strict';

  /* ---- pool of fragments carried by clouds ---- */
  const POOL = [
    'x = 5', 'y = 3', 'n = 7', 'k = 2', 'bolt = 42', 'msg = "storm"',
    'x = x + 1', 'y = y * 2', 'n = n - 1', 'k = k * k', 'x = x % 4',
    'print(x)', 'print(y)', 'print(x + y)', 'print(x * y)', 'print(bolt)', 'print(msg)',
    'if x > 3: print("strike!")', 'if n > 5: print(n)',
    'for i in range(3): print(i)', 'for i in range(x): print(i)',
    'while k < 30: k = k + 7',
  ];
  const pick = (a) => a[Math.floor(Math.random() * a.length)];
  const rnd = (a, b) => a + Math.random() * (b - a);

  // "base" fragments — define a variable from a literal (no dependencies).
  // With coverage on, each is dealt to at least one starting cloud; otherwise
  // fragments that depend on a missing variable would fail forever.
  const BASE = ['x = 5', 'y = 3', 'n = 7', 'k = 2', 'bolt = 42', 'msg = "storm"'];
  const SEED_N = 9;
  const shuffle = (a) => {
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };

  /* ---- DOM references ---- */
  const sky = document.getElementById('sky');
  const canvas = document.getElementById('fx');
  const ctx = canvas.getContext('2d');
  const flashEl = document.getElementById('flash');
  const logEl = document.getElementById('log');
  const emptyEl = document.getElementById('empty');
  const toastsEl = document.getElementById('toasts');
  const bufEl = document.getElementById('buf');
  const cChargeEl = document.getElementById('cCharge');
  const skyvarsEl = document.getElementById('skyvars');
  const reduced = matchMedia('(prefers-reduced-motion:reduce)').matches;

  /* ---- parameters and state ---- */
  const CW = 132, CH = 88;         // cloud size
  const THRESH = 12, MAXBUF = 8;   // discharge threshold, max fragments in the cell
  let clouds = [], particles = [], bolt = null;
  let buffer = [], charge = 0, strikes = 0, okLines = 0;
  let running = true, speed = 1, gustUntil = 0;
  let memory = false, skyEnv = {};   // "sky memory": namespace shared across strikes
  let coverage = false;              // guaranteed coverage of base definitions
  let evolution = false, replacements = 0;   // selection: useful fragments outcompete useless ones
  const EVOLVE_EVERY = 2, MUT_RATE = 0.15;   // how often selection runs, mutation chance
  let W = 0, H = 0;
  const dpr = Math.min(devicePixelRatio || 1, 2);
  const lastPair = new Map();

  /* transient hint — "what did that click do" */
  function toast(msg, kind) {
    const t = document.createElement('div');
    t.className = 'toast' + (kind ? ' ' + kind : '');
    t.textContent = msg;
    toastsEl.appendChild(t);
    requestAnimationFrame(() => t.classList.add('show'));
    setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 320); }, 1700);
    while (toastsEl.children.length > 4) toastsEl.removeChild(toastsEl.firstChild);
  }

  /* live render of the storm cell */
  function renderBuf() {
    const near = charge >= THRESH * 0.75;
    cChargeEl.textContent = Math.round(charge) + ' / ' + THRESH;
    cChargeEl.classList.toggle('hot', near);
    if (buffer.length === 0) {
      bufEl.innerHTML = '<span class="c-empty">empty — waiting for clouds to collide</span>';
      return;
    }
    bufEl.innerHTML = '';
    buffer.forEach((b) => {
      const s = document.createElement('span');
      s.className = 'bchip';
      s.textContent = b.line;
      s.title = 'from ' + b.from;
      bufEl.appendChild(s);
    });
  }

  /* format a value Python-style */
  function fmtVal(v) {
    return v === true ? 'True' : v === false ? 'False' : (typeof v === 'string' ? '"' + v + '"' : String(v));
  }

  /* live namespace of the "sky memory" */
  function renderSkyVars() {
    if (!memory) { skyvarsEl.hidden = true; return; }
    skyvarsEl.hidden = false;
    const keys = Object.keys(skyEnv);
    let html = '<span class="sv-lbl">Sky memory</span>';
    if (keys.length === 0) html += '<span class="sv-empty">empty — no variable has survived a strike yet</span>';
    else html += keys.map((k) => '<span class="svar">' + esc(k + ' = ' + fmtVal(skyEnv[k])) + '</span>').join('');
    skyvarsEl.innerHTML = html;
  }

  function resize() {
    const r = sky.getBoundingClientRect();
    W = r.width; H = r.height;
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    clouds.forEach((c) => { c.x = Math.min(c.x, W - CW); c.y = Math.min(c.y, H - CH); });
  }

  function makeCloud(x, y, frag) {
    const el = document.createElement('div');
    el.className = 'cloud';
    el.innerHTML = '<div class="body"><div class="name"><span class="id"></span><span class="q">±0</span></div><span class="chip"></span></div>';
    const c = {
      el, x, y,
      vx: rnd(-0.5, 0.5) || 0.3, vy: rnd(-0.4, 0.4) || 0.2,
      charge: 0, fitScore: 0, fitCount: 0, frag: frag || pick(POOL),
      id: 'C' + (clouds.length + 1),
    };
    el.querySelector('.id').textContent = c.id;
    el.querySelector('.chip').textContent = c.frag;
    el.addEventListener('click', (e) => { e.stopPropagation(); reroll(c); });
    sky.appendChild(el);
    clouds.push(c);
    paintCloud(c);
    return c;
  }

  function reroll(c) {
    c.frag = pick(POOL);
    c.el.querySelector('.chip').textContent = c.frag;
    spark(c.x + CW / 2, c.y + CH / 2, '#8fb4ff', 8);
    toast(c.id + ' recoded -> ' + c.frag);
  }

  function paintCloud(c) {
    c.el.style.transform = 'translate(' + c.x + 'px,' + c.y + 'px)';
    const q = Math.round(c.charge);
    c.el.querySelector('.q').textContent = (q > 0 ? '+' : '') + q;
    c.el.classList.toggle('pos', c.charge > 0.5);
    c.el.classList.toggle('neg', c.charge < -0.5);
  }

  function seed() {
    clouds.forEach((c) => c.el.remove());
    clouds = [];
    let frags;
    if (coverage) {
      frags = BASE.slice();                                  // all base definitions
      while (frags.length < SEED_N) frags.push(pick(POOL));  // fill the rest at random
      shuffle(frags);
    } else {
      frags = Array.from({ length: SEED_N }, () => pick(POOL));
    }
    frags.forEach((f) => makeCloud(rnd(20, Math.max(40, W - CW - 20)), rnd(20, Math.max(40, H - CH - 20)), f));
  }

  /* ---- particles + lightning drawing ---- */
  function spark(x, y, color, count) {
    count = count || 14;
    for (let i = 0; i < count; i++) {
      const a = Math.random() * Math.PI * 2, sp = rnd(0.6, 3);
      particles.push({ x, y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: 1, color: color || '#ffe07a' });
    }
  }

  function makeBolt(x1, y1, x2, y2, disp) {
    let pts = [{ x: x1, y: y1 }, { x: x2, y: y2 }];
    for (let it = 0; it < 5; it++) {
      const np = [];
      for (let i = 0; i < pts.length - 1; i++) {
        const a = pts[i], b = pts[i + 1];
        const mx = (a.x + b.x) / 2 + rnd(-disp, disp);
        const my = (a.y + b.y) / 2 + rnd(-disp, disp);
        np.push(a, { x: mx, y: my });
      }
      np.push(pts[pts.length - 1]);
      pts = np; disp *= 0.55;
    }
    const branches = [];
    for (let i = 3; i < pts.length - 2; i += 4) {
      if (Math.random() < 0.4) {
        const p = pts[i];
        branches.push([{ x: p.x, y: p.y }, { x: p.x + rnd(-60, 60), y: p.y + rnd(20, 70) }]);
      }
    }
    return { pts, branches, life: 1 };
  }

  function strikeAt(x, y) {
    bolt = makeBolt(x, -10, x, y, 42);
    const maxF = reduced ? 0.14 : 0.9;
    flashEl.style.transition = 'none';
    flashEl.style.opacity = maxF;
    requestAnimationFrame(() => { flashEl.style.transition = 'opacity .55s ease'; flashEl.style.opacity = 0; });
    spark(x, y, '#fff7d6', reduced ? 10 : 34);
  }

  function drawBolt() {
    if (!bolt) return;
    const draw = (pts, w, col, alpha) => {
      ctx.beginPath();
      ctx.moveTo(pts[0].x, pts[0].y);
      for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i].x, pts[i].y);
      ctx.lineWidth = w; ctx.strokeStyle = col; ctx.globalAlpha = alpha * bolt.life;
      ctx.lineJoin = 'round'; ctx.lineCap = 'round';
      ctx.shadowBlur = 22; ctx.shadowColor = '#ffd23f';
      ctx.stroke();
    };
    draw(bolt.pts, 6, 'rgba(255,210,63,.55)', 1);
    bolt.branches.forEach((b) => draw(b, 2.5, 'rgba(255,210,63,.5)', 1));
    draw(bolt.pts, 2, '#fff7d6', 1);
    ctx.globalAlpha = 1; ctx.shadowBlur = 0;
    bolt.life -= 0.045;
    if (bolt.life <= 0) bolt = null;
  }

  /* ---- discharge log ---- */
  function esc(s) { return s.replace(/[&<>]/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[m])); }

  function logStrike(entries, res) {
    if (emptyEl) emptyEl.style.display = 'none';
    const el = document.createElement('div');
    el.className = 'strike';
    const okc = res.trace.filter((t) => t.ok).length;
    const n = entries.length;
    let html = '<div class="st-head"><span>⚡ Strike #' + strikes + '</span><span class="meta">' + n + ' frags · ' + okc + '/' + n + ' ok</span></div>';
    html += '<div class="code">';
    res.trace.forEach((t, i) => {
      const g = String(i + 1).padStart(2, '0');
      const who = entries[i] ? esc(entries[i].from) : '';
      let row = '<div class="' + (t.ok ? 'ln' : 'ln err') + '"><span class="g">' + g + '</span><span class="who">' + who + '</span><span class="src">' + esc(t.line) + '</span>';
      if (!t.ok) row += '<span class="note"># ' + esc(t.err) + '</span>';
      html += row + '</div>';
    });
    html += '</div>';
    if (res.out.length) {
      html += '<div class="out"><span class="lbl">output</span>' + esc(res.out.join('\n')) + '</div>';
    }
    el.innerHTML = html;
    logEl.appendChild(el);
    while (logEl.children.length > 26) {
      logEl.removeChild(logEl.firstElementChild === emptyEl ? logEl.children[1] : logEl.firstElementChild);
    }
    logEl.scrollTop = logEl.scrollHeight;
  }

  /* ---- discharge ---- */
  function pushBuf(line, from) {
    const last = buffer[buffer.length - 1];
    if (!last || last.line !== line) buffer.push({ line, from });
  }

  function triggerStrike(x, y) {
    if (buffer.length === 0) {
      strikeAt(x || W / 2, y || H / 2);
      toast('⚡ empty discharge — the storm cell is empty', 'zap');
      return;
    }
    const entries = buffer.slice();
    buffer = []; charge = 0;
    const lines = entries.map((e) => e.line);
    // sky memory: the same namespace across strikes -> the program grows
    const res = StormLang.runProgram(lines, memory ? skyEnv : {});
    strikes++;
    okLines += res.trace.filter((t) => t.ok).length;
    strikeAt(x || W / 2, y || H * 0.55);
    logStrike(entries, res);
    const okc = res.trace.filter((t) => t.ok).length;
    const printed = res.out.length;
    toast('⚡ strike #' + strikes + ' · ' + okc + '/' + entries.length + ' ok' + (printed ? ' · output ↓' : ''), 'zap');
    clouds.forEach((c) => { c.charge *= 0.3; paintCloud(c); });
    renderBuf();
    renderSkyVars();
    if (evolution) evolveStep(res);
    updateTelemetry();
  }

  /* Selection: after each strike, update fragment "fitness". We use the AVERAGE
     reward per appearance (fitScore/fitCount), not the sum — otherwise fitness
     couples to frequency and often-colliding assignments beat rare but useful
     prints. Printing is worth more than a bare success (+2 for output, +1 for
     success, -1 for an error). Every EVOLVE_EVERY strikes the worst participating
     cloud is replaced by an offspring of the best (with a mutation chance), so
     useful fragments outcompete useless ones. */
  const fit = (c) => (c.fitCount ? c.fitScore / c.fitCount : 0);

  function evolveStep(res) {
    clouds.forEach((c) => {
      const mine = res.trace.filter((t) => t.line === c.frag);
      if (!mine.length) return;
      const printed = mine.some((t) => t.ok && t.produced && t.produced.length);
      const okAny = mine.some((t) => t.ok);
      c.fitScore += printed ? 2 : (okAny ? 1 : -1);
      c.fitCount += 1;
    });
    if (strikes % EVOLVE_EVERY === 0) evolve();
  }

  function evolve() {
    const rated = clouds.filter((c) => c.fitCount > 0); // only clouds that actually took part
    if (rated.length < 2) return;
    let best = rated[0], worst = rated[0];
    for (const c of rated) {
      if (fit(c) > fit(best)) best = c;
      if (fit(c) < fit(worst)) worst = c;
    }
    if (best === worst || fit(best) <= fit(worst)) return; // nothing to learn from
    const before = worst.frag;
    const mutated = Math.random() < MUT_RATE;
    worst.frag = mutated ? pick(POOL) : best.frag; // offspring of the best, or a mutation
    worst.fitScore = 0; worst.fitCount = 0;
    worst.el.querySelector('.chip').textContent = worst.frag;
    spark(worst.x + CW / 2, worst.y + CH / 2, mutated ? '#c88bff' : '#7ee0a6', 12);
    replacements++;
    toast('🧬 ' + worst.id + ': ' + before + ' -> ' + worst.frag + (mutated ? ' (mutation)' : ' (offspring of ' + best.id + ')'));
  }

  /* ---- telemetry ---- */
  const T = {
    c: document.getElementById('tClouds'),
    ch: document.getElementById('tCharge'),
    st: document.getElementById('tStrikes'),
    ln: document.getElementById('tLines'),
    evo: document.getElementById('tEvo'),
    f: document.getElementById('tFill'),
  };
  function updateTelemetry() {
    T.c.textContent = clouds.length;
    T.ch.textContent = Math.round(charge);
    T.st.textContent = strikes;
    T.ln.textContent = okLines;
    T.evo.textContent = replacements;
    const pct = Math.min(1, charge / THRESH);
    T.f.style.right = (100 - pct * 100) + '%';
  }

  /* ---- main loop ---- */
  let last = performance.now();
  function loop(now) {
    const dt = Math.min(50, now - last) / 16.67;
    last = now;
    ctx.clearRect(0, 0, W, H);

    const boost = now < gustUntil ? 1.8 : 1;
    if (running) {
      // motion (wind)
      for (const c of clouds) {
        c.x += c.vx * speed * boost * dt;
        c.y += c.vy * speed * boost * dt * 0.8;
        if (c.x < 0) { c.x = 0; c.vx = Math.abs(c.vx); }
        if (c.x > W - CW) { c.x = W - CW; c.vx = -Math.abs(c.vx); }
        if (c.y < 0) { c.y = 0; c.vy = Math.abs(c.vy); }
        if (c.y > H - CH) { c.y = H - CH; c.vy = -Math.abs(c.vy); }
        c.vx += rnd(-0.03, 0.03); c.vy += rnd(-0.03, 0.03);
        c.vx = Math.max(-1.3, Math.min(1.3, c.vx));
        c.vy = Math.max(-1.1, Math.min(1.1, c.vy));
        paintCloud(c);
      }
      // collisions
      for (let i = 0; i < clouds.length; i++) {
        for (let j = i + 1; j < clouds.length; j++) {
          const a = clouds[i], b = clouds[j];
          const dx = a.x - b.x, dy = a.y - b.y;
          const d = Math.hypot(dx, dy);
          if (d < CW * 0.62) {
            const key = a.id + '|' + b.id, t0 = lastPair.get(key) || 0;
            // push apart so they don't clump
            const nx = dx / (d || 1), ny = dy / (d || 1);
            a.vx += nx * 0.04; a.vy += ny * 0.04;
            b.vx -= nx * 0.04; b.vy -= ny * 0.04;
            if (now - t0 > 650) {
              lastPair.set(key, now);
              const delta = pick([-2, -1, 1, 2]);
              a.charge += delta; b.charge -= delta;
              charge += Math.abs(delta);
              const mx = (a.x + b.x) / 2 + CW / 2, my = (a.y + b.y) / 2 + CH / 2;
              spark(mx, my, delta > 0 ? '#ffca4a' : '#57c9e6');
              pushBuf(a.frag, a.id); pushBuf(b.frag, b.id);
              paintCloud(a); paintCloud(b);
              renderBuf();
              if (charge >= THRESH || buffer.length >= MAXBUF) triggerStrike(mx, my);
              updateTelemetry();
            }
          }
        }
      }
    }

    // particles
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx; p.y += p.vy; p.vy += 0.04; p.life -= 0.03;
      if (p.life <= 0) { particles.splice(i, 1); continue; }
      ctx.globalAlpha = p.life; ctx.fillStyle = p.color;
      ctx.shadowBlur = 8; ctx.shadowColor = p.color;
      ctx.beginPath(); ctx.arc(p.x, p.y, 2.1 * p.life + 0.6, 0, Math.PI * 2); ctx.fill();
    }
    ctx.globalAlpha = 1; ctx.shadowBlur = 0;

    drawBolt();
    requestAnimationFrame(loop);
  }

  /* ---- controls ---- */
  document.getElementById('btnRun').addEventListener('click', (e) => {
    running = !running;
    e.currentTarget.textContent = running ? '⏸ Pause' : '▶ Play';
    e.currentTarget.classList.toggle('primary', !running);
  });
  document.getElementById('btnGust').addEventListener('click', () => {
    gustUntil = performance.now() + 1100;
    clouds.forEach((c) => { c.vx = rnd(-1.2, 1.2); c.vy = rnd(-1, 1); });
    toast('🌬 gust — clouds scattered');
  });
  document.getElementById('btnAdd').addEventListener('click', () => {
    const c = makeCloud(rnd(20, Math.max(40, W - CW - 20)), rnd(20, Math.max(40, H - CH - 20)));
    toast('＋ ' + c.id + ' in the sky · carries ' + c.frag);
    updateTelemetry();
  });
  document.getElementById('btnStrike').addEventListener('click', () => triggerStrike(W / 2, H * 0.5));
  document.getElementById('btnMem').addEventListener('click', (e) => {
    memory = !memory;
    skyEnv = {}; // start accumulation from a clean slate on toggle
    e.currentTarget.textContent = memory ? '🧠 Memory: on' : '🧠 Memory: off';
    e.currentTarget.classList.toggle('primary', memory);
    renderSkyVars();
    toast(memory ? '🧠 sky memory on — namespace persists across strikes' : '🧠 sky memory off — each strike starts fresh');
  });
  document.getElementById('btnCov').addEventListener('click', (e) => {
    coverage = !coverage;
    e.currentTarget.textContent = coverage ? '🎯 Coverage: on' : '🎯 Coverage: off';
    e.currentTarget.classList.toggle('primary', coverage);
    // re-seed the sky by the new rule; restart accumulation
    buffer = []; charge = 0; skyEnv = {}; particles = []; bolt = null; lastPair.clear();
    seed(); renderBuf(); renderSkyVars(); updateTelemetry();
    toast(coverage ? '🎯 coverage on — base definitions guaranteed' : '🎲 coverage off — fragments are random');
  });
  document.getElementById('btnEvo').addEventListener('click', (e) => {
    evolution = !evolution;
    e.currentTarget.textContent = evolution ? '🧬 Evolution: on' : '🧬 Evolution: off';
    e.currentTarget.classList.toggle('primary', evolution);
    clouds.forEach((c) => { c.fitScore = 0; c.fitCount = 0; });
    toast(evolution ? '🧬 evolution on — useful fragments outcompete useless ones' : '🧬 evolution off');
  });
  document.getElementById('btnReset').addEventListener('click', () => {
    buffer = []; charge = 0; strikes = 0; okLines = 0; particles = []; bolt = null; lastPair.clear();
    skyEnv = {}; replacements = 0;
    logEl.innerHTML = ''; logEl.appendChild(emptyEl); emptyEl.style.display = '';
    seed(); renderBuf(); renderSkyVars(); updateTelemetry();
    toast('↺ sky reset');
  });
  document.getElementById('spd').addEventListener('input', (e) => { speed = parseFloat(e.target.value); });
  sky.addEventListener('click', (e) => {
    const r = sky.getBoundingClientRect();
    const c = makeCloud(e.clientX - r.left - CW / 2, e.clientY - r.top - CH / 2);
    toast('＋ ' + c.id + ' in the sky · carries ' + c.frag);
    updateTelemetry();
  });

  /* ---- start ---- */
  new ResizeObserver(resize).observe(sky);
  requestAnimationFrame(() => {
    resize(); seed(); renderBuf(); renderSkyVars(); updateTelemetry();
    requestAnimationFrame(loop);
  });
})();
