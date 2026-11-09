# GALAXY ESCAPE

ENGG1330 Group Project 2026–27 — a single-player, turn-based console puzzle adventure in Python.

> **TODO before submitting:** fill in every `[TODO]` below (group number, names, subclass,
> contributions, test results), then delete this note.

| | |
|---|---|
| Group | [TODO group no.] |
| Subclass | [TODO e.g. 1A] |
| Members | Peak [TODO full name], Antonio [TODO full name], [TODO member 3], [TODO member 4] |
| Container | `engg1330-project:2026-v03` |
| Entry point | `main.py` |
| Playtime | about [TODO measured] minutes for one full run |

## 1. Purpose and story

You were captured and taken aboard the enemy battle station **IRONWAKE**. You slipped
away from the guards, and the last ship leaves at midnight. Escape through three levels,
reach the control room, set the station to self-destruct and fly away before it explodes.

## 2. How to run

Inside the course container, from the top level of the extracted project folder:

```
python3 main.py
```

- Terminal must be at least **80 columns × 24 rows**. If the window is smaller (at the
  start or in the middle of play), the game pauses with a short "WINDOW TOO SMALL"
  message and carries on when the window is made bigger.
- No extra packages: Python standard library only.
- If the maze's ball/star symbols look wrong, run `python3 main.py --ascii`.
- `Ctrl+C` quits the game at any time (and skips the end credits).

Each level can also be run on its own for testing, e.g. `python3 LV3.py`.

## 3. Rules and controls

| Screen | What you do | Controls |
|---|---|---|
| Welcome + How to play | Read the story and the rules (3 pages) | `ENTER` next page, `b` back |
| Level 1 – Holding cell | [TODO update when LV1 is finished] Ask two strangers questions, then decide which one is the enemy spy. Wrong choice = caught. | Type a number + `ENTER` |
| Stealth alert (between levels, 50% chance) | A guard comes close. Press the shown letter before the bar runs out (2.5 s). | One key, no `ENTER` |
| Level 2 – Maintenance tunnels | Guide the ball through a random maze to the exit star (bottom-right). | Arrow keys or `W A S D`, `R` new maze, `Q` twice to quit (= caught) |
| Level 3 – Control room | Search the room for clues, then crack the 5-letter self-destruct code, Wordle-style. 6 guesses per try; you can search again and retry. | Type a number / a 5-letter word + `ENTER`; `BACK` leaves the panel |

**Code colours (Level 3):** green `[A]` = right letter, right spot; yellow `(A)` = in the code,
wrong spot; gray ` A ` = not in the code.

**Win:** enter the correct code in Level 3. The ship flies off, the station explodes and
the end credits roll.
**Lose:** pick the wrong suspect, quit the maze, or get spotted by a guard → GAME OVER.
**Restart:** after a win or a loss the game asks `Play again? (y/n)`. You can also exit
and run `python3 main.py` again.

## 4. Connected puzzles

