import contextlib
import math
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

# Settings
CELLS_W, CELLS_H = 19, 10
GRID_W, GRID_H = CELLS_W * 2 + 1, CELLS_H * 2 + 1
TILE_W, MARGIN = 2, 1
TIME_LIMIT, MIN_DEAD_ENDS = 45, 12
WALL, PATH = 1, 0
DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))
KEY_MOVES = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
# Arrow keys arrive as short codes: "\x1b[A" on Mac/Linux, "\xe0H" on Windows.
# read_moves() swaps each code for the matching WASD letter.
ARROW_KEYS = {"\x1b[A": "w", "\x1b[B": "s", "\x1b[D": "a", "\x1b[C": "d",
              "\xe0H": "w", "\xe0P": "s", "\xe0K": "a", "\xe0M": "d"}
HINT_MESSAGE = "You found a crystal! You gain one LETTER for the next stage of the game"

# Terminal appearance
RESET, BOLD, GREEN, YELLOW = "\x1b[0m", "\x1b[1m", "\x1b[1;32m", "\x1b[93m"
ENCODING = (getattr(sys.stdout, "encoding", None) or "").lower()
ASCII_ONLY = "--ascii" in sys.argv or "utf" not in ENCODING
if ASCII_ONLY:
    WALL_T = "\x1b[34m##" + RESET
    BALL_T = "\x1b[1;33m()" + RESET
    HINT_T, HINT_NAME = "\x1b[1;35m<>" + RESET, "<>"
    GOAL_T, GOAL_NAME = "\x1b[1;32mEX" + RESET, "EX"
else:
    WALL_T = "\x1b[44m  " + RESET
    BALL_T = "\x1b[1;33m● " + RESET
    HINT_T, HINT_NAME = "\x1b[1;35m◆ " + RESET, "◆"
    GOAL_T, GOAL_NAME = "\x1b[1;32m★ " + RESET, "★"
FLOOR_T, TRAIL_T = "  ", "\x1b[36m. " + RESET
MAGENTA = "\x1b[1;35m"
CRYSTAL_ART = ["      /\\",
               "     /  \\",
               "    | /\\ |",
               "    | \\/ |",
               "     \\  /",
               "      \\/", ""]
ENTER_SCREEN = "\x1b[?1049h\x1b[?25l\x1b[2J"
LEAVE_SCREEN = "\x1b[0m\x1b[?25h\x1b[?1049l"

found_hint = False


def carve_maze():
    """Carve a random maze using depth-first search."""
    #Depth-first search algorithm is used to carve a random maze. 
    #The maze is represented as a grid of walls and paths, where walls are represented by 1 and open paths by 0. 
    #The algorithm starts at a random cell and explores neighboring cells, carving out paths until all cells have been visited.
    grid = [[WALL] * GRID_W for _ in range(GRID_H)]
    grid[1][1] = PATH
    stack = [(1, 1)]
    while stack:
        r, c = stack[-1]
        options = []
        for dr, dc in DIRS:
            nr, nc = r + dr * 2, c + dc * 2
            if 0 < nr < GRID_H - 1 and 0 < nc < GRID_W - 1:
                if grid[nr][nc] == WALL:
                    options.append((dr, dc))
        if not options:
            stack.pop()
            continue
        dr, dc = random.choice(options)
        grid[r + dr][c + dc] = PATH
        grid[r + dr * 2][c + dc * 2] = PATH
        stack.append((r + dr * 2, c + dc * 2))
    return grid


def shortest_path_length(grid, start, goal):
    """Calculate the shortest route using breadth-first search."""
    #This function uses BFS algorithm to find the shortest path from start to finish in the maze
    
    queue, seen = deque([(start, 0)]), {start}
    while queue:
        (r, c), distance = queue.popleft()
        if (r, c) == goal:
            return distance
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            position = (nr, nc)
            if grid[nr][nc] == PATH and position not in seen:
                seen.add(position)
                queue.append((position, distance + 1))
    return None


