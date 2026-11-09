"""
GALAXY ESCAPE - end credits (simple version)

Run:  python credits.py
Text scrolls slowly up the screen in yellow, like a space-movie ending.
Lines near the bottom are spread out and lines near the top are packed
together and dimmed, which makes the text look like it is flying away.

Every frame is drawn from the top-left corner over the previous one,
so the terminal itself never scrolls and everything stays inside 80 x 24.
"""

import time

import screen

YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"   # clear the screen, cursor to the top-left
HOME = "\033[H"           # cursor to the top-left (draw over the last frame)

WIDTH = 79      # stay one column short of 80 so lines never wrap
ROWS = 23       # rows used by the animation (row 24 stays free)
SPEED = 0.35    # seconds between frames

# Lines must be 38 characters or less, because the bottom rows spread
# every letter out with a space and the result must fit in 79 columns.
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


def spread(text):
    """'ABC' -> 'A B C'. Spreads a line out so it looks closer to the player."""
    return " ".join(text)


def style_row(text, row):
    """Pick the look of a line from how high up the screen it is."""
    if row < ROWS // 3:                      # top third: far away
        return DIM + YELLOW + text.center(WIDTH) + RESET
    if row < 2 * ROWS // 3:                  # middle third
        return YELLOW + text.center(WIDTH) + RESET
    return BOLD + YELLOW + spread(text).center(WIDTH) + RESET   # bottom: close


def draw_frame(step):
    """Draw the credits as they look after `step` lines have scrolled in."""
    screen.wait_for_size()                   # credits pause if the window shrinks
    lines = []
    for row in range(ROWS):
        index = row + step - ROWS            # which credit line sits on this row
        if 0 <= index < len(CREDITS):
            lines.append(style_row(CREDITS[index], row))
        else:
            lines.append(" " * WIDTH)        # blank row (also wipes the old frame)
    print(HOME + "\n".join(lines))


def play_credits():
    print(CLEAR, end="")
    for step in range(len(CREDITS) + ROWS + 1):   # until the last line leaves the top
        draw_frame(step)
        time.sleep(SPEED)
    screen.wait_for_size()
    print(CLEAR, end="")
    draw_the_end()
    screen.ask(" " * 29 + "Press ENTER to finish", draw_the_end)


def draw_the_end():
    print("\n" * 10 + BOLD + YELLOW + "THE END".center(WIDTH) + RESET + "\n")


if __name__ == "__main__":
    try:
        play_credits()
    except KeyboardInterrupt:     # Ctrl+C skips the credits
        print(RESET + CLEAR, end="")