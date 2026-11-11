# GALAXY ESCAPE

ENGG1330 Group Project 2026–27 — a single-player, turn-based console puzzle adventure in Python.

| | |
|---|---|
| Group | 7 |
| Subclass | 1B |
| Members | Khanthithao Krittichok, Leung Ho Long Ryan, Mensah Lord Kojo Tandoh, Sutowo Antonio |
| Container | `engg1330-project:2026-v03` |
| Entry point | `main.py` |
| Playtime | about 3–5 minutes for one full run |

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
- `Ctrl+C` leaves the game at any time.

Each level can also be run on its own for testing, e.g. `python3 LV1.py`.

## 3. Rules and controls

Every screen is turn based: nothing happens until the player acts. Most screens take a
typed answer and `ENTER`; the maze moves one step per key press.

| Screen | What you do | Controls |
|---|---|---|
| Welcome + How to play | Read the story and the rules | `ENTER` |
| Level 1 – Blaster range | Clear a 3×3 grid of troopers in 3 rounds with few shots, without hitting a prisoner. Armored troopers need 2 hits. Hitting a prisoner or running out of shots restarts the round. | `r1`–`r3` row, `c1`–`c3` column, `1`–`9` one door, `hint`, `quit` |
| Level 2 – Maintenance tunnels | Walk through a random maze to the exit `EX` (bottom-right). | Arrow keys or `w a s d`, one step per key press (hold to keep going, no `ENTER`); `r` new maze; `q` twice to give up |
| Level 3 – Control room | Search the room for clues, then crack the 5-letter self-destruct code, Wordle-style. 6 guesses per try; you can search again and retry. | `1`–`3`, a 5-letter word, `BACK` leaves the panel, `quit` |

**Code colours (Level 3):** green `[A]` = right letter, right spot; yellow `(A)` = in the code,
wrong spot; gray ` A ` = not in the code.

**Win:** enter the correct code in Level 3. The station explodes and the end credits roll.
**Lose:** type `quit` in any level → GAME OVER.
**Restart:** after a win or a loss the game asks `Play again? (y/n)`.

## 4. Connected puzzles

- Clearing Level 1 without hitting any prisoner gives one extra guess (7 instead of 6) on
  the Level 3 self-destruct panel.
