#!/usr/bin/env python3
"""
MAZE RUNNER - a 2D terminal maze game.

* Pure Python 3, standard library only (no pip installs, no curses needed).
* Fits inside an 80 x 24 terminal (the game uses 79 x 23).
* Maze is generated with the randomised depth-first search
  ("recursive backtracker") algorithm.
* Move the ball with the ARROW KEYS (WASD also works).

Run it:      python3 maze.py          (Windows: python maze.py)
ASCII mode:  python3 maze.py --ascii  (if the ball/star glyphs look wrong)

Controls:  Arrow keys / WASD = move    R = new maze    Q = quit
           (Q asks first: press Q twice to really quit)
"""

import contextlib
import os
import random
import sys
import time
from collections import deque

import screen

if os.name == "nt":
    import msvcrt
else:
    import select

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
CELLS_W, CELLS_H = 19, 10          # maze size in "cells"
GRID_W = CELLS_W * 2 + 1           # 39 tiles wide  (walls occupy tiles too)
GRID_H = CELLS_H * 2 + 1           # 21 tiles tall
TILE_W = 2                         # one tile = 2 terminal columns (looks square)
MARGIN = 1                         # blank columns on the left
SCREEN_W = MARGIN + GRID_W * TILE_W    # 79 columns used
SCREEN_H = GRID_H + 2                  # 23 rows used (title + maze + footer)
MIN_DEAD_ENDS = 12                 # regenerate if the maze has fewer dead ends

WALL, PATH = 1, 0
DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))
MOVES = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

# ---------------------------------------------------------------------------
# Look & feel (ANSI escape codes)
# ---------------------------------------------------------------------------
ENCODING = (getattr(sys.stdout, "encoding", None) or "").lower()
ASCII_ONLY = "--ascii" in sys.argv or "utf" not in ENCODING

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
CYAN = "\x1b[36m"
GREEN = "\x1b[1;32m"

if ASCII_ONLY:
    WALL_T = "\x1b[34m##" + RESET
    BALL_T = "\x1b[1;33m()" + RESET
    GOAL_T = "\x1b[1;32mEX" + RESET
    GOAL_NAME = "EX"
else:
    WALL_T = "\x1b[44m  " + RESET                 # solid blue block
    BALL_T = "\x1b[1;33m\u25cf " + RESET          # yellow ball
    GOAL_T = "\x1b[1;32m\u2605 " + RESET          # green star
    GOAL_NAME = "\u2605"
FLOOR_T = "  "
TRAIL_T = "\x1b[36m. " + RESET                    # breadcrumb where you've been

ENTER_SCREEN = "\x1b[?1049h\x1b[?25l\x1b[2J"      # alt screen, hide cursor, clear
LEAVE_SCREEN = "\x1b[0m\x1b[?25h\x1b[?1049l"      # restore everything


# ---------------------------------------------------------------------------
# Maze generation: randomised DFS / recursive backtracker
# ---------------------------------------------------------------------------
def carve_maze():
    """Return a fresh maze grid carved by randomised depth-first search.

    The grid is a list of rows; cells live on odd (row, col) coordinates and
    the tiles between them are walls that get knocked down as the DFS walks.
    The explicit stack below is the "recursive" part of the backtracker
    (no Python recursion, so there is no recursion-limit risk).
    """
    grid = [[WALL] * GRID_W for _ in range(GRID_H)]
    grid[1][1] = PATH
    stack = [(1, 1)]

    while stack:
        r, c = stack[-1]
        options = []
        for dr, dc in DIRS:
            nr, nc = r + dr * 2, c + dc * 2
            if 0 < nr < GRID_H - 1 and 0 < nc < GRID_W - 1 and grid[nr][nc] == WALL:
                options.append((dr, dc))          # unvisited neighbouring cell
        if options:
            dr, dc = random.choice(options)       # randomly pick one
            grid[r + dr][c + dc] = PATH           # knock down the wall between
            grid[r + dr * 2][c + dc * 2] = PATH   # open the new cell
            stack.append((r + dr * 2, c + dc * 2))
        else:
            stack.pop()                           # dead end -> backtrack
    return grid


