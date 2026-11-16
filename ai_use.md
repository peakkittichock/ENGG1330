# AI Use
Generative AI used: Yes

## Entry 1
- Member and date: Krittichok Khanthithao (Peak), 9 November, 2026 
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Set up the first version of the project (initial commit): `main.py` linking the
  levels, `screen.py`, `Lobby.py`, `Endcredit.py`, first versions of `LV1.py`-`LV3.py`,
  and the docs. [CHECK: remove any file the AI did not help with]
- Substantial parts affected (files/materials): `main.py`, `screen.py`, `Lobby.py`,
  `Endcredit.py`, `LV1.py`, `LV2.py`, `LV3.py`, `README.md`, `GAME_PLAN.md`,
  `ACKNOWLEDGEMENTS.md`
- What was kept, changed, or rejected, and how results were checked: Kept the team's story
  (DEATH STAR escape) and the three-level plan. Most of this first version was later
  simplified or replaced (see Entries 1-4). Checked by running `python3 main.py` and playing through.

## Entry 2
- Member and date: Krittichok Khanthithao (Peak), 11 November, 2026 
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Merge a teammate's Level 1 (`stage1_blaster.py`) into the project and connect it
  to `main.py` (the Level 1 bonus gives one extra guess in Level 3).
- Substantial parts affected (files/materials): `LV1.py`, `main.py`, `LV3.py`
- What was kept, changed, or rejected, and how results were checked: Kept the teammate's
  game idea (3 x 3 grid, troopers, armored troopers, prisoners, row/column/door shots).
  Rounds were changed so each one can be solved with exactly its number of shots; this was
  checked with the `find_plan()` search and by playing all 3 rounds by hand.

## Entry 3
- Member and date:  Krittichok Khanthithao (Peak), 11 November, 2026 
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

## Entry 4
- Member and date: Krittichok Khanthithao (Peak), 11 November, 2026 
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Let the Level 2 maze be played with the arrow keys (hold a key to keep moving)
  instead of typing `w a s d` + `ENTER` each time.
- Substantial parts affected (files/materials): `LV2.py`
- What was kept, changed, or rejected, and how results were checked: Kept the maze
  generator and the `w a s d` keys. Added single-key reading (`termios`, `select`) with a
  typed fallback when there is no real terminal. Checked by hand (manual test 4: hold an
  arrow key, walk into a wall, press `x`, press `q` once) and Ctrl+C / Ctrl+D (manual
  test 9).

## Entry 5
- Member and date: Krittichok Khanthithao (Peak), 11 November, 2026 
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Bring back Ryan's stealth event with its timer, without the bug where a late key
  press leaked into the next level.
- Substantial parts affected (files/materials): `Stealth.py`, `main.py`, `Lobby.py`
- What was kept, changed, or rejected, and how results were checked: Kept Ryan's idea, the
  random hide letter, the shrinking `====` bar and his messages. The `Thread` + `input()`
  timer was replaced by reading one key at a time. A turn-based version (no timer) was
  suggested by the AI but rejected by the team, who chose to keep the timer. Checked by
  pressing the right key, a wrong key and no key.

## Entry 6
- Member and date: Krittichok Khanthithao (Peak), 11 November, 2026 
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Drafts of the documentation, and adding the group number, subclass and member
  names to the end credits.
- Substantial parts affected (files/materials): `README.md`, `ACKNOWLEDGEMENTS.md`,
  `GAME_PLAN.md`, `Endcredit.py`, this file
- What was kept, changed, or rejected, and how results were checked: The group filled in
  the group number, names, subclass, playtime and manual test results, and checked every
  section against the game. An automated test file (`test_game.py`) was written with AI
  and later removed by the team; testing is the manual test table in the README.

## Entry 7
- Member and date: Krittichok Khanthithao (Peak), 14 November, 2026 
- Tool and model/version: Claude Code (Anthropic), Claude Opus 5.5
- Purpose: Merge the teammate's final Stage 1 (`stage1_blaster.py`) into `LV1.py`.
- Substantial parts affected (files/materials): `LV1.py`, `README.md`, `GAME_PLAN.md`
- What was kept, changed, or rejected, and how results were checked: Kept the teammate's
  new rules: 4 rounds, conveyor belt rows, a limit of 2 prisoner hits per round, and the
  `reset` and `help` commands. Kept the DEATH STAR story (troopers and prisoners) instead of
  the teammate's story text, and kept the shared `screen.py` and the `play()` contract used
  by `main.py`. Checked with `find_plan()` that each round can be cleared with exactly its
  number of shots and not with one fewer, and by playing through Level 1.