- The clues in the Level 3 control room (the commander's log and the broken screen)
  change what the player knows on the panel: without them the panel shows no hint.
- Clearing each level is what unlocks the next part of the station.

## 5. Files

| File | What it does |
|---|---|
| `main.py` | Runs the whole game: welcome → levels → credits, game over and play again |
| `Lobby.py` | Welcome screen and how-to-play page |
| `LV1.py` | Level 1: blaster range (depth-first search for the `hint` command) |
| `LV2.py` | Level 2: random maze (depth-first search maze generation) |
| `LV3.py` | Level 3: control room, Wordle-style code panel, ending |
| `Endcredit.py` | Scrolling end credits |
| `screen.py` | Shared screen code: colours, 80 × 24 check and pause |
| `ai_use.md` | Generative AI disclosure log |
| `ACKNOWLEDGEMENTS.md` | Sources, inspirations and borrowed ideas |

Every level has a `play()` function that returns `True` if the player cleared it and
`False` if they gave up, so `main.py` can chain them.

## 6. Design choices (short)

- **Nested lists:** the Level 1 range and the Level 2 maze are lists of lists
  (`grid[row][col]`); Level 3 keeps guesses as `(word, result)` pairs.
- **Level 1 hint:** a depth-first search tries every shot that hits a trooper and no
  prisoner, then searches again from the new grid, until the grid is clear or the shots
  run out. The tests use the same search to prove each round's shot limit is the smallest
  that works.
- **Maze generation:** randomised depth-first search with a stack. Every cell is visited,
  so the exit can always be reached.
- **Wordle scoring:** two passes. Greens first; the remaining answer letters are counted and
  yellows are only given while that count lasts, so `EEEEE` vs `OMEGA` shows one green and
  no yellows.
- **80 × 24 screen:** every screen goes through `screen.show()`, which clears the screen,
  prints at most 22 lines and puts the prompt on row 23, so `ENTER` never scrolls.
- **Small window:** before every screen, `screen.wait_for_size()` checks the terminal size.
  If it is under 80 × 24 it shows a one-line message (cut to fit the window) and waits.

## 7. Invalid actions and boundary cases

A wrong action is explained on screen and the player stays where they were.

| Where | Invalid action / boundary case | What the game does |
|---|---|---|
| Any prompt | `Ctrl+C` / `Ctrl+D` | Leaves cleanly with "Thanks for playing!" |
| Any screen | Window smaller than 80 × 24, down to 1 × 1 | Pauses with a message that fits, carries on when enlarged |
| Level 1 | `zzz`, `r9`, empty, a door with nothing in it | Message, no shot used |
| Level 1 | Last shot used with troopers left | ROUND FAILED, round restarts |
| Level 2 | Any other key | "That key does nothing", no move |
| Level 2 | Walking into a wall | Stays put, "Bump! That's a wall." |
| Level 2 | `q` pressed by mistake | Asks first; only a second `q` gives up |
| Level 3 room | Empty input, `9`, `hello` | Says it is not an option |
| Level 3 panel | Empty, 4 or 6 letters, digits, `É`, same code twice | Says what is wrong, no guess used |
| Level 3 panel | Panel opened before finding clues | `BACK` leaves without losing |
| Play again? | `maybe`, empty | Asked again; accepts `y`/`yes`/`n`/`no` |

## 8. Testing

### Manual tests (in a fresh `engg1330-project:2026-v03` container)

| # | Test | Expected | Result |
|---|---|---|---|
| 1 | Full normal playthrough | Reaches the ending and credits | Pass |
| 2 | Level 1: shoot a prisoner | ROUND FAILED, round restarts, no bonus at the end | Pass |
| 3 | Level 1: type `hint` | Shows a safe shot | Pass |
| 4 | Level 2: hold an arrow key, walk into a wall, press `x`, press `q` once | Moves step by step, messages, no crash, `q` only asks | Pass |
| 5 | Level 3: `ab`, `12345`, empty, same code twice | Message, no guess used | Pass |
| 6 | Level 3: use all guesses wrong | Alarm message, back in the room, can retry | Pass |
| 7 | Type `quit` in a level, then `y` | GAME OVER, then game restarts | Pass |
| 8 | Start in a window smaller than 80 × 24, then enlarge | Pause message, game carries on | Pass |
| 9 | `Ctrl+C` / `Ctrl+D` at a prompt | "Thanks for playing!", no traceback | Pass |

## 9. Known limitations

- The size is checked before each screen is drawn. If the window is made smaller while
  the player is typing, the pause comes after `ENTER`.
- A very long typed answer (over one line) can wrap. Normal answers are a few characters.
- On Windows the maze takes typed `w a s d` + `ENTER` instead of arrow keys. The course
  container (Linux) uses arrow keys.
- Level 3 never ends in a loss: after the last wrong guess the player can search the room
  and retry. This is on purpose so the final puzzle cannot block the ending.
- Colours use ANSI escape codes; very old terminals may show raw codes.

## 10. Contributions

| Member | Contributions |
|---|---|
| Khanthithao Krittichok (Peak) | [TODO check] Level 1 (owner); joined all files into `main.py`; how-to-play rules; Level 3 ending; game plan document; README, tests |
| Sutowo Antonio | [TODO check] Level 2 maze |
| Leung Ho Long Ryan | [TODO] e.g. stealth event idea (`Stealth.py`, later cut because the brief rules out real-time controls) |
| Mensah Lord Kojo Tandoh | [TODO] e.g. Level 3, welcome screen art, end credits, videos |

Everyone: planning on the team Excalidraw board, playtesting, checking the final
submission. [TODO edit to match what actually happened.]

## 11. Sources and acknowledgements

See `ACKNOWLEDGEMENTS.md` (sources and inspirations) and `ai_use.md` (generative AI use).