- The clues in the Level 3 control room (the commander's log and the broken screen)
  change what the player knows when using the self-destruct panel: without them the
  panel shows no hint.
- [TODO if added: Level 1 reward (clue / keycard) used in Level 2 or Level 3.]
- Clearing each level is what unlocks the next part of the station.

## 5. Files

| File | What it does |
|---|---|
| `main.py` | Runs the whole game: lobby → levels → credits, game over and play again |
| `Lobby.py` | Welcome screen and the 3 how-to-play pages |
| `LV1.py` | Level 1: holding cell / find the spy |
| `LV2.py` | Level 2: random maze (recursive backtracker + BFS check) |
| `LV3.py` | Level 3: control room, Wordle-style code panel, ending animation |
| `Stealth.py` | Random stealth event between levels |
| `Endcredit.py` | Scrolling end credits |
| `screen.py` | Pauses the game while the window is smaller than 80 × 24 |
| `test_game.py` | Automated tests (see section 8) |
| `ai_use.md` | Generative AI disclosure log |
| `ACKNOWLEDGEMENTS.md` | Sources, inspirations and borrowed ideas |

Every level follows one contract so `main.py` can chain them: each entry function returns
`True` if the player cleared it and `False` if they were caught.

## 6. Design choices (short)

- **Nested data structures:** the maze is a list of lists (`grid[row][col]`); how-to-play
  pages are a list of `(title, lines)` tuples; Level 3 keeps guesses as `(word, result)` pairs.
- **Maze generation:** randomised depth-first search with an explicit stack (no recursion
  limit). A breadth-first search then measures the shortest route ("par") and the maze is
  rejected if it has fewer than 12 dead ends, so every maze is solvable and not too easy.
- **Wordle scoring:** two passes. Greens are marked first; the remaining answer letters are
  counted, and yellows are only given while that count lasts. This stops a repeated letter
  (e.g. `EEEEE` vs `OMEGA`) from showing extra yellows.
- **80 × 24 screen:** every screen is redrawn from the top-left (`\033[H`) instead of
  printing more lines, so the terminal never scrolls.
- **Our own `input()`:** `screen.ask(prompt, redraw)` reads one key at a time in cbreak
  mode, like the maze. Every 0.25 s without a key it checks the window size, so a resize
  while typing pauses at once; `redraw()` then puts the screen back. It refuses keys that
  would go past column 79, so typed answers cannot wrap or scroll the 80 × 24 area. Without
  a real terminal (tests) it falls back to `input()`.
- **Small window = pause, not quit:** one shared function, `screen.wait_for_size()`, is
  called before every screen is drawn (and before every animation frame). If the window is
  under 80 × 24 it shows a message cut down to fit the window, checks the size every 0.3 s,
  then clears the screen so the caller redraws. Keys pressed while paused are thrown away.
  The maze polls for a key every 0.25 s instead of blocking, so it can pause straight away.
  The stealth event checks the size *before* its timer starts, so the pause is never unfair.

## 7. Invalid actions and boundary cases

The game never crashes or ends by accident on bad input. A wrong action is
explained on screen and the player stays where they were.

| Where | Invalid action / boundary case | What the game does |
|---|---|---|
| Every typed prompt | `Ctrl+D` (end of input) | Leaves cleanly with "Thanks for playing!" (was a crash: `EOFError`) |
| Every typed prompt | `Ctrl+C` | Leaves cleanly; during the credits it only skips the credits |
| How-to-play pages | Any key other than `ENTER` / `b` | Same page, message: `'xyz' is not a command. Press ENTER, or type b to go back.` |
| How-to-play pages | `b` on page 1 (lower boundary) | Stays on page 1: "This is already the first page." |
| Level 3 room menu | Empty input, `9`, `hello` | Same room, says what was typed and that 1, 2 or 3 is needed |
| Level 3 panel | Empty input | "You didn't type anything." No guess used |
| Level 3 panel | 4 or 6 letters (one off the boundary of 5) | "Too short: 4 letter(s)" / "Too long: 6 characters". No guess used |
| Level 3 panel | Digits, spaces, symbols, accented letters (`É`) | Names the bad character, "Use the letters A-Z only." No guess used |
| Level 3 panel | Same code typed twice | "You already tried BUILT." No guess used |
| Level 3 panel | Panel opened before finding clues | Type `BACK` to leave without losing; guesses-left counter shown |
| Level 3 panel | 6th (last) guess | Red "LAST GUESS!" warning; a right last guess still wins |
| Level 2 maze | Walking into a wall | Ball stays, footer: "Bump! That's a wall" |
| Level 2 maze | Unknown key / lone `Esc` | Ignored, footer explains the controls |
| Level 2 maze | `Q` pressed by mistake | Asks to confirm; `Q` again quits (= caught), any other key cancels |
| Play again? | `maybe`, empty, `1` | Asked again ("Please type y or n"); accepts `y`/`yes`/`n`/`no` in any case |
| Any screen | Window smaller than 80 × 24, down to 1 × 1 | Game pauses with a message that fits, carries on when enlarged |
| Any typed prompt | Window made smaller **while typing** | Pauses at once (not after `ENTER`); when enlarged, the screen is redrawn and the text typed so far comes back |
| Any typed prompt | Typing past the end of the row (e.g. 200 keys) | Extra keys ignored at column 79, so the answer never wraps or scrolls the screen |
| Any typed prompt | Arrow keys, Tab, Esc, Thai / Chinese letters | Control keys ignored; wide characters counted as 2 columns so the limit still holds |
| Stealth alert | Window made smaller during the countdown | Timer pauses and keeps the time left; the alert is redrawn, then the countdown carries on |

## 8. Testing

### Automated tests

```
python3 -m unittest -v test_game.py
```

57 tests, standard library only. They replace `input()` with pre-typed answers, so no
keyboard is needed. They cover:

- Wordle scoring, including repeated letters
- Level 3: win, invalid codes (too short/long, digits, empty, symbols, accented letters,
  repeated codes) that do not cost a guess, winning on the last guess, running out of
  guesses, `BACK` out of the panel, invalid menu choices, retrying after a failed panel
- Level 2 play loop: one `Q` only asks, two `Q`s quit, another key cancels, wall bump and
  unknown-key messages
- Level 2: 30 random mazes are all solvable with a solid border and enough dead ends;
  BFS on a hand-made grid; key mapping
- Every fixed screen (welcome art, how-to-play pages, credits, ending art) fits 80 × 24
- Stealth: no guard, right letter, capital letter, wrong letter, too slow
- `main.py`: win, game over at each step, play again / quit, invalid play-again answers
  are asked again, `Ctrl+D` exits cleanly
- How-to-play: `b` on the first page and unknown commands show a message
- Small window: the pause message fits every size from 1 × 1 to 79 × 23; exactly
  80 × 24 does not pause; the game waits until the window is big enough again; the maze
  notices a resize without a key press; the stealth timer pauses while the window is small
- Typing: answers stop exactly at the end of the prompt's row, wide characters count as 2
  columns, backspace / ENTER / control keys, every prompt leaves room for a 5-letter code

### Manual tests (in a fresh `engg1330-project:2026-v03` container)

| # | Test | Expected | Result |
|---|---|---|---|
| 1 | Full normal playthrough | Reaches ending animation and credits | [TODO] |
| 2 | Type letters / empty input in numbered menus | Message naming the bad input, same screen again | [TODO] |
| 3 | Level 3: type `ab`, `12345`, empty, the same code twice | Specific message (too short / A-Z only / already tried), no guess used | [TODO] |
| 4 | Level 3: use all 6 guesses wrong | Alarm message, back in the room, can retry | [TODO] |
| 5 | Maze: walk into walls, press unknown keys | Ball does not move, footer message, no crash | [TODO] |
| 6 | Maze: press `Q`, then `Q` again | First asks to confirm; second → GAME OVER, then "Play again?" | [TODO] |
| 7 | Stealth: wrong key / wait too long | Caught → GAME OVER | [TODO] |
| 8 | Win, then `y` at "Play again?" | Game restarts from the welcome screen | [TODO] |
| 9 | Start in a window smaller than 80 × 24, then enlarge it; shrink it during the maze | "WINDOW TOO SMALL" message, game continues where it was after enlarging | [TODO] |
| 10 | `Ctrl+C` during credits / during play | Credits skipped / game exits cleanly | [TODO] |
| 11 | `Ctrl+D` at any typed prompt | "Thanks for playing!", no traceback | [TODO] |
| 12 | Level 3: open panel first, type `BACK` | Back in the room, can search for clues | [TODO] |
| 13 | "Play again?": type `maybe` | Asked again | [TODO] |
| 14 | At any typed prompt, hold a key down | Typing stops at the end of the row, nothing wraps or scrolls | [TODO] |
| 15 | Start typing a code, shrink the window, enlarge it | Pause message at once; panel comes back with the letters typed so far | [TODO] |
| 16 | Shrink the window during the stealth countdown | Timer pauses; countdown continues after enlarging | [TODO] |

## 9. Known limitations

- [TODO remove when done] Level 1 is still a placeholder (choose 1 to continue).
- The stealth event uses a 2.5-second timer. The brief says real-time controls are out of
  scope; [TODO: result of asking the STA — keep / make turn-based / disable with
  `STEALTH_CHANCE = 0` in `main.py`].
- Level 2 needs an interactive terminal (it reads single key presses).
- On Windows, `screen.ask()` falls back to `input()`, so there a resize while typing is
  noticed after `ENTER` and a very long answer can wrap. The course container (Linux) uses
  the full version.
- Level 3 never ends in a loss: after 6 wrong guesses the player can search the room and
  retry. This is on purpose so the final puzzle cannot block the ending.
- Colours use ANSI escape codes; very old terminals may show raw codes.

## 10. Contributions

| Member | Contributions |
|---|---|
| Peak | [TODO check] Level 1 (owner); joined all files into `main.py`; how-to-play rules; Level 3 ending animation; game plan document; README, tests |
| Antonio | [TODO check] Level 2 maze |
| [TODO member 3] | [TODO] Stealth event idea and first version (`Stealth.py`) |
| [TODO member 4] | [TODO] e.g. Level 3, welcome screen art, end credits, videos |

Everyone: planning on the team Excalidraw board, playtesting, checking the final
submission. [TODO edit to match what actually happened.]

## 11. Sources and acknowledgements

See `ACKNOWLEDGEMENTS.md` (sources and inspirations) and `ai_use.md` (generative AI use).
