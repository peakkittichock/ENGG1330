# Acknowledgements

All code was written for this project by the group, with help from generative AI as
disclosed in `ai_use.md`. No outside code files, libraries or assets were copied in.
The game uses only the Python standard library.

Built-in functions. (n.d.). Python Documentation. https://docs.python.org/3/builtins/functions.html#enumerate

Claude. (2026). Claude. https://claude.com/

Ctypes — A foreign function library for python — Python 3.9.5 documentation. (n.d.). Docs.Python.Org. https://docs.python.org/3/library/ctypes.html

GeeksforGeeks. (2026, October 17). Breadth first search or BFS for a graph. GeeksforGeeks. https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/

GeeksforGeeks. (2026b, October 25). Dijkstra’s algorithm. GeeksforGeeks. https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/

Google. (2025). Gemini. Gemini.Google.Com; Google. https://gemini.google.com/app

io — Core tools for working with streams. (n.d.). Python Documentation. https://docs.python.org/3/library/io.html

javidx9. (n.d.). Programming mazes [Video]. YouTube. https://www.youtube.com/watch?v=Y37-gB83HKE

JimShapedCoding. (2020, November 8). Python OS module | the best functions. YouTube. https://www.youtube.com/watch?v=mQppXRN841w

Lawrence, J. (2022, March 1). Why Most Wordle Clones are Wrong! DEV Community. https://dev.to/denvercoder1/why-most-wordle-clones-are-wrong-390c

Maranan, M. (2023, July 6). How to make a maze game in python - the python code. Thepythoncode.Com. https://thepythoncode.com/article/build-a-maze-game-in-python

MSVCRT — Useful routines from the MS VC++ runtime. (2024). Python Documentation. https://docs.python.org/3/library/msvcrt.html

Nicholas Britell - Topic. (2022, October 20). Pilgrim [Video]. YouTube. https://youtu.be/lyKYUivIUlE

OpenAI. (2025, September 12). ChatGPT. Chatgpt.Com; OpenAI. https://chatgpt.com

os — Miscellaneous operating system interfaces. (n.d.). Python Documentation. https://docs.python.org/3/library/os.html#os.get_terminal_size

Pymaze. (2015, January 3). PyPI. https://pypi.org/project/pymaze/

Python collections Module. (n.d.).

Python. (2010). SYS — System-specific parameters and functions — Python 3.7.3 documentation. Python.Org. https://docs.python.org/3/library/sys.html

Real Python. (n.d.). MSVCRT. Real Python. https://realpython.com/ref/stdlib/msvcrt/

Select — Waiting for I/O completion — Python 3.10.4 documentation. (n.d.). Docs.Python.Org. https://docs.python.org/3/library/select.html

shutil — High-level file operations. (n.d.). Python Documentation. https://docs.python.org/3/library/shutil.html

sys — System-specific parameters and functions. (n.d.). Python Documentation. https://docs.python.org/3/library/sys.html

time — Time access and conversions. (n.d.). Python Documentation. https://docs.python.org/3/library/time.html

time — Time access and conversions. (n.d.-b). Python Documentation. https://docs.python.org/3/library/time.html#time.sleep

W3Schools. (n.d.). Python collections module https://www.w3schools.com/python/ref_module_collections.asp

w3schools. (n.d.). Python OS Module. Www.W3schools.com. https://www.w3schools.com/python/module_os.asp

W3Schools. (n.d.). Python random module. Www.W3schools.Com. https://www.w3schools.com/python/module_random.asp

## Ideas and algorithms we adapted

| What | Where used | Source / note |

| Wordle guessing game (green / yellow / gray letters) | `LV3.py` code panel | Game mechanic from *Wordle* by Josh Wardle (now The New York Times). We only reuse the idea; our word, clues, scoring code and display are our own. |
| Recursive backtracker (randomised depth-first search) maze generation | `LV2.py` `carve_maze()` | Standard algorithm |
| Depth-first search for a safe plan of shots | `LV1.py` `find_plan()` | Standard search algorithm taught in python websites and youtube videos. |
| Story, all screens | Inspired by *Star Wars* (Lucasfilm). Some *Star Wars* words are used as fan references: stormtrooper, Empire, Rebel, X-wing, Death Star, lightsaber, and the Level 3 code `KYBER` (kyber crystal). The game title, the station name DEATH STAR, the story; no *Star Wars* images, sounds or text were copied. |
| ANSI escape codes for colour and cursor movement | All screens | Standard terminal codes (ECMA-48 / "ANSI escape code" on Wikipedia). |

## Generative AI

Claude Code (Anthropic), OpenAI GPT-Sol6.1, and Gemini were used for planning, code, debugging and documentation.