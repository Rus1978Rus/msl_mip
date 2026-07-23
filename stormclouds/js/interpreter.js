/*
 * StormClouds — a tiny interpreter for a subset of Python.
 *
 * A pure, DOM-free module: tokenizer -> parser -> evaluator.
 * Each line (a "fragment" carried by a cloud) is one self-contained
 * expression or statement. runProgram() runs a list of lines REPL-style in a
 * shared namespace and returns the output plus a per-line trace.
 *
 *   StormLang.runProgram(['x = 5', 'print(x + 1)'])
 *     -> { out: ['6'], trace: [...], env: { x: 5 } }
 *
 * Supported: assignment, arithmetic (+ - * / %), comparisons, strings,
 * print(...), single-line if / while / for i in range(...).
 */
(function (global) {
  'use strict';

  const KW = ['if', 'for', 'in', 'while', 'print', 'range', 'True', 'False'];

  // --- tokenizer ------------------------------------------------------------
  function tokenize(src) {
    const toks = [];
    let i = 0;
    const isD = (c) => c >= '0' && c <= '9';
    const isA = (c) => /[A-Za-z_]/.test(c);
    while (i < src.length) {
      const c = src[i];
      if (c === ' ' || c === '\t') { i++; continue; }
      if (isD(c)) {
        let j = i;
        while (j < src.length && isD(src[j])) j++;
        toks.push({ t: 'num', v: parseInt(src.slice(i, j), 10) });
        i = j; continue;
      }
      if (c === '"' || c === "'") {
        let j = i + 1;
        while (j < src.length && src[j] !== c) j++;
        if (j >= src.length) throw new Error('unterminated string literal');
        toks.push({ t: 'str', v: src.slice(i + 1, j) });
        i = j + 1; continue;
      }
      if (isA(c)) {
        let j = i;
        while (j < src.length && /[A-Za-z0-9_]/.test(src[j])) j++;
        const w = src.slice(i, j);
        toks.push({ t: KW.includes(w) ? 'kw' : 'name', v: w });
        i = j; continue;
      }
      const two = src.slice(i, i + 2);
      if (['==', '!=', '>=', '<='].includes(two)) { toks.push({ t: 'op', v: two }); i += 2; continue; }
      if ('()+-*/%<>=:,'.includes(c)) { toks.push({ t: 'op', v: c }); i++; continue; }
      throw new Error("unexpected character '" + c + "'");
    }
    return toks;
  }

  // --- parser (recursive descent) -------------------------------------------
  function parse(line) {
    const toks = tokenize(line);
    let pos = 0;
    const peek = () => toks[pos];
    const next = () => toks[pos++];
    const eatOp = (v) => { const t = next(); if (!t || t.t !== 'op' || t.v !== v) throw new Error("expected '" + v + "'"); };
    const eatKw = (v) => { const t = next(); if (!t || t.t !== 'kw' || t.v !== v) throw new Error("expected '" + v + "'"); };
    const isOp = (t, set) => t && t.t === 'op' && set.includes(t.v);

    const expr = () => cmp();
    function cmp() { let l = add(); while (isOp(peek(), ['<', '>', '<=', '>=', '==', '!='])) { const op = next().v; l = { type: 'bin', op, l, r: add() }; } return l; }
    function add() { let l = mul(); while (isOp(peek(), ['+', '-'])) { const op = next().v; l = { type: 'bin', op, l, r: mul() }; } return l; }
    function mul() { let l = un(); while (isOp(peek(), ['*', '/', '%'])) { const op = next().v; l = { type: 'bin', op, l, r: un() }; } return l; }
    function un() { if (isOp(peek(), ['-'])) { next(); return { type: 'un', e: un() }; } return prim(); }
    function prim() {
      const t = next();
      if (!t) throw new Error('unexpected end of input');
      if (t.t === 'num') return { type: 'num', v: t.v };
      if (t.t === 'str') return { type: 'str', v: t.v };
      if (t.t === 'kw' && (t.v === 'True' || t.v === 'False')) return { type: 'bool', v: t.v === 'True' };
      if (t.t === 'name') return { type: 'name', v: t.v };
      if (t.t === 'op' && t.v === '(') { const e = expr(); eatOp(')'); return e; }
      throw new Error("invalid expression: '" + t.v + "'");
    }
    function args() {
      const a = [];
      if (!(peek() && peek().t === 'op' && peek().v === ')')) {
        a.push(expr());
        while (peek() && peek().t === 'op' && peek().v === ',') { next(); a.push(expr()); }
      }
      return a;
    }

    function stmt() {
      const t = peek();
      if (t && t.t === 'kw' && t.v === 'if') { next(); const cond = expr(); eatOp(':'); return { type: 'if', cond, body: stmt() }; }
      if (t && t.t === 'kw' && t.v === 'while') { next(); const cond = expr(); eatOp(':'); return { type: 'while', cond, body: stmt() }; }
      if (t && t.t === 'kw' && t.v === 'for') {
        next();
        const nm = next();
        if (!nm || nm.t !== 'name') throw new Error('expected a variable name');
        eatKw('in'); eatKw('range'); eatOp('(');
        const ra = args(); eatOp(')'); eatOp(':');
        return { type: 'for', v: nm.v, range: ra, body: stmt() };
      }
      if (t && t.t === 'kw' && t.v === 'print') { next(); eatOp('('); const a = args(); eatOp(')'); return { type: 'print', args: a }; }
      if (t && t.t === 'name' && toks[pos + 1] && toks[pos + 1].t === 'op' && toks[pos + 1].v === '=') {
        const nm = next().v; next();
        return { type: 'assign', name: nm, expr: expr() };
      }
      return { type: 'expr', expr: expr() };
    }

    const s = stmt();
    if (pos !== toks.length) throw new Error('unexpected trailing tokens');
    return s;
  }

  // --- evaluator ------------------------------------------------------------
  const truthy = (v) => v !== 0 && v !== '' && v !== false && v != null;
  const pyStr = (v) => (v === true ? 'True' : v === false ? 'False' : String(v));

  function applyOp(op, l, r) {
    switch (op) {
      case '+': return (typeof l === 'string' || typeof r === 'string') ? pyStr(l) + pyStr(r) : l + r;
      case '-': return l - r;
      case '*': return l * r;
      case '/': if (r === 0) throw new Error('division by zero'); return Math.trunc(l / r);
      case '%': if (r === 0) throw new Error('division by zero'); return ((l % r) + r) % r;
      case '>': return l > r;
      case '<': return l < r;
      case '>=': return l >= r;
      case '<=': return l <= r;
      case '==': return l === r;
      case '!=': return l !== r;
    }
    throw new Error("unknown operator '" + op + "'");
  }

  function ev(n, env) {
    switch (n.type) {
      case 'num': case 'str': case 'bool': return n.v;
      case 'name': if (!(n.v in env)) throw new Error("name '" + n.v + "' is not defined"); return env[n.v];
      case 'un': return -ev(n.e, env);
      case 'bin': return applyOp(n.op, ev(n.l, env), ev(n.r, env));
    }
    throw new Error('unknown node');
  }

  function run(node, env, out, depth) {
    if (depth > 60) throw new Error('maximum nesting depth exceeded');
    switch (node.type) {
      case 'assign': env[node.name] = ev(node.expr, env); return;
      case 'expr': ev(node.expr, env); return;
      case 'print': out.push(node.args.map((a) => pyStr(ev(a, env))).join(' ')); return;
      case 'if': if (truthy(ev(node.cond, env))) run(node.body, env, out, depth + 1); return;
      case 'for': {
        const r = node.range.map((a) => ev(a, env));
        let start = 0, stop;
        if (r.length === 1) stop = r[0]; else { start = r[0]; stop = r[1]; }
        let c = 0;
        for (let k = start; k < stop; k++) {
          if (c++ > 1000) throw new Error('too many iterations');
          env[node.v] = k;
          run(node.body, env, out, depth + 1);
        }
        return;
      }
      case 'while': {
        let c = 0;
        while (truthy(ev(node.cond, env))) {
          if (c++ > 1000) throw new Error('infinite loop (>1000 iterations)');
          run(node.body, env, out, depth + 1);
        }
        return;
      }
    }
  }

  /**
   * Run a list of lines REPL-style in a shared namespace.
   * A failing line does not abort the program — it is marked as failed and the
   * rest keep running, so the "chaos" of random assembly stays visible.
   *
   * @param {string[]} lines  fragments to run
   * @param {object}   [env]  external namespace. Pass the same object across
   *   calls ("sky memory") to accumulate state so the program grows over time;
   *   without it, every strike starts from a clean slate.
   */
  function runProgram(lines, env) {
    env = env || {};
    const out = [], trace = [];
    for (const line of lines) {
      const before = out.length;
      try {
        run(parse(line), env, out, 0);
        trace.push({ line, ok: true, produced: out.slice(before) });
      } catch (e) {
        trace.push({ line, ok: false, err: e.message });
      }
    }
    return { out, trace, env };
  }

  const StormLang = { tokenize, parse, runProgram };

  if (typeof module !== 'undefined' && module.exports) module.exports = StormLang;
  else global.StormLang = StormLang;
})(typeof globalThis !== 'undefined' ? globalThis : this);