def count_dead_ends(grid, start, goal):
    total = 0
    for r in range(1, GRID_H, 2):
        for c in range(1, GRID_W, 2):
            if (r, c) in (start, goal):
                continue
            if sum(grid[r + dr][c + dc] == PATH for dr, dc in DIRS) == 1:
                total += 1
    return total


def generate_maze():
    start, goal = (1, 1), (GRID_H - 2, GRID_W - 2)
    while True:
        grid = carve_maze()
        if count_dead_ends(grid, start, goal) >= MIN_DEAD_ENDS:
            return grid, start, goal, shortest_path_length(grid, start, goal)


def spawn_hint(grid, start, goal):
    """Choose a free passage reachable before entering the exit."""
    candidates, seen, stack = [], {start, goal}, [start]
    while stack:
        r, c = stack.pop()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            position = (nr, nc)
            if 0 <= nr < GRID_H and 0 <= nc < GRID_W:
                if grid[nr][nc] == PATH and position not in seen:
                    seen.add(position)
                    candidates.append(position)
                    stack.append(position)
    return random.choice(candidates)


def read_moves(timeout): #This function was debugged and assisted by ChatGPT-Sol 6.1 AI
    """Wait up to `timeout` seconds for key presses. Return the moves, in order."""
    if os.name == "nt":
        deadline = time.monotonic() + timeout
        while not msvcrt.kbhit():
            if time.monotonic() >= deadline:
                return []
            time.sleep(0.002)
        text = ""
        while msvcrt.kbhit():
            text += msvcrt.getwch()
    else:
        fd = sys.stdin.fileno()
        if not select.select([fd], [], [], timeout)[0]:
            return []
        data = os.read(fd, 1024)
        if not data or b"\x04" in data:
            raise EOFError("Terminal input was closed.")
        text = data.decode("latin-1")

    for code, letter in ARROW_KEYS.items():
        text = text.replace(code, letter)
    return [KEY_MOVES[key] for key in text.lower() if key in KEY_MOVES]


@contextlib.contextmanager
def raw_terminal(): #This function was debugged and assisted by ChatGPT-Sol 6.1 AI
    """Prepare the terminal and restore its original settings afterward."""
    if os.name == "nt":
        os.system("")  # turns on ANSI colour codes in the Windows console
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        saved_mode = termios.tcgetattr(fd)
        tty.setcbreak(fd)
    try:
        yield
    finally:
        # Throw away keys still held down, so they don't leak into the next screen.
        if os.name == "nt":
            while msvcrt.kbhit():
                msvcrt.getwch()
        else:
            termios.tcflush(fd, termios.TCIFLUSH)
            termios.tcsetattr(fd, termios.TCSADRAIN, saved_mode)


def countdown_text(seconds_left):
    return f"{RESET}{BOLD}COUNTDOWN: {seconds_left:02d} seconds remaining{RESET}"


def at(row, column, text):
    return f"\x1b[{row};{column}H{text}"


def draw_maze(grid, pos, goal, hint_pos, trail, seconds_left):
    lines = [countdown_text(seconds_left)]
    for r, tiles in enumerate(grid):
        row = [" " * MARGIN]
        for c, tile in enumerate(tiles):
            position = (r, c)
            if position == pos:
                row.append(BALL_T)
            elif position == goal:
                row.append(GOAL_T)
            elif tile == WALL:
                row.append(WALL_T)
            elif position == hint_pos:
                row.append(HINT_T)
            elif position in trail:
                row.append(TRAIL_T)
            else:
                row.append(FLOOR_T)
        lines.append("".join(row))
    lines += [f" Arrow keys / WASD: move    Reach the {GOAL_NAME} (bottom-right)", ""]
    sys.stdout.write("\x1b[H" + "\r\n".join(line + "\x1b[K" for line in lines))
    sys.stdout.flush()


