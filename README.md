# DEATHSTAR ESCAPE

ENGG1330 Group Project 2026–27. A single-player console puzzle adventure in Python.

| | |
|---|---|
| Group | 7 |
| Subclass | 1B |
| Members | Khanthithao Krittichok, Leung Ho Long Ryan, Mensah Lord Kojo Tandoh, Sutowo Antonio |
| Container | `engg1330-project:2026-v03` |
| Entry point | `main.py` |
| Playtime | about 3–5 minutes for one full run |

## 1. Purpose and story

You are a REBEL, captured and brought aboard the Empire's battle station, the **Death Star**.
You slipped away from your guards, and the last ship leaves at midnight.

1. Prove you can handle a blaster on the **blaster range** to earn an access card.
2. Run through the **maintenance tunnels** before the clock runs out, and grab a crystal
   that holds part of the self-destruct code.
3. Crack the **self-destruct code** in the control room.

Guards patrol between the levels, so you have to hide quickly. When the code is accepted,
you take an X-wing out of the hangar, the station explodes behind you and the end credits
roll.

## 2. How to run

Inside the course container, from the top level of the extracted project folder:

```
python3 main.py
```

- Terminal must be at least **80 columns × 24 rows** (bigger is fine; the game only uses
  80×24). Whenever the window is smaller, at any point while `main.py` runs, everything
  pauses (timers, animations, drawing) and one message asks you to enlarge it. The
  game carries on from the same screen when the window is big enough again.
- No extra packages: Python standard library only.
- `python3 main.py --ascii` draws the Level 2 maze with plain ASCII characters, for
  terminals without UTF-8.
- Each part can also be run on its own for testing, e.g. `python3 LV1.py`,
  `python3 Stealth.py`, `python3 LV2.py`, `python3 LV3.py`, `python3 Endcredit.py`.

## 3. Rules and controls

The game runs in this order:

**Title → How to play → Level 1 → Guard → Level 2 → Guard → Level 3 → End credits**

Most screens are turn based: nothing happens until you type an answer and press `ENTER`.
Two parts are timed: the guard events (5 seconds) and the Level 2 maze (45 seconds).

| Screen | What you do | Controls |
|---|---|---|
| Title | Animated title with twinkling stars | `ENTER` |
| How to play | Story and a short summary of every level | `ENTER` |
| Level 1: Blaster range | Clear every stormtrooper from a 3×3 grid of doors in **4 rounds**, using a limited number of shots (see table below). Each shot hits everything in its row, column or door, **allies included**. | `r1`–`r3` row, `c1`–`c3` column, `1`–`9` one door, `hint`, `reset`, `help`, `quit` |
| Guard event (after Level 1 and after Level 2) | A guard is coming. The game shows a hiding place, e.g. `TYPE VENT and press ENTER`. Type the word before the 5-second bar runs out. A wrong word clears the line so you can try again. | Letters, `Backspace`, `ENTER` (any case) |
| Level 2: Maintenance tunnels | Reach the exit `★` (bottom-right) of a random maze within **45 seconds**. A crystal `◆` is hidden somewhere in the tunnels. Walk over it to collect it (optional). | Arrow keys or `w a s d`, one step per press. Hold a key to keep moving; no `ENTER` |
| Level 3: Control room | Read the commander's log for a clue, then guess the **5-letter self-destruct code**, Wordle-style. **4 guesses** (5 with the Level 1 bonus). | `1` read the log, `2` open the panel, a 5-letter word, `BACK` leave the panel, `quit` |
| End credits | The station explodes, then the credits scroll over the stars | `ENTER` to finish |

### Level 1 rounds

| Round | Name | Shots | Special |
|---|---|---|---|
| 1 | Warm up | 2 | Plain troopers |
| 2 | Armor plating | 4 | Armored troopers `=[o o]=` need 2 hits (the first hit cracks them into a normal trooper) |
| 3 | The conveyor | 3 | Row 2 (marked `>>`) is a conveyor belt: after every shot it slides one door right, and the last door wraps around to the first |
| 4 | Double trouble | 4 | Armor and a conveyor belt together |

- A round fails if you **run out of shots** with troopers left, or **hit 2 allies**
  (rebel pilots `.-=-.`). A failed round restarts. `reset` restarts it yourself.
- Shooting a row, column or door with nothing in it is not counted as a shot.
- `hint` shows one safe shot (one that hits a trooper and no ally) that can still lead
  to clearing the round. If none is left, it tells you to `reset`.
- `help` shows the Level 1 instructions again.

### Level 3 code colours

| Tile | Meaning |
|---|---|
| green `[A]` | right letter, right place |
| yellow `(A)` | letter is in the code, but in another place |
| gray ` A ` | letter is not in the code |

Leaving the panel with `BACK` keeps the guesses you have already used.

### Winning, losing and restarting

- **Win:** enter the correct code in Level 3. The station explodes, the credits roll and
  the game shows "You escaped from the Death Star!".
