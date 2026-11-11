# Acknowledgements

All code was written for this project by the group, with help from generative AI as
disclosed in `ai_use.md`. No outside code files, libraries or assets were copied in.
The game uses only the Python standard library.

## Ideas and algorithms we adapted

| What | Where used | Source / note |
|---|---|---|
| Wordle guessing game (green / yellow / gray letters) | `LV3.py` code panel | Game mechanic from *Wordle* by Josh Wardle (now The New York Times). We only reuse the idea; our word, clues, scoring code and display are our own. |
| Recursive backtracker (randomised depth-first search) maze generation | `LV2.py` `carve_maze()` | Standard algorithm, e.g. Wikipedia, "Maze generation algorithm". |
| Depth-first search for a safe plan of shots | `LV1.py` `find_plan()` | Standard search algorithm taught in introductory programming courses. |
| Space-opera setting (captured hero, battle station, escape by starfighter) | Story, all screens | General genre inspiration. All names (GALAXY ESCAPE, IRONWAKE) and all ASCII art are our own; no franchise names, characters or art are used. |
| ANSI escape codes for colour and cursor movement | All screens | Standard terminal codes (ECMA-48 / "ANSI escape code" on Wikipedia). |
| [TODO if true] Title lettering style | `Lobby.py` `TITLE` | [TODO: say if the big letters were typed by hand or made with a FIGlet-style generator, and which font.] |

## People

- [TODO] STA / classmates who play-tested and gave feedback.

## Generative AI

Claude Code (Anthropic) was used for planning, code, debugging and documentation.
Details, and how we checked the results, are in `ai_use.md`.
