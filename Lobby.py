"""
GALAXY ESCAPE - welcome screen (simple version)

Run:  python welcome.py
The whole screen is 22 lines + 1 prompt line, so it fits inside 80 x 24
and pressing Enter does not make the screen scroll.
"""

import re

import screen

# Colour codes (ANSI). Put one before text to colour it, RESET to stop.
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"   # clear the screen and move the cursor to the top-left

# r"..." is a raw string: the backslashes in the art are kept exactly as typed.
TITLE = r"""
   .              .                                        .       .
         .             ___   _   _      _   __  ____   __
                      / __| /_\ | |    /_\  \ \/ /\ \ / /             .
.                    | (_ |/ _ \| |__ / _ \  >  <  \ V /         .       .
                      \___/_/ \_\____/_/ \_\/_/\_\  |_|       .     *
                   *                                     .                    *
    *   *                 ___ ___  ___   _   ___ ___
                   *     | __/ __|/ __| /_\ | _ \ __|
                         | _|\__ \ (__ / _ \|  _/ _|        .
          *              |___|___/\___/_/ \_\_| |___|              .         *
                .  ."""

TAGLINE = "                      ~ the last ship leaves at midnight ~  *                 *"

STATION = r"""
             .
                  .              _.-=========-._
        *                    .-'`  \    |    /  `'-.         .
                           .'  ____\____|____/____  '.              .      *
      .             <=====[|===[ I R O N W A K E ]===|]=====>  .
            .              '.  ----/----|----\----  .'               .
       .                .    '-._  /    |    \  _.-'      .               .
                                 `'-=========-'`               .
      *    .                                       *                      *
                             *  IRONWAKE online          .             ."""


def draw_welcome():
    print(BOLD + YELLOW + TITLE[1:] + RESET)    # [1:] skips the first empty line
    print(TAGLINE)
    print(CYAN + STATION[1:] + RESET)    # the IRONWAKE battle station


def show_welcome():
    screen.wait_for_size()            # pause if the window is under 80 x 24
    print(CLEAR, end="")
    draw_welcome()
    screen.ask(" " * 29 + BOLD + "Press ENTER to play" + RESET, draw_welcome)


# ======================================================================
# HOW TO PLAY PAGES
# Each page is drawn inside a box 79 characters wide:
#   21 box lines + 1 blank line + 1 prompt line = 23 lines, fits 80 x 24.
# ======================================================================


GREEN_TILE = "\033[42;30m"    # black letter on green
YELLOW_TILE = "\033[43;30m"   # black letter on yellow
GRAY_TILE = "\033[47;30m"     # black letter on gray

BOX_WIDTH = 79                 # whole box, including the borders
INSIDE = BOX_WIDTH - 4         # text space between "| " and " |"
CONTENT_ROWS = 17              # lines of text per page


def tile(letter, kind):
    """One coloured Wordle tile, drawn the same way as in level 3:
    green [L] = right spot, yellow (L) = wrong spot, gray  L  = not in code."""
    if kind == "G":
        return GREEN_TILE + f"[{letter}]" + RESET
    if kind == "Y":
        return YELLOW_TILE + f"({letter})" + RESET
    return GRAY_TILE + f" {letter} " + RESET


def tiles(word, result):
    """A row of tiles, e.g. tiles('SOLAR', 'Y_YYG')."""
    return " ".join(tile(ch, kind) for ch, kind in zip(word, result))


def visible_length(text):
    """Length as seen on screen: colour codes take no space, so remove them."""
    return len(re.sub(r"\033\[[0-9;]*m", "", text))


def box_line(text=""):
    """'| text           |' padded so the right border always lines up."""
    padding = INSIDE - visible_length(text)
    return "| " + text + " " * padding + " |"


def heading(text):
    return BOLD + YELLOW + text + RESET


