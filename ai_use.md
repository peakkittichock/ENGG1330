# AI Use
Generative AI used: Yes

> **TODO before submitting:** every member must add their own entries (any AI tool, any
> part: design, code, debugging, docs, videos), check the entries below, and replace each
> `[TODO]`. Then delete this note.

## Entry 1
- Member and date: Peak, 2026-11-08
- Tool and model/version: Claude Code, Claude Opus 5.5 (`claude-opus-5-5`)
- Purpose: Turn the team's Excalidraw planning board into a written game plan, and
  convert the project brief and submission guidelines PDFs into Markdown so the plan
  could be checked against the course rules.
- Substantial parts affected (files/materials): `GAME_PLAN.md` (planning document, not
  part of the game); Markdown copies of the brief and guidelines.
- What was kept, changed, or rejected, and how results were checked: Kept as the team's
  plan. Checked the plan against the board and the original PDFs.
  [TODO: anything the team changed or rejected.]

## Entry 2
- Member and date: Peak, 2026-11-08
- Tool and model/version: Claude Code, Claude Opus 5.5
- Purpose: Join the separate level files into one game (lobby → level 1 → level 2 →
  level 3 → end credits) with game over and "play again"; add a temporary Level 1 so the
  full game could run before the real Level 1 was finished.
- Substantial parts affected (files/materials): `main.py` (new), `LV1.py` (placeholder),
  small changes so each level returns `True`/`False`.
- What was kept, changed, or rejected, and how results were checked: Kept the
  one-contract design (each level returns True/False). Played the whole game through in
  the terminal to check every transition. The placeholder Level 1 is replaced by our own
  level [TODO when done]. Later covered by automated tests in `test_game.py`
  (`TestMainFlow`).

## Entry 3
- Member and date: Peak, 2026-11-08
- Tool and model/version: Claude Code, Claude Opus 5.5
- Purpose: Rewrite the how-to-play pages to match the changed game, and animate the
  Level 3 ending (ship flies away, station explodes) at a readable speed.
- Substantial parts affected (files/materials): `Lobby.py` (`PAGES`, page drawing),
  `LV3.py` (`ending()`, `draw_scene()`, frame art).
- What was kept, changed, or rejected, and how results were checked: Read every page in
  an 80 × 24 terminal to check nothing wraps or scrolls. Asked for the animation to be
  slowed down after the first version was too fast (`FRAME_DELAY`, `BOOM_DELAY`).
  Automated tests check that all pages and frames fit the screen.
  [TODO: what we changed by hand.]

## Entry 4
- Member and date: [TODO teammate name] (on Peak's laptop), 2026-11-09
- Tool and model/version: Claude Code, Claude Opus 5.5
- Purpose: Our teammate wrote a first version of the stealth quick-time event using a
  thread for the timer, and asked the AI to make it work reliably between levels.
- Substantial parts affected (files/materials): `Stealth.py`; two calls in `main.py`.
- What was kept, changed, or rejected, and how results were checked: Kept the
  teammate's idea (guard warning, random letter, press it in time). Changed: (1) the
  thread was removed, because after a timeout the thread still waiting on `input()`
  swallowed the player's next line (e.g. the ENTER for the next level); it now reads
  one key with `select` (macOS/Linux) or `msvcrt` (Windows); (2) the letter was picked
  once at import, so it was the same all game; it is now picked each time; (3) keys
  pressed before the bar appears are thrown away. Tested in a real terminal: right key,
  wrong key, ENTER, and waiting too long. We noticed the timer may count as "real-time
  controls", which the brief excludes, so we [TODO: decision after asking the STA].

## Entry 5
- Member and date: Peak, 2026-11-09
- Tool and model/version: Claude Code, Claude Opus 5.5
- Purpose: Check what was still missing before the deadline; draft the README,
  acknowledgements and this log; write automated tests; make the game pause (instead of
  quitting) when the window is smaller than 80 × 24, as the brief requires.
- Substantial parts affected (files/materials): `README.md`, `ACKNOWLEDGEMENTS.md`,
  `ai_use.md`, `test_game.py`, `screen.py` (new); one-line size checks added to
  `main.py`, `Lobby.py`, `LV1.py`, `LV2.py`, `LV3.py`, `Stealth.py`, `Endcredit.py`.
  Level 2 used to exit the whole game on a small window; now it pauses.
- What was kept, changed, or rejected, and how results were checked: Ran
  `python3 -m unittest -v test_game.py` (39 tests pass). Ran the game in a simulated
  terminal and resized it: starting at 60x20, shrinking to 40x10 on the how-to-play page
  and to 70x20 in the middle of the maze all showed the pause message, and enlarging
  the window carried on from the same place. That test found a bug: a key pressed while
  paused still moved the ball afterwards, so keys typed during the pause are now
  thrown away. Checked the Wordle test cases by
  working out the expected colours by hand (e.g. `EEEEE` vs `OMEGA` must give only one
  green and no yellows). The team filled in names, contributions and manual test results
  in the README themselves. [TODO: anything else changed.]

## Entry 6
- Member and date: [TODO Antonio, date]
- Tool and model/version: [TODO]
- Purpose: [TODO Level 2 maze — say if AI was used or delete this entry]
- Substantial parts affected (files/materials): `LV2.py`
- What was kept, changed, or rejected, and how results were checked: [TODO]

## Entry 7
- Member and date: [TODO member, date]
- Tool and model/version: [TODO]
- Purpose: [TODO e.g. Level 3 Wordle, welcome screen, end credits, videos]
- Substantial parts affected (files/materials): [TODO]
- What was kept, changed, or rejected, and how results were checked: [TODO]

## Entry 5
- Member and date: Peak, 2026-11-09
- Tool and model/version: Claude Code, Claude Opus 5.5
- Purpose: Check how the game handles invalid actions and boundary cases (marked under
  "Correctness and robustness") and improve it.
- Substantial parts affected (files/materials): `main.py` (`ask_play_again()`, Ctrl+D
  handling), `LV3.py` (`check_code()`, `BACK`, guesses-left line), `LV2.py` (footer
  messages, quit confirmation), `Lobby.py` (feedback line), `screen.py` (`ask()`), `Stealth.py` (timer pause), `test_game.py` (18 new
  tests), README section 7.
- What was kept, changed, or rejected, and how results were checked: Problems found:
  Ctrl+D crashed the game with a traceback; any answer other than `y` at "Play again?"
  quit; accented letters passed `isalpha()`; repeating a code wasted a guess; one stray
  `Q` in the maze ended the game; invalid keys gave no feedback.
  Second part (the team pointed out that resizing the terminal is the key boundary case):
  added `screen.ask()` to replace `input()`, so a resize while typing pauses at once and
  long answers cannot wrap or scroll past 80 × 24; the stealth timer now pauses on resize.
  Checked by driving the real game in a pseudo-terminal (resize mid-typing, 200 key
  presses, Ctrl+D). That test found a bug in the first version: arrow-key handling
  swallowed keys typed straight after it; fixed. All 57 tests pass.
  [TODO: play through in the container and fill in manual tests 11-13.]