def shortest_path_length(grid, start, goal):
    """Breadth-first search; returns number of steps or None if unreachable."""
    seen = {start}
    queue = deque([(start, 0)])
    while queue:
        (r, c), dist = queue.popleft()
        if (r, c) == goal:
            return dist
        for dr, dc in DIRS:
            nxt = (r + dr, c + dc)
            if grid[nxt[0]][nxt[1]] == PATH and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, dist + 1))
    return None


def count_dead_ends(grid, start, goal):
    """Count cells that have exactly one opening (excluding start and goal)."""
    total = 0
    for r in range(1, GRID_H, 2):
        for c in range(1, GRID_W, 2):
            if (r, c) in (start, goal):
                continue
            openings = sum(grid[r + dr][c + dc] == PATH for dr, dc in DIRS)
            if openings == 1:
                total += 1
    return total


def generate_maze():
    """Make a maze that has plenty of dead ends AND a guaranteed route.

    A DFS-carved maze is a spanning tree, so every cell is reachable and there
    is exactly one route between any two cells.  We still verify with a BFS
    and insist on a minimum number of dead ends before accepting the maze.
    """
    start = (1, 1)
    goal = (GRID_H - 2, GRID_W - 2)
    while True:
        grid = carve_maze()
        par = shortest_path_length(grid, start, goal)
        if par is not None and count_dead_ends(grid, start, goal) >= MIN_DEAD_ENDS:
            return grid, start, goal, par


# ---------------------------------------------------------------------------
# Keyboard input (arrow keys) - standard library only
# ---------------------------------------------------------------------------
def _plain_key(ch):
    """Map an ordinary character to a game action."""
    return {
        "w": "UP", "s": "DOWN", "a": "LEFT", "d": "RIGHT",
        "q": "QUIT", "r": "NEW", "\x03": "QUIT",
    }.get(ch.lower())


if os.name == "nt":
    def read_key():
        """Block until a key is pressed (Windows)."""
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):                 # special-key prefix
            return {"H": "UP", "P": "DOWN", "K": "LEFT", "M": "RIGHT"}.get(
                msvcrt.getwch())
        return _plain_key(ch)
else:
    def read_key():
        """Block until a key is pressed (Linux / macOS)."""
        fd = sys.stdin.fileno()
        data = os.read(fd, 1)
        if not data:                               # EOF
            return "QUIT"
        ch = data.decode("latin-1")
        if ch != "\x1b":
            return _plain_key(ch)

        # Arrow keys arrive as ESC [ A/B/C/D  (or ESC O A/B/C/D).
        if not select.select([fd], [], [], 0.1)[0]:
            return None                            # a lone ESC press
        if os.read(fd, 1) not in (b"[", b"O"):
            return None
        final = b""
        while select.select([fd], [], [], 0.1)[0]:
            byte = os.read(fd, 1)
            final = byte
            if 0x40 <= byte[0] <= 0x7E:            # end of the escape sequence
                break
        return {b"A": "UP", b"B": "DOWN", b"C": "RIGHT", b"D": "LEFT"}.get(final)


def key_ready(wait):
    """True if a key is pressed within `wait` seconds (does not read it)."""
    if os.name == "nt":
        end = time.time() + wait
        while time.time() < end:
            if msvcrt.kbhit():
                return True
            time.sleep(0.02)
        return False
    return bool(select.select([sys.stdin], [], [], wait)[0])


def next_key():
    """Wait for the next key, but keep an eye on the window size.

    Returns "RESIZE" if the window became smaller than 80 x 24 while we were
    waiting, so the game can pause straight away instead of after the next
    key press.
    """
    while not key_ready(0.25):
        if screen.too_small():
            return "RESIZE"
    return read_key()


@contextlib.contextmanager
def raw_terminal():
    """Put the terminal in single-key mode and always restore it afterwards."""
    if os.name == "nt":
        try:                                       # turn on ANSI colours
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            os.system("")
        yield
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        saved = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)                      # no echo, no Enter needed
            yield
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, saved)


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------
# Footer messages for wrong actions (each fits in one 79-column line).
HELP_LINE = " Arrow keys / WASD: move    R: new maze    Q: quit"
WALL_LINE = " Bump! That's a wall - try another way.    R: new maze    Q: quit"
UNKNOWN_LINE = " That key does nothing. Use arrow keys / WASD, R = new maze, Q = quit."
CONFIRM_QUIT_LINE = (" Really quit? The guards will catch you! "
                     "Q again = quit, any other key = stay.")


