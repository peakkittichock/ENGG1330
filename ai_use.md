# AI Use
Generative AI used: Yes

Each entry below is a substantive use of generative AI. Every member who used AI adds their
own entries. Full chat transcripts are kept by the member and can be shown to the teaching
team on request.

## Entry 1
- Member and date: Khanthithao Krittichok (Peak), 2026-11-11
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Merge a teammate's Level 1 (`stage1_blaster.py`) into the project and connect it
  to `main.py` (the Level 1 bonus gives one extra guess in Level 3).
- Substantial parts affected (files/materials): `LV1.py`, `main.py`, `LV3.py`
- What was kept, changed, or rejected, and how results were checked: Kept the teammate's
  game idea (3 x 3 grid, troopers, armored troopers, prisoners, row/column/door shots).
  Rounds were changed so each one can be solved with exactly its number of shots; this was
  checked with the `find_plan()` search and by playing all 3 rounds by hand.

## Entry 2
- Member and date: Khanthithao Krittichok (Peak), 2026-11-11
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Review all the code and make it simpler: shorter functions, fewer features,
  removal of long comments and docstrings.
- Substantial parts affected (files/materials): all `.py` files, `README.md`,
  `GAME_PLAN.md`, `ACKNOWLEDGEMENTS.md`
- What was kept, changed, or rejected, and how results were checked: Kept the story, the
  three levels and the end credits. `screen.py` was cut down to one 80 x 24 check with a
  resize message. The first stealth event was removed here (it was brought back later, see
  Entry 4). Checked by playing the whole game in the course container (README manual tests
  1-9).

## Entry 3
- Member and date: Khanthithao Krittichok (Peak), 2026-11-11
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Let the Level 2 maze be played with the arrow keys (hold a key to keep moving)
  instead of typing `w a s d` + `ENTER` each time.
- Substantial parts affected (files/materials): `LV2.py`
- What was kept, changed, or rejected, and how results were checked: Kept the maze
  generator and the `w a s d` keys. Added single-key reading (`termios`, `select`) with a
  typed fallback when there is no real terminal. Checked by hand (manual test 4: hold an
  arrow key, walk into a wall, press `x`, press `q` once) and Ctrl+C / Ctrl+D (manual
  test 9).

## Entry 4
- Member and date: Khanthithao Krittichok (Peak), 2026-11-11
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Bring back Ryan's stealth event with its timer, without the bug where a late key
  press leaked into the next level.
- Substantial parts affected (files/materials): `Stealth.py`, `main.py`, `Lobby.py`
- What was kept, changed, or rejected, and how results were checked: Kept Ryan's idea, the
  random hide letter, the shrinking `====` bar and his messages. The `Thread` + `input()`
  timer was replaced by reading one key at a time. A turn-based version (no timer) was
  suggested by the AI but rejected by the team, who chose to keep the timer. Checked by
  pressing the right key, a wrong key and no key.

## Entry 5
- Member and date: Khanthithao Krittichok (Peak), 2026-11-11
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Drafts of the documentation, and adding the group number, subclass and member
  names to the end credits.
- Substantial parts affected (files/materials): `README.md`, `ACKNOWLEDGEMENTS.md`,
  `GAME_PLAN.md`, `Endcredit.py`, this file
- What was kept, changed, or rejected, and how results were checked: The group filled in
  the group number, names, subclass, playtime and manual test results, and checked every
  section against the game. An automated test file (`test_game.py`) was written with AI
  and later removed by the team; testing is the manual test table in the README.

## Entry 6
- Member and date: Khanthithao Krittichok (Peak), 2026-11-14
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Merge the teammate's final Stage 1 (`stage1_blaster.py`) into `LV1.py`.
- Substantial parts affected (files/materials): `LV1.py`, `README.md`, `GAME_PLAN.md`
- What was kept, changed, or rejected, and how results were checked: Kept the teammate's
  new rules: 4 rounds, conveyor belt rows, a limit of 2 prisoner hits per round, and the
  `reset` and `help` commands. Kept the IRONWAKE story (troopers and prisoners) instead of
  the teammate's story text, and kept the shared `screen.py` and the `play()` contract used
  by `main.py`. Checked with `find_plan()` that each round can be cleared with exactly its
  number of shots and not with one fewer, and by playing through Level 1.

## Entry 7
- Member and date: Khanthithao Krittichok (Peak), 2026-11-09
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Set up the first version of the project (initial commit): `main.py` linking the
  levels, `screen.py`, `Lobby.py`, `Endcredit.py`, first versions of `LV1.py`-`LV3.py`,
  and the docs. [CHECK: remove any file the AI did not help with]
- Substantial parts affected (files/materials): `main.py`, `screen.py`, `Lobby.py`,
  `Endcredit.py`, `LV1.py`, `LV2.py`, `LV3.py`, `README.md`, `GAME_PLAN.md`,
  `ACKNOWLEDGEMENTS.md`
- What was kept, changed, or rejected, and how results were checked: Kept the team's story
  (IRONWAKE escape) and the three-level plan. Most of this first version was later
  simplified or replaced (see Entries 1-4). [CHECK: add anything you rejected] Checked by
  running `python3 main.py` and playing through.

## Entry 8
- Member and date: Khanthithao Krittichok (Peak), 2026-11-14
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Merge Antonio's updated Level 2 maze into `LV2.py` and link its hint to Level 3.
- Substantial parts affected (files/materials): `LV2.py`, `LV3.py`, `main.py`,
  `README.md`, `GAME_PLAN.md`
- What was kept, changed, or rejected, and how results were checked: Kept Antonio's maze
  (recursive backtracker, at least 12 dead ends, 45-second clock, BFS par, hint `○`).
  Added `LV2.found_hint`, passed by `main.py` to Level 3, where it shows `_ _ _ G _`; the
  broken-screen option in Level 3 was removed because the hint replaces it. Checked by
  playing Level 2 with and without the hint and by letting the clock run out (manual
  tests 2 and 4 still to retest).

## Entry 9
- Member and date: Khanthithao Krittichok (Peak), 2026-11-14 [CHECK date]
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Find bugs in the game: ask the AI to read the code, point out crashes, wrong
  input handling and places where the levels did not connect correctly.
- Substantial parts affected (files/materials): `main.py`, `LV1.py`, `LV2.py`, `LV3.py`,
  `Stealth.py`, `screen.py` [CHECK: keep only files that had bugs]
- What was kept, changed, or rejected, and how results were checked: Bugs found and fixed:
  [CHECK: list each one, e.g. a late key press in the stealth event leaking into the next
  level (fixed in Entry 4)]. Bug reports that turned out to be wrong were rejected after
  testing them by hand. Each fix was checked by repeating the steps that caused the bug
  and by running the README manual tests.

## Entry 10
- Member and date: [TODO: each teammate who used AI (e.g. for `stage1_blaster.py`,
  `Stealth.py`, Antonio's `LV2.py`, story or ASCII art), with date]
- Tool and model/version: [TODO]
- Purpose: [TODO]
- Substantial parts affected (files/materials): [TODO]
- What was kept, changed, or rejected, and how results were checked: [TODO]
