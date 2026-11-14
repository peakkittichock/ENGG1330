import os
import random
import select
import sys
import time

import screen
from screen import BOLD, GREEN, RED, RESET, YELLOW

TIME_LIMIT = 5  # seconds to type the word and press ENTER
BAR = 20        # length of the countdown bar
TICK = 0.1      # how often the bar is redrawn (seconds)
# Word to type -> where you hide.
HIDE_PLACES = {
    "ceiling": "up in the ceiling",
    "vent": "inside the vent",
    "deck": "under the deck",
    "cargo": "behind the cargo",
    "gonkdroid": "behind the GONK droid",
    "r2q5": "behind R2-Q5",
}

ALERT = [
    BOLD + RED + "  !! A GUARD IS COMING !!" + RESET, "",
    "  Footsteps echo down the corridor. A guard is coming close!",
    "  Get ready to hide...", "",
    "      ()                [o o]",
    "      /\\                 |=| ", "",
]


def draw(left, typed, note):
    """Redraw one line: shrinking bar, seconds left, what the player typed."""
    filled = round(BAR * left / TIME_LIMIT)
    colour = GREEN if left > TIME_LIMIT / 2 else YELLOW if left > TIME_LIMIT / 4 else RED
    bar = colour + "=" * filled + RESET + " " * (BAR - filled)
    sys.stdout.write(f"\r\x1b[K  [{bar}] {left:3.1f}s  {note}> {typed}")
    sys.stdout.flush()


def timed_typing(word, get_key):
    """Read keys until the right word + ENTER (True) or time runs out (False).
    A wrong word clears the line so the player can type again."""
    deadline = time.time() + TIME_LIMIT
    typed, note = "", ""
    while True:
        left = deadline - time.time()
        if left <= 0:
            draw(0, typed, note)
            print()
            return False
        draw(left, typed, note)
        key = get_key()
        if key is None:
            continue
        if key in "\r\n":
            if typed.strip().lower() == word:
                print()
                return True
            typed, note = "", RED + "Wrong! " + RESET
        elif key in "\x7f\x08":           # backspace
            typed = typed[:-1]
        elif key.isprintable() and len(typed) < 20:
            typed += key


def type_with_timer(word):
    if os.name == "nt":                   # Windows
        import msvcrt

        def get_key():
            end = time.time() + TICK
            while time.time() < end:
                if msvcrt.kbhit():
                    return msvcrt.getwch()
                time.sleep(0.01)
            return None
        return timed_typing(word, get_key)

    import termios                        # Mac / Linux
    import tty
    fd = sys.stdin.fileno()
    saved = termios.tcgetattr(fd)
    tty.setcbreak(fd)                     # read keys one by one, no echo
    termios.tcflush(fd, termios.TCIFLUSH)  # ignore keys pressed too early

    def get_key():
        if select.select([fd], [], [], TICK)[0]:
            return os.read(fd, 1).decode("latin-1")
        return None
    try:
        return timed_typing(word, get_key)
    finally:
        termios.tcflush(fd, termios.TCIFLUSH)  # drop late keys so they don't reach the next level
        termios.tcsetattr(fd, termios.TCSADRAIN, saved)


def type_without_timer(word):
    """No real terminal (e.g. piped input): plain input(), time checked after ENTER."""
    deadline = time.time() + TIME_LIMIT
    while True:
        answer = input("  > ").strip().lower()
        if time.time() > deadline:
            return False
        if answer == word:
            return True
        print(RED + "  Wrong! Type it again, quick!" + RESET)


def quicktime():
    """Guard event. Returns True if the player hides in time, False if caught."""
    word = random.choice(list(HIDE_PLACES))
    place = HIDE_PLACES[word]
    screen.wait_for_size()
    print(screen.CLEAR + "\n".join(ALERT))
    time.sleep(1)
    print(BOLD + YELLOW + f"  TYPE  {word.upper()}  and press ENTER to hide {place}!" + RESET)
    print(f"  You have {TIME_LIMIT} seconds! Wrong word? Just type it again.\n")

    if sys.stdin.isatty():
        hidden = type_with_timer(word)
    else:
        hidden = type_without_timer(word)

    if hidden:
        screen.show(["", GREEN + BOLD + f"  You hide {place}." + RESET,
                     GREEN + BOLD + "  The guard walked away without noticing you." + RESET,
                     "", "  You can proceed. :)"], "Press ENTER to continue> ")
    return hidden


if __name__ == "__main__":
    print("Hidden!" if quicktime() else "Caught!")