## Entry 8
- Member and date: Krittichok Khanthithao (Peak), 14 November, 2026 
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
- Member and date: Krittichok Khanthithao (Peak), 14 November, 2026 
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
- Member and date: Antonio Sutowo, 23 October, 2026 
- Tool and model/version, where available: gpt-6.1 sol 
- Purpose: To improve the visual appearance of the maze and make it functional for playing. 
- Relevant prompts: Improve for me the terminal appearance for the generated maze I made using the Depth-First search algorithm. And keep it to 80x24 terminal size. Make sure that I can control my yellow dot programmed previously on the maze with hashtags. 
- Files/materials affected: LV2.py 
- What we kept, changed or rejected:  The old version of the maze, which was output visually as walls full of hashtags, was not functional at all. I used gpt sol-6.1 to develop my manually built maze into a fully functional one that has a more visually pleasing layout. gpt sol-6.1 used ANSI color codes to make walls look blue in color and to display a trail left behind as the player uses WASD and arrow keys to control the yellow dot representing the player/character being played in the game’s story. 
- How we checked it; tests and corrections: I checked the functionality of the new code by testing out for errors when moving and using WASD and arrow keys at the same time to examine whether or not the maze was functioning well for the player from start to finish. The function raw_terminal() was debugged by sol gpt-6.1 to ensure that the display of the maze within the terminal was proper and correct, following the rule of keeping it within a row of 80 by column 24 size large. 



## Entry 11 
- Member and date: Antonio Sutowo, 1 November, 2026 
- Tool and model/version, where available: gpt-6.1 sol 
- Purpose: To improve the functionality of the program’s processing of the input keys “WASD” or arrow keys from the user to then connect it to the output of smoothly moving and controlling the yellow dot around the maze. To enable responsive player controls. 
- Relevant prompts: Define read_character()’s function such that it can read and DETECT real keyboard input in REAL TIME! I am emphasising on the REAL TIME part. Please ensure the code works such that it works for both Windows/Linux and MacOS operating systems, and that the WASD keys and arrow keys have equal delay reactions in terms of time for the output terminal program. 
- Files/materials affected: LV2.py 
- What we kept, changed or rejected: read_character() function changed in such a way that it can wait for keyboard input for a specified amount of time. After sol-6.1 helped improve the code, the function can now detect whether the user has pressed a key, collect the keyboard characters that are available (WASD keys or Arrow Keys on the keyboard), and most importantly return the characters to another function for processing. It also detects the operating system and uses the most appropriate method to read keypresses without requiring the Enter key. It implements a timeout so that the game can continue running even when the player does not press any key. The function returns the collected characters to read_key(), which interprets them as movement commands. 
- How we checked it; tests and corrections: I checked it by ensuring whether the function msvcrt.kbhit() detects available keyboard input and whether the loop would terminate when there is absolutely no key being pressed. The AI helped check whether the short sleep prevents unnecessary CPU usage as well. We also tested the keyboard input functions WASD and arrow keys on each of our laptops, we had different operating systems (Windows and MacOS). AI helped checked whether select.select() respects the programmed timeout and whether os.read() collects available input correctly. AI provided explanations of the logic, identified potential input-handling limitations and most importantly, helped assess whether the function was suitable for real-time keyboard controls in the maze game. 

## Entry 12 
- Member and date: Antonio Sutowo, 2 November, 2026 
- Tool and model/version, where available: gpt-6.1 sol 
- Purpose: To improve the design of the crystal / key to be collected in the maze. 
- Relevant prompts: Please improve the design of the purple orb in the maze to a diamond shaped crystal. Help design for the displayed output of the crystal after winning the maze as well. 
- Files/materials affected: LV2.py 
- What we kept, changed or rejected: What changed was the design of the key which gives a hint for the players to the next level of the game. Initially, the design of the key was just a purple circle, which makes it look like a purple orb. To make the key more integrated with the Star Wars storyline, I changed it to a crystal to make it look more related to a Kyber Crystal, with “Kyber” actually being the Wordle word at the end of the level to successfully self-destruct the death star and win the game. Gpt-sol 6.1 provided the design of the crystal, changing it from an orb to a digitally, visually pleasing purple crystal. 
- How we checked it; tests and corrections: I tested the functionality of this design by playing multiple games of the maze repeatedly and collecting the key/crystal every single time I played a game, to ensure that the maze game itself was still able to be continued and played. I tested by trying to reach the star to finish the game and see the displayed output after collecting the crystal. 


## Entry 13 
- Member and date: Antonio Sutowo, 2 November, 2026 
- Tool and model/version, where available: gpt-6.1 sol 
- Purpose: To help debug the frequent problems of yellow dot being able to destroy the walls of the maze after collecting the updated crystal design. 
- Relevant prompts: Fix this file such that the maze game doesn’t break when the yellow dot collects the crystal and when the crystal disappears. It appears as though the yellow dot does not recognise the walls of the maze and instead breaks the maze within the terminal after collecting the crystal. 
- Files/materials affected: LV2.py 
- What we kept, changed or rejected:  AI debugged the rules of DFS, checking the condition grid[nr][nc] != PATH, to prevent the player from moving into a wall. The detection is stronger now and the problem of collecting the crystal has been resolved, such that functions of moving and controlling the yellow dot using WASD and/or arrow keys through the path of the maze functions normally even after collecting the crystal.
- How we checked it; tests and corrections: I did a final test by going through the maze game again and testing whether any bugs occur within the terminal after collecting the crystal that is randomly generated in the maze. I tested it by playing the yellow dot around the maze, deliberately moving the yellow dot toward walls and dead-ends to test whether or not the program can successfully detect walls and not destroy it into open paths.  


