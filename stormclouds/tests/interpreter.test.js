/*
 * Tests for the StormLang mini-interpreter. No framework.
 * Run:  node stormclouds/tests/interpreter.test.js
 */
'use strict';

const StormLang = require('../js/interpreter.js');

let passed = 0, failed = 0;

function eq(actual, expected, name) {
  const a = JSON.stringify(actual), e = JSON.stringify(expected);
  if (a === e) { passed++; }
  else { failed++; console.error('  x ' + name + '\n      expected: ' + e + '\n      actual:   ' + a); }
}

// program output (array of printed strings)
const out = (lines) => StormLang.runProgram(lines).out;
// how many lines ran without error
const okCount = (lines) => StormLang.runProgram(lines).trace.filter((t) => t.ok).length;

// --- assignment and print ---
eq(out(['x = 5', 'print(x)']), ['5'], 'assignment and print');
eq(out(['x = 5', 'x = x + 1', 'print(x)']), ['6'], 'variable mutation');
eq(out(['print(2 + 3 * 4)']), ['14'], 'operator precedence');
eq(out(['print((2 + 3) * 4)']), ['20'], 'parentheses');
eq(out(['print(7 % 3)']), ['1'], 'modulo');
eq(out(['print(7 / 2)']), ['3'], 'integer division (trunc)');

// --- strings ---
eq(out(['msg = "storm"', 'print(msg)']), ['storm'], 'string variable');
eq(out(['print("a" + "b")']), ['ab'], 'string concatenation');

// --- comparisons and if ---
eq(out(['x = 5', 'if x > 3: print("yes")']), ['yes'], 'if taken');
eq(out(['x = 1', 'if x > 3: print("no")']), [], 'if not taken — no output');

// --- loops ---
eq(out(['for i in range(3): print(i)']), ['0', '1', '2'], 'for range(n)');
eq(out(['for i in range(2, 5): print(i)']), ['2', '3', '4'], 'for range(a, b)');
eq(out(['k = 2', 'while k < 10: k = k + 3', 'print(k)']), ['11'], 'while');

// --- REPL: shared namespace, errors don't abort the program ---
eq(okCount(['print(x)', 'x = 5', 'print(x)']), 2, 'failing line is skipped, the rest run');
eq(out(['print(x)', 'x = 5', 'print(x)']), ['5'], 'output continues after an error');

// --- sky memory: shared env across calls ---
{
  const sky = {};
  StormLang.runProgram(['x = 5'], sky);              // strike 1: define x
  const r = StormLang.runProgram(['print(x)'], sky); // strike 2: x survived
  eq(r.out, ['5'], 'shared env: variable survives a strike');
  eq(sky.x, 5, 'shared env is mutated in place');
}
{
  const sky = {};
  StormLang.runProgram(['n = 10'], sky);
  StormLang.runProgram(['n = n - 3'], sky);
  const r = StormLang.runProgram(['print(n)'], sky);
  eq(r.out, ['7'], 'shared env: accumulation over three strikes');
}
eq(out(['x = 5', 'print(x)']), ['5'], 'no env — clean slate, as before');

// --- loop guards ---
eq(okCount(['while k < 5: k = k']), 0, 'undefined k -> error, not an infinite loop');
{
  const r = StormLang.runProgram(['k = 0', 'while k < 5: k = 0']);
  eq(r.trace[1].ok, false, 'an infinite while is stopped by an error');
}

// --- summary ---
console.log('\nStormLang: ' + passed + ' passed, ' + failed + ' failed');
process.exit(failed ? 1 : 0);
