# ⚡ StormClouds — a code storm

A cloud-and-lightning simulation where **code is genuinely born from chaos**.

Every cloud carries a Python fragment. "Wind" drifts the clouds across the
sky; when they collide they exchange charge and drop their fragment into a
**storm cell**. Once the cell's charge reaches a threshold — **lightning**:
the accumulated fragments are assembled into a program and **executed** by a
small embedded Python-subset interpreter, and the result (with output, and
with errors on lines whose variables weren't defined yet) goes to the
discharge log.

The idea grew from a simple question — "when clouds rub against each other,
do you get electricity?" — carried over to code: what if you let blocks of
code collide like clouds and watch what "discharges" come out.

## Metaphor -> mechanics

| Phenomenon       | What actually happens                                          |
| ---------------- | -------------------------------------------------------------- |
| 🌬️ Wind          | Random drift of clouds across the grid                         |
| 💥 Collision     | Clouds exchange charge and drop their fragment into the cell   |
| ⚡ Lightning     | The assembled program is **executed** (REPL-style)             |
| Charge ±         | Sign of a cloud's charge (warm = plus, cool = minus)           |

Errors are a feature: you can see a working snippet occasionally assemble
itself out of random order, and more often just syntactic noise. A line
missing a variable is flagged and skipped; the rest keep running.

## Run

No build, no dependencies — it's a static page.

```bash
# just open the file in a browser
open index.html        # macOS
xdg-open index.html    # Linux

# or serve it locally
python3 -m http.server 8000
# -> http://localhost:8000
```

## Structure

```
stormclouds/
├── index.html            # instrument-panel markup
├── styles.css            # "night storm" theme
├── js/
│   ├── interpreter.js    # mini-Python: tokenizer -> parser -> evaluator (StormLang)
│   └── simulation.js     # clouds, wind, collisions, strikes, rendering
├── tests/
│   └── interpreter.test.js
└── README.md
```

`interpreter.js` is a pure, DOM-free module; it works both in the browser
(global `StormLang`) and in Node (`require`), which is what the tests use.

## The mini-language (a subset of Python)

Each fragment is one self-contained line. Supported:

- assignment: `x = 5`, `x = x + 1`, `msg = "storm"`
- arithmetic: `+ - * / %` (division is integer, like `//`)
- comparisons: `> < >= <= == !=`
- `print(...)` with multiple arguments
- single-line `if <cond>: <stmt>`
- single-line `while <cond>: <stmt>` (guarded to <= 1000 iterations)
- `for i in range(n): <stmt>` and `for i in range(a, b): <stmt>`

```js
StormLang.runProgram(['x = 5', 'print(x + 1)']);
// -> { out: ['6'], trace: [...], env: { x: 5 } }
```

## Controls

- **⏸ Pause / ▶ Play** — stop/resume the simulation
- **🌬 Gust** — shake all clouds
- **＋ Cloud** — add a cloud with a random fragment
- **⚡ Strike** — force lightning with the current cell
- **🧠 Memory** — toggle: shared namespace across strikes. Off — every strike
  starts from a clean slate (pure chaos); on — variables survive strikes and
  the program grows over time.
- **🎯 Coverage** — toggle: re-seeds the sky so that every base definition
  (`x = 5`, `y = 3`, …) is carried by at least one cloud. Removes the
  "opening-draw lottery".
- **🧬 Evolution** — toggle: useful fragments "reproduce" among clouds while
  useless ones are pushed out. Selection uses the *average reward per
  appearance* (not the sum — otherwise merely frequent fragments win), and
  printing is valued above bare success. Replacement count — "🧬 Swaps" in the
  telemetry.
- **↺ Reset** — clear the sky and the log
- **Speed** — wind tempo
- **click the sky** — a new cloud at that spot
- **click a cloud** — re-roll its fragment

Each line in the discharge log is tagged with the source cloud (`C1…Cn`) that
brought that fragment.

## Tests

```bash
node tests/interpreter.test.js
```

## Notes and measurements

These come from headless-browser runs and are what motivated each toggle:

- **Sky memory** on average lifts the share of lines that run (~45% -> ~75%),
  but widens the variance: the outcome depends on which base fragments the
  clouds were dealt at the start.
- **Coverage** removes that lottery: with memory + coverage the run-rate is
  ~94% (sd ~6) versus ~52% (sd ~32) without it.
- **Evolution**: a naive fitness ("sum of survivals") collapses the population
  into a trivial self-contained monoculture. Switching to *average reward per
  appearance* and valuing printing pushes the share of printing fragments
  ~7% -> ~24% and roughly doubles output per strike, without killing the
  assignments they depend on. The lesson: **selection optimizes exactly what
  you measure, not what you want.**

## Where it could go

- **Save / load** interesting "sky runs" and their programs.
- A custom mini-language, tuned for assembly from random pieces, instead of a
  Python subset.

## License

Free to use — including commercially and inside your own projects — but if you
make money from a product that includes this code, **7% of that revenue goes to
the author**. See [`LICENSE`](LICENSE). The author keeps full ownership and can
license it separately. This is a custom royalty license, not a standard
open-source one.

---

A standalone, educational/toy side-project. Unrelated to any analyzer — it
lives entirely on its own.