## Entry 14 
- Member and date: Antonio Sutowo, 3 November, 2026 
- Tool and model/version, where available: gpt-6.1 sol 
- Purpose: To ensure that the game pauses when the terminal is too small (when it reaches below the size of 80x24). 
- Relevant prompts: Please ensure that the game (especially the countdown) pauses when the terminal gets too small. Make sure that it always outputs a message telling the user to resize the window terminal to at least 80x24 to continue playing. 
- Files/materials affected: LV2.py 
- What we kept, changed or rejected: What was changed was the addition of a statement and a set of rules to check the terminal size. The program uses an imported screen module to manage terminal display behaviour. The screen.wait_while_paused() function is called during the gameplay, and the code documentation would indicate that the countdown timer always pauses when the terminal becomes too small. 
- How we checked it; tests and corrections: The maze dimensions are calculated using GRID_W, GRID_H, and TILE_W to ensure that the game fits within the required display area. I tested it by constantly reducing the size of the terminal to below 80x24 to see if the output message is sent and if the countdown is correctly stopped if the terminal is not within the size. 


## Entry 15 
- Member:  Lord Kojo Tandoh Mensah
 - Date: October 31, 2026
 - Tool and model/version: Claude

- Purpose: AI assistance in designing and implementing the recursive backtracking searching algorithm(find_plan) to power the automated in-game hint feature.
 - Files/materials affected: find_plan function, grid deep-copying logic, and the hint command handler.
- What was kept, changed or rejected, and how you checked it (tests or corrections):
Kept: The core recursive traversal and state-simulation structure (simulating shots and conveyor belt slides on cloned grid copies).
Checked: Verified correctness by testing the hint command across all levels to ensure it accurately returns safe, winning move sequences without suggesting illegal moves or friendly fire.
Changed/Enhanced: Integrated it directly with the hint command handler in play_round() to dynamically translate coordinate steps into player-readable names ( “row 1” or “door 5” ).

## Entry 16 
- Member: Lord Kojo Tandoh Mensah
 - Date: 5 November, 2026
 - Tool and model/version: Claude Sonnet 5.5
- Purpose: AI assistance in developing the multi-line ASCII sprite mapping, coordinate math, and terminal grid layout engine (board_lines).
 - Files/materials affected: board_lines, SPRITES definitions, paint, and round_screen.
- What was kept, changed or rejected, and how you checked it (tests or corrections):
Kept: The multi-line string construction, SPRITES dictionary mappings, and dynamic index calculations (r * 3 + c + 1).
Changed/Enhanced: Updated the conveyor belt rendering logic (r in belts) to dynamically display arrow indicators (>) and explanatory text showing wrap-around behavior ( “ door %d wraps to door %d” ). 
Checked: Results were checked visually by running the game in an 80 * 24 terminal window to ensure sprites, borders, and conveyor indicators (>>) aligned correctly without breaking formatting.


## Entry 17 
- Member: Lord Kojo Tandoh Mensah
- Date: 10 November, 2026
 - Tool and model/version: Claude Sonnet 5.5
- Purpose: AI assistance in developing robust terminal dimension polling, state-change tracking, and dynamic text wrapping via the external screen module.
- Files/materials affected: External screen module integration and resize handling.
- What was kept, changed or rejected, and how you checked it (tests or corrections):
Kept: The polling loop structure using shutil.get_terminal_size (), time.sleep(), and text-slicing logic for smooth resizing prompts.
Changed: Refactored this logic out of the main script to an external screen module to keep the codebase modular.
Checked: Results were checked by manually resizing the terminal window smaller and larger during execution to ensure it pauses and resumes correctly without flickering or infinite loops.

## Entry 18 
- Member: Lord Kojo Tandoh Mensah
- Date: 13 November, 2026
 - Tool and model/version: Claude Sonnet 5.5
- Purpose: AI assistance in writing defensive, flexible user input sanitization that handles whitespace, case insensitivity, shorthand expansion, and grid boundary checks.
- Files/materials affected: parse_move function
- What was kept, changed or rejected, and how you checked it (tests or corrections):
Kept: The shorthand conversion logic (turning bare numbers like “5” into “d5” ), lowercase normalization, and column/row range checks (text[1] > “3” ).
Checked: Verified by testing a wide range of edge-case inputs (mixed casing, extra spaces, out-of-bounds numbers like r4, and invalid syntax) to ensure errors are handled gracefully.

## Entry 19
- Member: Leung Ho Long Ryan 
-Date: 8 November, 2026
-Tool and model /version: Gemini
-Purpose:
To generate a first draft for the quicktime event, it is for reference only and is now completely rewritten by Peak
- What was kept, changed or rejected, and how you checked it (tests or corrections):
Nothing from the generated code was kept, the thread with input logic was replaced by key-by-key checking instead for more stable and better performance.
- Files/materials affected: Stealth.py