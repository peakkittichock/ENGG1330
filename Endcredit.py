import time

import screen
from screen import BOLD, RESET, YELLOW

ROWS = 22
SPEED = 0.35

CREDITS = [
    "THE IRONWAKE FALLS SILENT",
    "",
    "Against all odds, one small ship",
    "slips out of the hangar at midnight",
    "and disappears into the stars.",
    "",
    "The Earther is free.",
    "",
    "",
    "* GALAXY ESCAPE *",
    "",
    "",
    "A GAME BY",
    "",
    "Coding ........... Peak",
    "Puzzles & Story .. Member 2",
    "Testing .......... Member 3",
    "Docs & Videos .... Member 4",
    "",
    "",
    "Made for ENGG1330",
    "The University of Hong Kong, 2026",
    "",
    "",
    "THANK YOU FOR PLAYING",
]


def play_credits():
    print(screen.CLEAR, end="")
    for step in range(len(CREDITS) + ROWS):
        screen.wait_for_size()
        lines = []
        for row in range(ROWS):
            i = row + step - ROWS
            text = CREDITS[i] if 0 <= i < len(CREDITS) else ""
            lines.append(YELLOW + text.center(79) + RESET)
        print("\033[H" + "\n".join(lines))
        time.sleep(SPEED)
    screen.show([""] * 10 + [BOLD + YELLOW + "THE END".center(79) + RESET],
                " " * 29 + "Press ENTER to finish")


if __name__ == "__main__":
    play_credits()