- **Lose (GAME OVER):** too slow in a guard event; the Level 2 clock reaches 0; all
  Level 3 guesses wrong; or `quit` (in Level 1, at the Level 2 start screen, or in
  Level 3). The game-over screen shows *"You are caught and executed by the EMPIRE"*.
- **Restart:** after a win or a loss the game asks `Play again? (y/n)`. `y` starts again
  from the title screen, `n` quits.
- `Ctrl+C` quits the game with "Thanks for playing!". In Level 1 it counts as giving up
  (GAME OVER, then `Play again?`).

## 4. Connected puzzles

What you do in one level changes the next ones:

- **Level 1 → Level 3:** finish all 4 rounds without hitting **any** ally (failed
  attempts count too) and you get **one extra guess** (5 instead of 4) on the
  self-destruct panel.
- **Level 2 → Level 3:** collect the crystal `◆` in the maze and the panel shows one
  letter of the code from the start (`_ _ _ E _`). No crystal, no letter.
- **Inside Level 3:** the commander's log gives the word clue "Think lightsaber."
  The panel shows `Clue: ???` until you read it.
- Clearing each level unlocks the next part of the station.

## 5. Files

| File | What it does |
|---|---|
| `main.py` | Runs the whole game in order, then the end credits or the game-over screen, and asks to play again |
| `Lobby.py` | Animated title screen and the how-to-play page |
| `LV1.py` | Level 1: blaster range (depth-first search for the `hint` command) |
| `Stealth.py` | Guard event between levels: type the hiding-place word before the countdown bar runs out |
| `LV2.py` | Level 2: random maze with a 45-second clock (depth-first search to build it, breadth-first search for the shortest route) |
| `LV3.py` | Level 3: control room and Wordle-style code panel |
| `Endcredit.py` | Station explosion animation and scrolling end credits |
| `defeated.py` | Game-over picture and message |
| `screen.py` | Shared screen code: colours, clearing the screen, 80 × 24 check and pause |
| `ai_use.md` | Generative AI disclosure log |
| `ACKNOWLEDGEMENTS.md` | Sources, inspirations and borrowed ideas |

Each part returns whether the player got through, so `main.py` can chain them:
`LV1.run_level1()` returns `{"passed": ..., "bonus_guess": ...}`;
`Stealth.quicktime()`, `LV2.play()` and `LV3.play()` return `True` or `False`.
`LV2.found_hint` remembers whether the crystal was collected.

## 6. Design choices (short)

- **Nested lists:** the Level 1 range and the Level 2 maze are lists of lists
  (`grid[row][col]`); Level 3 keeps guesses as `(word, result)` pairs.
- **Level 1 hint:** a depth-first search tries every shot that hits a trooper and no
  ally, applies it (including the belt slide) to a copy of the grid, then searches again
  from there, until the grid is clear or the shots run out.
- **Maze generation:** randomised depth-first search with a stack. Every cell is visited,
  so the exit can always be reached. Mazes with fewer than 12 dead ends are thrown away
  so the maze is not too easy. A breadth-first search finds the shortest route, shown
  after the maze as "shortest possible".
- **Fast maze drawing:** the maze is drawn once; after that only the player's old and new
  squares and the clock are redrawn, so holding a key stays smooth.
- **Wordle scoring:** two passes. Greens first; the letters of the code that are left are
  counted, and yellows are only given while that count lasts, so `EEEEE` against the code
  shows one green and no yellows.
- **Guard timer without threads:** the guard event reads one key at a time with a short
  timeout and redraws the bar in between. Keys still waiting when it ends are thrown
  away, so a late key press cannot leak into the next level.
- **80 × 24 screen:** every screen clears the terminal and is drawn from the top, and
  each screen is written to fit inside 80 × 24, so pressing `ENTER` never scrolls.
- **Small window:** before every screen, `screen.wait_for_size()` checks the terminal
  size. If it is under 80 × 24 it shows a one-line message (cut to fit the window) and
  waits. In Level 2 the clock is paused while it waits.

## 7. Invalid actions and boundary cases

A wrong action is explained on screen and the player stays where they were.

