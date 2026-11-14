import os
import sys
import threading
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

# While the window is smaller than 80x24 the game is paused:
# a background thread shows one message, and every print waits until it is over.
paused = False
quitting = False        # Ctrl+C pressed while paused
pause_start = 0.0
paused_time = 0.0       # total seconds spent paused
last_screen = ""        # what is on screen now, drawn again after a pause
lock = threading.Lock()
real_stdout = sys.stdout


def too_small():
    try:
        size = os.get_terminal_size(real_stdout.fileno())
    except OSError:
        return False
    return size.columns < COLS or size.lines < ROWS


def clock():
    """Like time.monotonic(), but stands still while the game is paused."""
    now = pause_start if paused else time.monotonic()
    return now - paused_time


def wait_while_paused():
    """Wait until the pause is over. True if there was a pause."""
    global quitting
    if not paused:
        return False
    try:
        while paused and not quitting:
            time.sleep(0.05)
    except KeyboardInterrupt:   # Ctrl+C while paused: quit the game
        quitting = True
        raise SystemExit
    return True


class PausingOutput:
    """Takes the place of sys.stdout: printing waits while paused."""

    def write(self, text):
        global last_screen
        while True:
            with lock:
                if not paused or quitting:
                    if "\033[2J" in text:            # screen cleared: start remembering again
                        last_screen = text[text.rfind("\033[2J"):]
                    elif text.startswith("\033[H"):  # whole new frame from the top
                        last_screen = text
                    else:
                        last_screen += text
                    return real_stdout.write(text)
            wait_while_paused()

    def fileno(self):
        raise OSError("no fileno")   # makes input() print its prompt through write()

    def __getattr__(self, name):
        return getattr(real_stdout, name)


def watch():
    global paused, pause_start, paused_time
    while True:
        if not paused and too_small():
            with lock:
                paused, pause_start = True, time.monotonic()
                real_stdout.write(CLEAR + f"Please make the window at least {COLS}x{ROWS}. Game paused.")
                real_stdout.flush()
        elif paused and not too_small():
            with lock:
                paused_time += time.monotonic() - pause_start
                paused = False
                real_stdout.write(CLEAR + last_screen)
                real_stdout.flush()
        time.sleep(0.1)


def start():
    """Call once when the game starts."""
    if sys.stdout is real_stdout and real_stdout.isatty():
        sys.stdout = PausingOutput()
        threading.Thread(target=watch, daemon=True).start()


def show(lines, prompt="> "):
    print(CLEAR + "\n".join(lines))
    return input(prompt)
