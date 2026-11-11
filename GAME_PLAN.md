# GAME_PLAN.md — Galaxy Escape (ENGG1330 group project)

Source: team Excalidraw board (decoded 2026-11-08) + current code in this folder.
Read this before touching any level so changes fit the plan.

## 1. What the game is

Terminal text adventure in pure Python 3 (standard library only, no pip installs).
Fits an 80x24 terminal; uses ANSI colour codes and `input()`.

Space-opera escape story (board brainstormed it as a Star Wars theme; the code uses
original names: **GALAXY ESCAPE**, station **IRONWAKE**. Keep original names in code
and text, use the space-opera vibe, do not copy franchise names/characters/art).

Story: player is a captured rebel/knight held on an enemy space station. They slip
away from the guards and must escape through 3 levels, reach a starfighter, and blow
the station up on the way out.

## 2. Flow

```
Welcome page -> How to play (rules, story) -> Level 1 -> Level 2 -> Level 3 -> End credits
                                              fail at any level => GAME OVER, "Play again? (y/n)"
```

`main.py` drives this (`play_once()`), so every level follows one contract:

| File | Entry function | Returns |
|---|---|---|
| `Lobby.py` | `run()` | nothing (welcome + how-to-play) |
| `LV1.py` | `play()` | `True` cleared / `False` quit; sets `LV1.earned_bonus` |
| `LV2.py` | `play()` | `True` / `False` |
| `LV3.py` | `play(extra_guesses=0)` | `True` escaped / `False` |
| `Endcredit.py` | `play_credits()` | nothing |

Do not break these names or return values. Each level file may also run standalone
(`if __name__ == "__main__":`).

## 3. Screens and levels (from the board)

### Welcome page (`Lobby.py`)
- Big title art + tagline. "Welcome, traveller... you are stuck on the station and must find a way out."
- "Press ENTER to start".
- How-to-play pages: explain rules in-theme, e.g. "You are a surviving knight captured
  and sent to the station for questioning. You slipped away from the guards, now escape
  and destroy the station."

### Level 1 — The blaster range (owner: Peak)
- "SHOOT THE ENEMY, not the ally": 3 x 3 grid of doors with troopers and prisoners.
  A bolt hits a row, a column or one door; armored troopers need 2 hits; few shots per round.
- 3 rounds. Hitting a prisoner or running out of shots restarts the round. `hint` uses a
  depth-first search. No prisoner hit = one extra guess in Level 3.
- **Status: built** in `LV1.py`.

### Level 2 — Through the shadows: maze (owner: Antonio)
- Imperial alarms sound; player enters the station's maintenance tunnels.
  Security droids patrol, laser barriers block paths.
- Objective: find the right path to the central control room (enter different rooms).
- **Status: built** in `LV2.py`: random 2D maze (recursive backtracker), arrow keys / `w a s d`,
  one step per key press (no timer, so still turn based). Par count and dead-end check were cut.

### Level 3 — Wordle: self-destruct code
- Player is in the control room. Find the self-destruct secret code and type it into
  the control panel; the station explodes; get into the starfighter in time to escape.
- Code: Wordle-style 5-letter guess, green/yellow/gray tiles, `MAX_GUESSES = 6`,
  answer `CODE = "OMEGA"`. Clues in room: commander's log ("last letter of the Greek
  alphabet") and broken screen (`_ _ _ G _`).
- Ending: 3-2-1 countdown, BOOM, "MISSION COMPLETE".
- **Status: built** — `score_guess()` does real Wordle scoring (greens first, then
  yellows by remaining count); covered by `test_game.py`.

### End credits (`Endcredit.py`)
- Station explodes, scrolling credits with team names. Only shown when player escapes.

## 4. Ideas on the board (not committed)

- **Final boss / station health**: station has HP; player types as many space-saga
  related words as possible in a time limit; ASCII station visibly breaks apart as HP drops.
  Hand out a "knowledge kit" word list to players. ("Warp to battleship" step before final.)
- **Random stealth event** between events: a guard walks close; player must press a
  random letter quickly to hide.
  ```python
  hideletter = random.choice("abcdefghijklmnopqrstuvwxyz")
  if random.random() < 0.5:
      print(f"A guard is coming close, PRESS {hideletter} to escape!")
      if input() == hideletter:
          print("The guard walked away without noticing you, you can proceed")
      else:
          print("You got caught")
  ```
  Open problem: countdown/timeout on `input()` (stdlib options: `select` on Unix, or
  measure `time.time()` before/after input and fail if too slow — simplest, cross-platform).
- Team decision: **finish all 3 levels first, extras after.** Set deadlines per level.

## 5. TODO

- [x] Build real Level 1 (blaster range).
- [x] Implement `score_guess()` in `LV3.py` (Wordle scoring).
- [x] Drafts: `README.md`, `ACKNOWLEDGEMENTS.md`, `ai_use.md`, `test_game.py` (33 tests).
  Team must fill every `[TODO]` (names, group no., contributions, manual test results).
- [x] Stealth event: built, then **cut** (`Stealth.py` removed). Its 2.5 s timer is a
  real-time control, which the brief rules out.
- [ ] Optional: station-HP typing boss, maze theme decorations.
- [ ] Agree deadlines for each level.

## 6. Rules for anyone (incl. Claude) editing code

- Standard library only; must run with `python3 main.py`.
- Keep every screen within 80x24: draw screens with `screen.show(lines, prompt)`
  (at most 22 lines of at most 79 characters).
- Keep the level contract in section 2.
- Beginner-readable code (course project): simple functions, comments, no clever tricks.

## 7. Course constraints (see `project_brief.md`, `Submission_Guidelines.md`)

- Deadline **Mon 16 Nov 2026 23:59**. Game show 30 Nov.
- Single-player, **turn-based**, 5–10 min playthrough, ≥2 connected puzzles, instructions,
  clear win condition, restart. **Real-time controls are out of scope** — so the timed
  stealth event and timed typing boss in section 4 conflict with the brief (stealth was
  cut). LV2 moves one step per key press (arrow keys / w a s d), no timer.
- Must run in container `engg1330-project:2026-v03`, stdlib + starter packages only.
- If terminal < 80x24: pause and show a resize message that fits the space. Done:
  `screen.wait_for_size()`.
- ZIP must include `README`, acknowledgements, `ai_use.md` (AI was used, so log entries needed).
- Extras/ASCII art don't raise the grade; robustness (invalid/boundary input) and
  readability/docs (20%) do.
