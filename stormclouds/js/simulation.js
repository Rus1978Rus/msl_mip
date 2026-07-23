/*
 * StormClouds — движок симуляции.
 *
 * Тучи (каждая несёт фрагмент кода) дрейфуют от «ветра», сталкиваются,
 * обмениваются зарядом и сбрасывают свой фрагмент в «грозовой очаг».
 * Когда заряд очага достигает порога — молния: очаг исполняется
 * через StormLang.runProgram(), результат уходит в журнал.
 *
 * Зависит от js/interpreter.js (глобальный StormLang) и разметки index.html.
 */
(function () {
  'use strict';

  /* ---- пул фрагментов, что носят тучи ---- */
  const POOL = [
    'x = 5', 'y = 3', 'n = 7', 'k = 2', 'bolt = 42', 'msg = "storm"',
    'x = x + 1', 'y = y * 2', 'n = n - 1', 'k = k * k', 'x = x % 4',
    'print(x)', 'print(y)', 'print(x + y)', 'print(x * y)', 'print(bolt)', 'print(msg)',
    'if x > 3: print("удар!")', 'if n > 5: print(n)',
    'for i in range(3): print(i)', 'for i in range(x): print(i)',
    'while k < 30: k = k + 7',
  ];
  const pick = (a) => a[Math.floor(Math.random() * a.length)];
  const rnd = (a, b) => a + Math.random() * (b - a);

  /* ---- ссылки на DOM ---- */
  const sky = document.getElementById('sky');
  const canvas = document.getElementById('fx');
  const ctx = canvas.getContext('2d');
  const flashEl = document.getElementById('flash');
  const logEl = document.getElementById('log');
  const emptyEl = document.getElementById('empty');
  const toastsEl = document.getElementById('toasts');
  const bufEl = document.getElementById('buf');
  const cChargeEl = document.getElementById('cCharge');
  const reduced = matchMedia('(prefers-reduced-motion:reduce)').matches;

  /* ---- параметры и состояние ---- */
  const CW = 132, CH = 88;         // размер тучи
  const THRESH = 12, MAXBUF = 8;   // порог разряда, макс. фрагментов в очаге
  let clouds = [], particles = [], bolt = null;
  let buffer = [], charge = 0, strikes = 0, okLines = 0;
  let running = true, speed = 1, gustUntil = 0;
  let W = 0, H = 0;
  const dpr = Math.min(devicePixelRatio || 1, 2);
  const lastPair = new Map();

  /* всплывающая подсказка — «что вышло из клика» */
  function toast(msg, kind) {
    const t = document.createElement('div');
    t.className = 'toast' + (kind ? ' ' + kind : '');
    t.textContent = msg;
    toastsEl.appendChild(t);
    requestAnimationFrame(() => t.classList.add('show'));
    setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 320); }, 1700);
    while (toastsEl.children.length > 4) toastsEl.removeChild(toastsEl.firstChild);
  }

  /* живой рендер грозового очага */
  function renderBuf() {
    const near = charge >= THRESH * 0.75;
    cChargeEl.textContent = Math.round(charge) + ' / ' + THRESH;
    cChargeEl.classList.toggle('hot', near);
    if (buffer.length === 0) {
      bufEl.innerHTML = '<span class="c-empty">пусто — ждём столкновений туч</span>';
      return;
    }
    bufEl.innerHTML = '';
    buffer.forEach((line) => {
      const s = document.createElement('span');
      s.className = 'bchip';
      s.textContent = line;
      bufEl.appendChild(s);
    });
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
      charge: 0, frag: frag || pick(POOL),
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
    toast(c.id + ' сменил код → ' + c.frag);
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
    for (let i = 0; i < 6; i++) {
      makeCloud(rnd(20, Math.max(40, W - CW - 20)), rnd(20, Math.max(40, H - CH - 20)));
    }
  }

  /* ---- частицы + отрисовка молнии ---- */
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

  /* ---- журнал разрядов ---- */
  function esc(s) { return s.replace(/[&<>]/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[m])); }

  function logStrike(lines, res) {
    if (emptyEl) emptyEl.style.display = 'none';
    const el = document.createElement('div');
    el.className = 'strike';
    const okc = res.trace.filter((t) => t.ok).length;
    let html = '<div class="st-head"><span>⚡ Разряд #' + strikes + '</span><span class="meta">' + lines.length + ' фрагм. · ' + okc + '/' + lines.length + ' ok</span></div>';
    html += '<div class="code">';
    res.trace.forEach((t, i) => {
      const g = String(i + 1).padStart(2, '0');
      if (t.ok) html += '<div class="ln"><span class="g">' + g + '</span><span class="src">' + esc(t.line) + '</span></div>';
      else html += '<div class="ln err"><span class="g">' + g + '</span><span class="src">' + esc(t.line) + '</span><span class="note"># ' + esc(t.err) + '</span></div>';
    });
    html += '</div>';
    if (res.out.length) {
      html += '<div class="out"><span class="lbl">вывод</span>' + esc(res.out.join('\n')) + '</div>';
    }
    el.innerHTML = html;
    logEl.appendChild(el);
    while (logEl.children.length > 26) {
      logEl.removeChild(logEl.firstElementChild === emptyEl ? logEl.children[1] : logEl.firstElementChild);
    }
    logEl.scrollTop = logEl.scrollHeight;
  }

  /* ---- разряд ---- */
  function pushBuf(line) { if (buffer[buffer.length - 1] !== line) buffer.push(line); }

  function triggerStrike(x, y) {
    if (buffer.length === 0) {
      strikeAt(x || W / 2, y || H / 2);
      toast('⚡ разряд вхолостую — очаг пуст', 'zap');
      return;
    }
    const lines = buffer.slice();
    buffer = []; charge = 0;
    const res = StormLang.runProgram(lines);
    strikes++;
    okLines += res.trace.filter((t) => t.ok).length;
    strikeAt(x || W / 2, y || H * 0.55);
    logStrike(lines, res);
    const okc = res.trace.filter((t) => t.ok).length;
    const printed = res.out.length;
    toast('⚡ разряд #' + strikes + ' · ' + okc + '/' + lines.length + ' ok' + (printed ? ' · вывод ↓' : ''), 'zap');
    clouds.forEach((c) => { c.charge *= 0.3; paintCloud(c); });
    renderBuf();
    updateTelemetry();
  }

  /* ---- телеметрия ---- */
  const T = {
    c: document.getElementById('tClouds'),
    ch: document.getElementById('tCharge'),
    st: document.getElementById('tStrikes'),
    ln: document.getElementById('tLines'),
    f: document.getElementById('tFill'),
  };
  function updateTelemetry() {
    T.c.textContent = clouds.length;
    T.ch.textContent = Math.round(charge);
    T.st.textContent = strikes;
    T.ln.textContent = okLines;
    const pct = Math.min(1, charge / THRESH);
    T.f.style.right = (100 - pct * 100) + '%';
  }

  /* ---- главный цикл ---- */
  let last = performance.now();
  function loop(now) {
    const dt = Math.min(50, now - last) / 16.67;
    last = now;
    ctx.clearRect(0, 0, W, H);

    const boost = now < gustUntil ? 1.8 : 1;
    if (running) {
      // движение (ветер)
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
      // столкновения
      for (let i = 0; i < clouds.length; i++) {
        for (let j = i + 1; j < clouds.length; j++) {
          const a = clouds[i], b = clouds[j];
          const dx = a.x - b.x, dy = a.y - b.y;
          const d = Math.hypot(dx, dy);
          if (d < CW * 0.62) {
            const key = a.id + '|' + b.id, t0 = lastPair.get(key) || 0;
            // расталкивание, чтобы не слипались
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
              pushBuf(a.frag); pushBuf(b.frag);
              paintCloud(a); paintCloud(b);
              renderBuf();
              if (charge >= THRESH || buffer.length >= MAXBUF) triggerStrike(mx, my);
              updateTelemetry();
            }
          }
        }
      }
    }

    // частицы
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

  /* ---- управление ---- */
  document.getElementById('btnRun').addEventListener('click', (e) => {
    running = !running;
    e.currentTarget.textContent = running ? '⏸ Пауза' : '▶ Пуск';
    e.currentTarget.classList.toggle('primary', !running);
  });
  document.getElementById('btnGust').addEventListener('click', () => {
    gustUntil = performance.now() + 1100;
    clouds.forEach((c) => { c.vx = rnd(-1.2, 1.2); c.vy = rnd(-1, 1); });
    toast('🌬 порыв ветра — тучи разлетелись');
  });
  document.getElementById('btnAdd').addEventListener('click', () => {
    const c = makeCloud(rnd(20, Math.max(40, W - CW - 20)), rnd(20, Math.max(40, H - CH - 20)));
    toast('＋ ' + c.id + ' в небе · несёт ' + c.frag);
    updateTelemetry();
  });
  document.getElementById('btnStrike').addEventListener('click', () => triggerStrike(W / 2, H * 0.5));
  document.getElementById('btnReset').addEventListener('click', () => {
    buffer = []; charge = 0; strikes = 0; okLines = 0; particles = []; bolt = null; lastPair.clear();
    logEl.innerHTML = ''; logEl.appendChild(emptyEl); emptyEl.style.display = '';
    seed(); renderBuf(); updateTelemetry();
    toast('↺ небо сброшено');
  });
  document.getElementById('spd').addEventListener('input', (e) => { speed = parseFloat(e.target.value); });
  sky.addEventListener('click', (e) => {
    const r = sky.getBoundingClientRect();
    const c = makeCloud(e.clientX - r.left - CW / 2, e.clientY - r.top - CH / 2);
    toast('＋ ' + c.id + ' в небе · несёт ' + c.frag);
    updateTelemetry();
  });

  /* ---- старт ---- */
  new ResizeObserver(resize).observe(sky);
  requestAnimationFrame(() => {
    resize(); seed(); renderBuf(); updateTelemetry();
    requestAnimationFrame(loop);
  });
})();
