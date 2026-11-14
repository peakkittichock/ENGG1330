import os
import random
import select
import sys
import time

import screen
from screen import BOLD, GREEN, RED, RESET, YELLOW

BAR = 20     # length of the countdown bar
TICK = 0.1   # seconds per bar step, so the player has BAR * TICK = 2 seconds
LETTERS = "abcdefghijklmnopqrstuvwxyz"

ALERT = [
    BOLD + RED + "  !! A GUARD IS COMING !!" + RESET, "",
    "  Footsteps echo down the corridor. A guard is coming close!",
    "  Get ready to hide...", "",
    "      ()                [o o]",
    "      /\\                 |=| ", "",
]


def press_in_time(letter):
    """Mac/Linux: read one key (no ENTER) while the bar shrinks."""
    import termios  # not available on Windows, so imported here
    import tty
    fd = sys.stdin.fileno()
    saved = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    termios.tcflush(fd, termios.TCIFLUSH)  # ignore keys pressed too early
    try:
        for left in range(BAR, 0, -1):
            print("\r  " + "=" * left + " " * (BAR - left), end="", flush=True)
            if select.select([fd], [], [], TICK)[0]:
                return os.read(fd, 1).decode("latin-1").lower() == letter
        return False
    finally:
        termios.tcflush(fd, termios.TCIFLUSH)  # drop late keys so they don't reach the next level
        termios.tcsetattr(fd, termios.TCSADRAIN, saved)


def type_in_time(letter):
    """Windows / no terminal: type the letter and ENTER within the time limit."""
    start = time.time()
    answer = input("  Type the letter and press ENTER: ").strip().lower()
    return answer == letter and time.time() - start <= BAR * TICK


def quicktime():
    """Guard event. Returns True if the player hides in time, False if caught."""
    letter = random.choice(LETTERS)
    screen.wait_for_size()
    print(screen.CLEAR + "\n".join(ALERT))
    time.sleep(1)
    print(BOLD + YELLOW + f"  PRESS  {letter.upper()}  to hide!" + RESET + "\n")

    if os.name != "nt" and sys.stdin.isatty():
        hidden = press_in_time(letter)
    else:
        hidden = type_in_time(letter)

    if hidden:
        screen.show(["", GREEN + BOLD + "  The guard walked away without noticing you." + RESET,
                     "", "  You can proceed. :)"], "Press ENTER to continue> ")
    return hidden


if __name__ == "__main__":
    print("Hidden!" if quicktime() else "Caught!")