def update_countdown(seconds_left):
    sys.stdout.write(at(1, 1, countdown_text(seconds_left) + "\x1b[K"))
    sys.stdout.flush()


def move_player(previous, pos, collected):
    updates = []
    for (r, c), tile in ((previous, TRAIL_T), (pos, BALL_T)):
        updates.append(at(r + 2, MARGIN + c * TILE_W + 1, tile))
    if collected:
        updates.append(at(GRID_H + 3, 1, HINT_MESSAGE + "\x1b[K"))
    sys.stdout.write("".join(updates))
    sys.stdout.flush()


def run_maze():
    """Play one maze. Returns (won, hint, moves, par)."""
    grid, start, goal, par = generate_maze()
    deadline = time.monotonic() + TIME_LIMIT
    pos, moves, hint, trail = start, 0, False, {start}
    hint_pos = spawn_hint(grid, start, goal)
    shown_seconds = max(0, math.ceil(deadline - time.monotonic()))
    draw_maze(grid, pos, goal, hint_pos, trail, shown_seconds)

    while True:
        # Window shrunk below 80x24: pause the clock until it is big enough again.
        if screen.too_small():
            paused_at = time.monotonic()
            screen.wait_for_size()
            deadline += time.monotonic() - paused_at
            draw_maze(grid, pos, goal, hint_pos, trail, shown_seconds)

        remaining = deadline - time.monotonic()
        seconds = max(0, math.ceil(remaining))
        if remaining <= 0:
            update_countdown(0)
            return False, hint, moves, par
        if seconds != shown_seconds:
            update_countdown(seconds)
            shown_seconds = seconds
        for dr, dc in read_moves(min(0.05, max(0, remaining))):
            nr, nc = pos[0] + dr, pos[1] + dc
            if grid[nr][nc] != PATH or time.monotonic() >= deadline:
                continue
            previous, pos = pos, (nr, nc)
            trail.add(pos)
            moves += 1
            collected = pos == hint_pos
            if collected:
                hint, hint_pos = True, None
            move_player(previous, pos, collected)
            if pos == goal:
                return True, hint, moves, par


def play():
    global found_hint
    found_hint = False

    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        print("Level 2 needs an interactive terminal (arrow keys).")
        return False

    intro = [BOLD + "\x1b[96m" + " LEVEL 2: THE MAINTENANCE TUNNELS" + RESET, "",
             " Alarms! Reach the exit " + GOAL_NAME + " (bottom-right) before the imperial guards",
             " catch you and EXECUTE you!"
             "",
             f" - You have {TIME_LIMIT} seconds.",
             " - Move with the arrow keys or w a s d (hold to keep going).",
             " - A crystal " + HINT_NAME + " is hidden in the tunnels. Pick it up",
             "   and it will reveal one letter of the code in Level 3.",
             " - Run out of time and you are caught: GAME OVER."]
    if screen.show(intro, " Press ENTER to start the clock> ").strip().lower() == "quit":
        return False

    screen.wait_for_size()
    with raw_terminal():
        sys.stdout.write(ENTER_SCREEN)
        try:
            won, hint, moves, par = run_maze()
        finally:
            sys.stdout.write(LEAVE_SCREEN)
            sys.stdout.flush()

    if not won:
        return False

    found_hint = hint
    lines = [GREEN + f" You escaped in {moves} moves (shortest possible: {par})!" + RESET, ""]
    if hint:
        lines += [MAGENTA + line + RESET for line in CRYSTAL_ART]
        lines.append(GREEN + " You collected the crystal!" + RESET)
        lines.append(" It will reveal one letter of the self-destruct code.")
    else:
        lines.append(YELLOW + " You left the hint behind. No letter hint in Level 3." + RESET)
    screen.show(lines, " Press ENTER to continue> ")
    return True


if __name__ == "__main__":
    print("Escaped the maze!" if play() else "Caught!")
