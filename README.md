# homework-alibi

[![make.fun · u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c](https://make.fun/badge/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c.svg)](https://make.fun/bounty/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c?utm_source=github&utm_medium=readme&utm_campaign=u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c)
[![rank](https://make.fun/badge/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c/nmlyz/homework-alibi/rank.svg)](https://make.fun/bounty/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c)
[![reward](https://make.fun/badge/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c/nmlyz/homework-alibi/reward.svg)](https://make.fun/bounty/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c?utm_source=github&utm_medium=readme&utm_campaign=u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c)

homework-alibi writes one line to a file: the excuse a dog gives after being caught eating the homework. The line is the dog talking about itself, deadpan, with a specific detail up front and the punch at the end:

> The worksheet said "show your working", so I showed it my teeth.

## How it works

The program keeps the excuse as two clauses — a setup and a punch — and checks each one on its own before writing anything:

- **Setup** (6 words): the worksheet gives an instruction. It must name the worksheet and the instruction "show your working", start with a capital and end with a comma.
- **Punch** (6 words): the dog obeys the instruction literally. It must name the showing and the teeth, and continue in lower case as the same sentence.

On top of the per-clause checks, the whole line is gated: 1 to 200 characters (this one is 64), a single line, single spaces, plain ASCII, no question or exclamation, and a fixed fingerprint of 12 words, 2 clauses, 1 sentence and 64 bytes. A typo in either clause fails loudly instead of shipping a different joke.

## Run it

```sh
python3 main.py
```

It writes the line to `/output/entry.txt` (or `$MAKEFUN_OUTPUT_DIR/entry.txt` when that is set). No network access, no dependencies beyond the standard library, and the same bytes on every run — the program reads the file back after writing and refuses to finish unless the bytes match the line exactly.

```sh
python3 main.py --check   # validate the line without writing a file
python3 main.py --print   # print the line and nothing else
```

## Determinism

There is no randomness, no clock and no network anywhere in the program: the line is a constant, the checks are pure functions of that constant, and the output is written with a fixed newline. Running it twice produces byte-identical files, which the read-back step verifies on every run.

## Files

- `main.py` — the whole program: clause checks, length and shape gates, writing, read-back verification and the run report.
- `LICENSE` — MIT.

---

<sub>See the line on [make.fun](https://make.fun/bounty/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c)</sub>
