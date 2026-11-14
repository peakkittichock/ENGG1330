import os
import sys
import time

COLS = 80
ROWS = 24

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
CLEAR = RESET + "\033[2J\033[H"
COLOR = sys.stdout.isatty()   # colours only in a real terminal, not a file or pipe


def too_small():
    if not sys.stdout.isatty():
        return False
    size = os.get_terminal_size()
    return size.columns < COLS or size.lines < ROWS


def resize_message(cols):
    return f"Window too small. Please resize to {COLS}x{ROWS}."[:max(cols - 1, 1)]


def wait_for_size():
    if not too_small():
        return False
    while too_small():
        size = os.get_terminal_size()
        print(CLEAR + resize_message(size.columns), end="", flush=True)
        time.sleep(0.5)
    print(CLEAR, end="")
    return True


def show(lines, prompt="> "):
    wait_for_size()
    print(CLEAR + "\n".join(lines))
    return input(prompt)
