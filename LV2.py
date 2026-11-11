import os
import random
import select
import sys

import screen
from screen import BOLD, CYAN, GREEN, RED, RESET, YELLOW

CELLS_W, CELLS_H = 19, 9
GRID_W = CELLS_W * 2 + 1
GRID_H = CELLS_H * 2 + 1
WALL, PATH = 1, 0

MOVES = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
ARROWS = {b"A": "w", b"B": "s", b"C": "d", b"D": "a"}

WALL_TILE = "\033[44m  " + RESET
PLAYER_TILE = BOLD + YELLOW + "()" + RESET
EXIT_TILE = BOLD + GREEN + "EX" + RESET
TRAIL_TILE = CYAN + ". " + RESET
FLOOR_TILE = "  "

HELP = "Arrow keys / w a s d: move (hold to keep going)   r: new maze   q: give up"


def carve_maze():
    grid = [[WALL] * GRID_W for _ in range(GRID_H)]
    grid[1][1] = PATH
    stack = [(1, 1)]
    while stack:
        r, c = stack[-1]
        options = []
        for dr, dc in MOVES.values():
            nr, nc = r + 2 * dr, c + 2 * dc
            if 0 < nr < GRID_H - 1 and 0 < nc < GRID_W - 1 and grid[nr][nc] == WALL:
                options.append((dr, dc))
        if options:
            dr, dc = random.choice(options)
            grid[r + dr][c + dc] = PATH
            grid[r + 2 * dr][c + 2 * dc] = PATH
            stack.append((r + 2 * dr, c + 2 * dc))
        else:
            stack.pop()
    return grid


def walk(grid, pos, keys, goal):
    path = []
    for key in keys:
        dr, dc = MOVES[key]
        nxt = (pos[0] + dr, pos[1] + dc)
        if grid[nxt[0]][nxt[1]] == WALL:
            return path, True
        pos = nxt
        path.append(pos)
        if pos == goal:
            break
    return path, False


def maze_lines(grid, pos, goal, trail, moves, message):
    lines = [BOLD + CYAN + " LEVEL 2: THE MAINTENANCE TUNNELS" + RESET
             + f"    Moves: {moves}    Reach EX (bottom-right)"]
    for r in range(GRID_H):
        row = " "
        for c in range(GRID_W):
            if (r, c) == pos:
                row += PLAYER_TILE
            elif (r, c) == goal:
                row += EXIT_TILE
            elif grid[r][c] == WALL:
                row += WALL_TILE
            elif (r, c) in trail:
                row += TRAIL_TILE
            else:
                row += FLOOR_TILE
        lines.append(row)
    lines.append(" " + message)
    return lines


def read_key(fd):
    key = os.read(fd, 1)
    if key in (b"", b"\x04"):
        raise EOFError
    if key != b"\x1b":
        return key.decode("latin-1").lower()
    if not select.select([fd], [], [], 0.1)[0] or os.read(fd, 1) not in (b"[", b"O"):
        return ""
    return ARROWS.get(os.read(fd, 1), "")


def draw(lines):
    screen.wait_for_size()
    sys.stdout.write("\033[H" + "\n".join(line + "\033[K" for line in lines) + "\033[J")
    sys.stdout.flush()


def wait_for_key(fd, lines):
    draw(lines)
    while not select.select([fd], [], [], 0.25)[0]:
        if screen.wait_for_size():
            draw(lines)
    return read_key(fd)


def play():
    live = os.name != "nt" and sys.stdin.isatty() and sys.stdout.isatty()
    if not live:
        return run_maze(None)

    import termios
    import tty
    fd = sys.stdin.fileno()
    saved = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        sys.stdout.write(screen.CLEAR + "\033[?25l")
        return run_maze(fd)
    finally:
        sys.stdout.write("\033[?25h")
        termios.tcsetattr(fd, termios.TCSADRAIN, saved)


def run_maze(fd):
    grid = carve_maze()
    start, goal = (1, 1), (GRID_H - 2, GRID_W - 2)
    pos, trail, moves = start, {start}, 0
    message = HELP
    quit_asked = False

    while True:
        lines = maze_lines(grid, pos, goal, trail, moves, message)
        if fd is None:
            keys = screen.show(lines, " Move> ").strip().lower().replace(" ", "")
        else:
            keys = wait_for_key(fd, lines)

        if keys == "quit" or (keys == "q" and quit_asked):
            return False
        if keys == "q":
            quit_asked = True
            message = YELLOW + "Press q again to give up (the guards catch you)." + RESET
            continue
        quit_asked = False

        if keys == "r":
            grid = carve_maze()
            pos, trail, moves = start, {start}, 0
            message = "A new maze! Good luck."
            continue
        if keys == "" or any(k not in MOVES for k in keys):
            message = YELLOW + "That key does nothing. Use the arrow keys or w a s d." + RESET
            continue

        path, hit_wall = walk(grid, pos, keys, goal)
        if path:
            pos = path[-1]
        moves += len(path)
        trail.update(path)

        if pos == goal:
            message = GREEN + f"You found the exit in {moves} moves!" + RESET
            if fd is not None:
                import termios
                termios.tcflush(fd, termios.TCIFLUSH)
                sys.stdout.write("\033[?25h")
            screen.show(maze_lines(grid, pos, goal, trail, moves, message),
                        " Press ENTER to continue> ")
            return True
        if hit_wall:
            message = RED + "Bump! That's a wall." + RESET
        else:
            message = HELP


if __name__ == "__main__":
    print("Escaped the maze!" if play() else "You gave up.")