| Where | Invalid action / boundary case | What the game does |
|---|---|---|
| Any screen | Window smaller than 80 × 24, down to 1 × 1 | Pauses with a message that fits, carries on when enlarged |
| Any prompt (outside Level 1) | `Ctrl+C` / `Ctrl+D` | Quits cleanly with "Thanks for playing!" |
| Level 1 | `Ctrl+C` / `Ctrl+D` | Counts as giving up: GAME OVER, then `Play again?` |
| Level 1 | `zzz`, `r9`, `c4`, empty | "not a valid command", no shot used |
| Level 1 | A row, column or door with nothing in it | "Nothing to hit", no shot used |
| Level 1 | 1 ally hit | Warning, round goes on, Level 3 bonus lost |
| Level 1 | 2 allies hit in one round | ROUND FAILED, round restarts |
| Level 1 | Last shot used with troopers left | ROUND FAILED, round restarts |
| Level 1 | `hint` when no safe plan is left | Says to type `reset` |
| Guard event | Wrong word | "Wrong!", line cleared, timer keeps running |
| Guard event | Keys pressed before the bar appears | Ignored (Mac / Linux) |
| Guard event | No right word within 5 seconds | Caught, GAME OVER |
| Level 2 | Any key other than arrows / `w a s d` | Ignored, no move |
| Level 2 | Walking into a wall | Stays put |
| Level 2 | Clock reaches 0 | GAME OVER |
| Level 2 | Window made smaller than 80 × 24 | Clock pauses until the window is big enough |
| Level 3 room | Empty input, `9`, `hello` | "is not an option. Choose 1 or 2." |
| Level 3 panel | Empty, 4 or 6 letters, digits, `É`, a code already tried | Says what is wrong, no guess used |
| Level 3 panel | Lowercase guess | Accepted (turned into capitals) |
| Level 3 panel | Opened before reading the log | Allowed; `BACK` leaves without losing guesses |
| Play again? | `maybe`, empty | Asked again; accepts `y`/`yes`/`n`/`no` |

## 8. Testing

### Manual tests (in a fresh `engg1330-project:2026-v03` container)

| # | Test | Expected | Result |
|---|---|---|---|
| 1 | Full normal playthrough | Reaches the explosion, credits and "You escaped from the Death Star!" | Pass |
| 2 | Level 1: shoot one ally, then a second one | First: warning, round goes on. Second: ROUND FAILED, round restarts. No bonus at the end | [TODO retest] |
| 3 | Level 1: type `hint` | Shows a safe shot | Pass |
| 4 | Level 1: clear all rounds with no ally hit | "Bonus: one extra guess", Level 3 shows 5 guesses | [TODO test] |
| 5 | Guard event: type a wrong word, then the right one in time | "Wrong!", then "You hide ..." | [TODO test] |
| 6 | Guard event: type nothing for 5 seconds | Caught, GAME OVER | [TODO test] |
| 7 | Level 2: hold an arrow key, walk into a wall, press `x`, let the clock run out | Moves step by step, no crash, GAME OVER | [TODO retest] |
| 8 | Level 2: collect the crystal, then reach the exit | Crystal screen; Level 3 shows `_ _ _ E _` | [TODO test] |
| 9 | Level 3: `ab`, `12345`, empty, same code twice | Message, no guess used | Pass |
| 10 | Level 3: use all guesses wrong | Alarm message, then game-over screen | Pass |
| 11 | Type `quit` in a level, then `y` | GAME OVER, then game restarts from the title | Pass |
| 12 | Start in a window smaller than 80 × 24, then enlarge | Pause message, game carries on | Pass |
| 13 | `Ctrl+C` / `Ctrl+D` at a prompt | "Thanks for playing!", no traceback | Pass |

## 9. Known limitations

- The window size is checked before each screen is drawn. If the window is made smaller
  while the player is typing, the pause comes after `ENTER`.
- A very long typed answer (over one line) can wrap. Normal answers are a few characters.
- Level 2 needs a real terminal (it reads single key presses). Without one, the level
  ends and counts as a loss.
- Terminals without UTF-8 (or `python3 main.py --ascii`) show the maze as `()` player,
  `<>` crystal, `EX` exit.
- Colours use ANSI escape codes; very old terminals may show raw codes.
- The brief asks for a turn-based game. The guard events (5 seconds) and the Level 2
  maze (45 seconds) are timed on purpose by the team to add tension. Resizing the window
  during a guard event does not pause its timer.
- Without a real terminal (e.g. piped input) the guard event uses a normal typed answer,
  and the 5 seconds are checked after `ENTER`.
- On Windows and without a real terminal, the title screen does not twinkle.
- The self-destruct code is fixed, so a second playthrough is easier. The Level 2 maze
  and the guard's hiding word are random every time.

## 10. Contributions

| Member | Contributions |
|---|---|
| Khanthithao Krittichok (Peak) | [TODO check] Level 1 (owner); joined all files into `main.py`; how-to-play rules; Level 3 ending; game plan document; README, tests |
| Sutowo Antonio | [TODO check] Level 2 maze |
| Leung Ho Long Ryan | [TODO check] Guard event (`Stealth.py`): idea and first version; timer rewritten without threads so a late key cannot leak into the next level; typed hiding-place word with a live countdown bar |
| Mensah Lord Kojo Tandoh | [TODO] e.g. Level 3, title screen art, end credits explosion, videos |

Everyone: planning on the team Excalidraw board, playtesting, checking the final
submission. [TODO edit to match what actually happened.]

## 11. Sources and acknowledgements

See `ACKNOWLEDGEMENTS.md` (sources and inspirations) and `ai_use.md` (generative AI use).