PAGES = [
    ("YOUR MISSION", [
        heading("THE STORY"),
        "You were captured and brought aboard the battle station IRONWAKE.",
        "You slipped away from your guards. The last ship leaves at midnight!",
        "",
        heading("YOUR GOAL"),
        "Clear all 3 levels, reach the control room, set the station to",
        "self-destruct and fly away before it explodes.",
        "",
        heading("HOW TO MAKE CHOICES"),
        "Most screens show a numbered list. Type a number and press ENTER:",
        "",
        "    1. Read the commander's log",
        "    2. Check the broken screen",
        "    3. Use the self-destruct panel        > " + BOLD + "1" + RESET,
        "",
        "Look around before you act: logs and screens hide useful clues.",
    ]),
    ("THE THREE LEVELS", [
        heading("LEVEL 1 - THE HOLDING CELL"),
        "Ask two strangers questions from a list, then decide which one is",
        "the enemy spy. Choose wrong and the guards catch you.",
        "",
        heading("LEVEL 2 - THE MAINTENANCE TUNNELS"),
        "Guide your ball through a maze to the exit star (bottom-right).",
        "    Arrow keys or W A S D = move  (no ENTER needed)",
        "    R = new maze      Q twice = quit (quitting before the exit = caught)",
        "",
        heading("LEVEL 3 - THE CONTROL ROOM"),
        "Search the room for clues, then type the 5-letter self-destruct",
        "code into the panel. You get 6 guesses per try. Run out and the",
        "alarm sounds, but you can search again and retry.",
        "",
        "Clear a level and the next one starts. Escape = MISSION COMPLETE!",
    ]),
    ("CODES AND DANGER", [
        heading("CRACKING THE CODE (WORDLE)"),
        "After each guess, every letter gets a colour:",
        "",
        "    " + tiles("SOLAR", "Y_YYG") + "      guess 1",
        "    " + tiles("LASER", "GGGGG") + "      guess 2: correct!",
        "",
        "    " + tile("R", "G") + " right spot    "
        + tile("S", "Y") + " in the code, wrong spot    "
        + tile("O", "_") + " not in the code",
        "",
        heading("STEALTH ALERT!"),
        "Between levels a guard may walk by. A letter appears, e.g. "
        + BOLD + "PRESS [ K ]" + RESET,
        "Press that key before the time bar runs out (about 2.5 seconds).",
        "Wrong key or too slow = caught.",
        "",
        heading("CAUGHT?") + "  It's GAME OVER, but you can type y to play again.",
        heading("TIP") + "  Start the code with common letters, like RAISE.",
    ]),
]


def draw_page(number, message=""):
    """Draw one page. `message` goes on the blank line under the box."""
    title, lines = PAGES[number]
    screen.wait_for_size()            # pause if the window is under 80 x 24
    print(CLEAR, end="")
    border = "+" + "-" * (BOX_WIDTH - 2) + "+"
    print(border)
    header = f"HOW TO PLAY  -  {title}  ({number + 1}/{len(PAGES)})"
    print(box_line(BOLD + header.center(INSIDE) + RESET))
    print(border)
    for row in range(CONTENT_ROWS):                    # always 17 rows, even if
        text = lines[row] if row < len(lines) else ""  # the page has fewer lines
        print(box_line(text))
    print(border)
    print("  " + message)               # feedback line (empty most of the time)


def show_how_to_play():
    """Enter = next page, b = previous page. Leaves after the last page.

    Invalid keys and "b" on the first page do not move the page; the player
    is told why on the line under the box.
    """
    page = 0
    message = ""
    while page < len(PAGES):
        draw_page(page, message)
        shown = message
        message = ""
        if page == len(PAGES) - 1:
            prompt = "ENTER = start the game    b = back"
        else:
            prompt = "ENTER = next page" + ("    b = back" if page > 0 else "")
        answer = screen.ask(" " * 2 + BOLD + prompt + RESET + "  > ",
                            lambda: draw_page(page, shown)).strip().lower()
        if answer == "b":
            if page == 0:
                message = YELLOW + "This is already the first page." + RESET
            page = max(page - 1, 0)
        elif answer == "":
            page += 1
        else:                       # anything else: same page, say why
            message = (YELLOW + f"'{answer[:20]}' is not a command. "
                       "Press ENTER, or type b to go back." + RESET)


def run():
    """Welcome screen + how-to-play pages (used by main.py)."""
    show_welcome()
    show_how_to_play()
    print(CLEAR, end="")


if __name__ == "__main__":
    run()
    print("The game starts here...")