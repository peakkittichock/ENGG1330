import os
import random
import select
import sys
import time

import screen
from screen import BOLD, GREEN, RED, RESET, YELLOW

BAR = 20
TICK = 0.1
LETTERS = "abcdefghijklmnopqrstuvwxyz"

ALERT = [
    BOLD + RED + "  !! A GUARD IS COMING !!" + RESET, "",
    "  Footsteps echo down the corridor. A guard is coming close!",
    "  Get ready to hide...", "",
    "      ()                [o o]",
    "      /\\                 |=| ", "",
]


def press_in_time(hideletter):
    import termios
    import tty
    fd = sys.stdin.fileno()
    saved = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        termios.tcflush(fd, termios.TCIFLUSH)
        for left in range(BAR, 0, -1):
            sys.stdout.write("\r  " + "=" * left + " " * (BAR - left))
            sys.stdout.flush()
            if select.select([fd], [], [], TICK)[0]:
                return os.read(fd, 1).decode("latin-1").lower() == hideletter
        return False
    finally:
        termios.tcflush(fd, termios.TCIFLUSH)
        termios.tcsetattr(fd, termios.TCSADRAIN, saved)


def type_in_time(hideletter):
    start = time.time()
    answer = input("  Type the letter and press ENTER: ").strip().lower()
    return answer == hideletter and time.time() - start <= BAR * TICK


def quicktime(chance):
    if random.random() >= chance:
        return True
    hideletter = random.choice(LETTERS)
    screen.wait_for_size()
    print(screen.CLEAR + "\n".join(ALERT))
    time.sleep(1)
    print(BOLD + YELLOW + f"  PRESS  {hideletter.upper()}  to hide!" + RESET + "\n")

    if os.name != "nt" and sys.stdin.isatty():
        hidden = press_in_time(hideletter)
    else:
        hidden = type_in_time(hideletter)

    if hidden:
        screen.show(["", GREEN + BOLD + "  The guard walked away without noticing you."
                     + RESET, "", "  You can proceed. :)"], "Press ENTER to continue> ")
        return True
    screen.show(["", RED + BOLD + "  The guard shines a light right on you." + RESET,
                 "", "  You got caught. :("], "Press ENTER> ")
    return False


if __name__ == "__main__":
    print("Hidden!" if quicktime(1) else "Caught!")