def draw(grid, pos, goal, trail, moves, solved, par, won, footer=HELP_LINE):
    lines = [f"{BOLD}{CYAN} MAZE RUNNER{RESET}   Moves: {moves}   "
             f"Mazes solved: {solved}   Find the {GOAL_NAME} (bottom-right)"]

    for r in range(GRID_H):
        row = [" " * MARGIN]
        for c in range(GRID_W):
            p = (r, c)
            if p == pos:
                row.append(BALL_T)
            elif p == goal:
                row.append(GOAL_T)
            elif grid[r][c] == WALL:
                row.append(WALL_T)
            elif p in trail:
                row.append(TRAIL_T)
            else:
                row.append(FLOOR_T)
        lines.append("".join(row))

    if won:
        lines.append(f" {GREEN}You escaped in {moves} moves "
                     f"(shortest possible: {par})!{RESET}   R: new maze   Q: quit")
    else:
        lines.append(footer)

    sys.stdout.write("\x1b[H" + "\r\n".join(line + "\x1b[K" for line in lines))
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Game loop
# ---------------------------------------------------------------------------
def play(stop_on_win=False):
    """Main maze loop. Returns True if a maze was solved, False on quit.

    stop_on_win=True (used by main.py): after the first escape, wait for a key
    and leave so the next level can start.
    """
    solved = 0
    grid, start, goal, par = generate_maze()
    pos, trail, moves, won = start, {start}, 0, False
    screen.wait_for_size()
    draw(grid, pos, goal, trail, moves, solved, par, won)

    quit_asked = False                             # True after the first Q
    while True:
        key = next_key()
        footer = HELP_LINE

        if key == "QUIT" and (quit_asked or won):  # second Q in a row: leave
            return solved > 0

        if key == "RESIZE":                        # window too small: pause,
            screen.wait_for_size()                 # then redraw everything
            footer = CONFIRM_QUIT_LINE if quit_asked else HELP_LINE

        elif key == "QUIT":                        # first Q: ask to confirm,
            quit_asked = True                      # one wrong key must not
            footer = CONFIRM_QUIT_LINE             # end the whole game

        elif key == "NEW":
            quit_asked = False
            grid, start, goal, par = generate_maze()
            pos, trail, moves, won = start, {start}, 0, False

        elif key in MOVES and not won:
            quit_asked = False
            dr, dc = MOVES[key]
            nr, nc = pos[0] + dr, pos[1] + dc
            if grid[nr][nc] == PATH:               # walls block the ball
                pos = (nr, nc)
                trail.add(pos)
                moves += 1
                if pos == goal:
                    won = True
                    solved += 1
            else:
                footer = WALL_LINE                 # bumped a wall: say so
        elif won:
            continue                               # after winning: ignore keys
        else:
            quit_asked = False                     # unknown key (or lone ESC):
            footer = UNKNOWN_LINE                  # ignore it, but say so

        draw(grid, pos, goal, trail, moves, solved, par, won, footer)

        if won and stop_on_win:
            sys.stdout.write(f"\r\n {GREEN}Press any key to continue...{RESET}")
            sys.stdout.flush()
            read_key()
            return True


def run_level():
    """Run level 2 once (used by main.py). Returns True if the maze is solved."""
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        sys.exit("Please run this game in an interactive terminal.")
    with raw_terminal():
        sys.stdout.write(ENTER_SCREEN)
        try:
            return play(stop_on_win=True)
        finally:
            sys.stdout.write(LEAVE_SCREEN)
            sys.stdout.flush()


def main():
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        sys.exit("Please run this game in an interactive terminal.")


    try:
        with raw_terminal():
            sys.stdout.write(ENTER_SCREEN)
            try:
                play()
            finally:
                sys.stdout.write(LEAVE_SCREEN)
                sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
