/*
 * Тесты мини-интерпретатора StormLang. Без фреймворков.
 * Запуск:  node stormclouds/tests/interpreter.test.js
 */
'use strict';

const StormLang = require('../js/interpreter.js');

let passed = 0, failed = 0;

function eq(actual, expected, name) {
  const a = JSON.stringify(actual), e = JSON.stringify(expected);
  if (a === e) { passed++; }
  else { failed++; console.error('  ✗ ' + name + '\n      ожидалось: ' + e + '\n      получено:  ' + a); }
}

// вывод программы (массив строк из print)
const out = (lines) => StormLang.runProgram(lines).out;
// сколько строк исполнилось без ошибки
const okCount = (lines) => StormLang.runProgram(lines).trace.filter((t) => t.ok).length;

// --- присваивание и печать ---
eq(out(['x = 5', 'print(x)']), ['5'], 'присваивание и печать');
eq(out(['x = 5', 'x = x + 1', 'print(x)']), ['6'], 'мутация переменной');
eq(out(['print(2 + 3 * 4)']), ['14'], 'приоритет операций');
eq(out(['print((2 + 3) * 4)']), ['20'], 'скобки');
eq(out(['print(7 % 3)']), ['1'], 'остаток');
eq(out(['print(7 / 2)']), ['3'], 'целочисленное деление (trunc)');

// --- строки ---
eq(out(['msg = "storm"', 'print(msg)']), ['storm'], 'строковая переменная');
eq(out(['print("a" + "b")']), ['ab'], 'конкатенация строк');

// --- сравнения и if ---
eq(out(['x = 5', 'if x > 3: print("да")']), ['да'], 'if истинный');
eq(out(['x = 1', 'if x > 3: print("нет")']), [], 'if ложный — нет вывода');

// --- циклы ---
eq(out(['for i in range(3): print(i)']), ['0', '1', '2'], 'for range(n)');
eq(out(['for i in range(2, 5): print(i)']), ['2', '3', '4'], 'for range(a, b)');
eq(out(['k = 2', 'while k < 10: k = k + 3', 'print(k)']), ['11'], 'while');

// --- REPL: общий namespace, ошибки не роняют программу ---
eq(okCount(['print(x)', 'x = 5', 'print(x)']), 2, 'строка с ошибкой пропускается, остальные ok');
eq(out(['print(x)', 'x = 5', 'print(x)']), ['5'], 'после ошибки вывод продолжается');

// --- память неба: общий env между вызовами ---
{
  const sky = {};
  StormLang.runProgram(['x = 5'], sky);          // разряд 1: объявили x
  const r = StormLang.runProgram(['print(x)'], sky); // разряд 2: x пережил
  eq(r.out, ['5'], 'общий env: переменная переживает разряд');
  eq(sky.x, 5, 'общий env мутируется на месте');
}
{
  const sky = {};
  StormLang.runProgram(['n = 10'], sky);
  StormLang.runProgram(['n = n - 3'], sky);
  const r = StormLang.runProgram(['print(n)'], sky);
  eq(r.out, ['7'], 'общий env: накопление за три разряда');
}
eq(out(['x = 5', 'print(x)']), ['5'], 'без env — как раньше, чистый лист');

// --- защита от зацикливания ---
eq(okCount(['while k < 5: k = k']), 0, 'необъявленная k → ошибка, не вечный цикл');
{
  const r = StormLang.runProgram(['k = 0', 'while k < 5: k = 0']);
  eq(r.trace[1].ok, false, 'бесконечный while останавливается ошибкой');
}

// --- итог ---
console.log('\nStormLang: ' + passed + ' passed, ' + failed + ' failed');
process.exit(failed ? 1 : 0);
