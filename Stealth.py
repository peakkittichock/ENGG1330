# Stealth event (quick-time event) - can be dropped in between any two levels.
#
# Idea by a teammate: a guard walks close, a random letter appears, and the
# player has to press that letter before the time bar runs out.
#
# Contract with main.py: quicktime(chance) returns
#   True  -> no guard came, or the player hid in time (game goes on)
#   False -> the player got caught                     (game over)
#
# How the timer works (standard library only, no threads):
#   * Linux / macOS: the terminal is put in "cbreak" mode (one key at a time,
#     no ENTER needed) and select() waits up to 0.1 s for a key, so the bar
#     can shrink while we wait.
#   * Windows: msvcrt.kbhit() tells us if a key is waiting.
#   * Not a real terminal (e.g. input piped from a file): fall back to a
#     normal input() and check how long the player took.

import os
import random
import sys
import time

import screen

if os.name == "nt":
    import msvcrt
else:
    import select
    import termios
    import tty

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
TIME_LIMIT = 2.5        # seconds the player has to press the letter
BAR_LENGTH = 25         # width of the countdown bar
GET_READY = 1.0         # pause before the letter appears

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

WARNINGS = [
    "Heavy boots echo down the corridor... a trooper is coming your way!",
    "A patrol droid's red eye sweeps the hallway towards you!",
    "Two guards turn the corner, chatting. They'll see you any second!",
]


def clear():
    print("\033[2J\033[H", end="")


# ---------------------------------------------------------------------------
# Keyboard helpers
# ---------------------------------------------------------------------------
def throw_away_old_keys():
    """Forget keys pressed earlier, so the player can't press them in advance."""
    if os.name == "nt":
        while msvcrt.kbhit():
            msvcrt.getwch()
    else:
        termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)


def key_waiting(wait):
    """Return True if a key is pressed within `wait` seconds."""
    if os.name == "nt":
        end = time.time() + wait
        while time.time() < end:
            if msvcrt.kbhit():
                return True
            time.sleep(0.01)
        return False
    ready, _, _ = select.select([sys.stdin], [], [], wait)
    return bool(ready)


def read_one_key():
    """Read a single key that we already know is waiting."""
    if os.name == "nt":
        return msvcrt.getwch()
    return os.read(sys.stdin.fileno(), 1).decode("latin-1")


def draw_bar(time_left):
    """Redraw the countdown bar on the current line."""
    filled = round(BAR_LENGTH * time_left / TIME_LIMIT)
    colour = GREEN if filled > BAR_LENGTH // 2 else RED
    bar = colour + "=" * filled + RESET + " " * (BAR_LENGTH - filled)
    sys.stdout.write(f"\r  [{bar}] {time_left:3.1f}s ")
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# The two ways of asking for the letter
# ---------------------------------------------------------------------------
def wait_for_key_timed(letter, redraw=None):
    """Show a shrinking bar and wait for ONE key. True = right key in time.

    If the window becomes smaller than 80 x 24 during the countdown, the
    timer PAUSES: the time left is kept, the game waits for a bigger window,
    redraw() puts the alert back on screen and the countdown carries on.
    Losing because the window was resized would be unfair.
    """
    fd = sys.stdin.fileno()
    saved = None
    if os.name != "nt":
        saved = termios.tcgetattr(fd)
        tty.setcbreak(fd)              # keys arrive at once, not echoed
    try:
        throw_away_old_keys()
        end = time.time() + TIME_LIMIT
        while True:
            time_left = end - time.time()
            if time_left <= 0:
                draw_bar(0)
                print()
                print(RED + "  Too slow!" + RESET)
                return False
            if screen.too_small():         # pause the timer
                screen.wait_for_size()     # (also throws away keys pressed
                if redraw is not None:     #  while paused)
                    redraw()
                end = time.time() + time_left
                continue
            draw_bar(time_left)
            if key_waiting(min(0.1, time_left)):
                key = read_one_key()
                print()
                if key.lower() == letter:
                    return True
                if key.isalnum():
                    print(RED + f"  You pressed '{key}' - wrong key!" + RESET)
                else:                  # ENTER, space, Esc, ...
                    print(RED + "  Wrong key!" + RESET)
                return False
    finally:
        if saved is not None:          # always give the terminal back
            termios.tcsetattr(fd, termios.TCSADRAIN, saved)


def wait_for_key_typed(letter):
    """Fallback without a real terminal: input() + ENTER, then check the time."""
    start = time.time()
    answer = input(f"  Type {letter} and press ENTER: ").strip().lower()
    taken = time.time() - start
    if taken > TIME_LIMIT:
        print(RED + f"  Too slow! ({taken:.1f}s)" + RESET)
        return False
    return answer == letter


# ---------------------------------------------------------------------------
# The event itself
# ---------------------------------------------------------------------------
def quicktime(chance=0.5):
    """Maybe spawn a guard. Returns True if safe, False if caught."""
    if random.random() >= chance:
        return True                    # no guard this time

    letter = random.choice("abcdefghijklmnopqrstuvwxyz")   # new letter every time

    warning = random.choice(WARNINGS)

    def draw_alert():
        print(BOLD + YELLOW + "[ !! STEALTH ALERT !! ]" + RESET)
        print()
        print(warning)
        print()
        print("Get ready to hide...")
        print()
        print(BOLD + f"  PRESS  [ {letter.upper()} ]  TO HIDE!" + RESET)
        print()

    screen.wait_for_size()             # resize first, so the timer is fair
    clear()
    print(BOLD + YELLOW + "[ !! STEALTH ALERT !! ]" + RESET)
    print()
    print(warning)
    print()
    print("Get ready to hide...")
    time.sleep(GET_READY)
    print()
    print(BOLD + f"  PRESS  [ {letter.upper()} ]  TO HIDE!" + RESET)
    print()

    if sys.stdin.isatty():
        safe = wait_for_key_timed(letter, draw_alert)
    else:
        safe = wait_for_key_typed(letter)

    print()
    if safe:
        print(GREEN + "The guard walks past without noticing you. "
              "You can proceed." + RESET)
        screen.ask("\n(press ENTER to continue) ",
                   lambda: print(GREEN + "The guard walks past without noticing "
                                 "you. You can proceed." + RESET))
    else:
        print(RED + "A hand grabs your shoulder... you've been spotted!" + RESET)
        time.sleep(1.5)
    return safe


# Demonstration: guard always appears when this file is run on its own.
if __name__ == "__main__":
    print("You hid!" if quicktime(1.0) else "You got caught.")
