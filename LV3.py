# Lv 3 : Finding the self-destruct code

import time

import screen

GREEN_TILE = "\033[42;30m"
YELLOW_TILE = "\033[43;30m"
GRAY_TILE = "\033[47;30m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

CODE = "OMEGA"          
MAX_GUESSES = 6         


def clear():
    print("\033[2J\033[H", end="")

# Wordle

def score_guess(guess, answer):
    result = ["_"] * 5
    leftover = {}
    for i in range(5):                         
        if guess[i] == answer[i]:
            result[i] = "G"
        else:
            leftover[answer[i]] = leftover.get(answer[i], 0) + 1
    for i in range(5):                         
        if result[i] == "_" and leftover.get(guess[i], 0) > 0:
            result[i] = "Y"
            leftover[guess[i]] -= 1
    return result


def tiles(guess, result):
    out = ""
    for letter, r in zip(guess, result):
        if r == "G":
            out += GREEN_TILE + f"[{letter}]" + RESET + " "
        elif r == "Y":
            out += YELLOW_TILE + f"({letter})" + RESET + " "
        else:
            out += GRAY_TILE + f" {letter} " + RESET + " "
    return out


LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BACK = "BACK"           # typed instead of a code: leave the panel


def check_code(guess, guesses):
    """Return an error message if `guess` cannot be used, or "" if it is fine.

    guess is already stripped and in capitals. A rejected code never costs a
    guess. Cases handled:
      * empty input (just ENTER)
      * too short / too long (the message says how many letters were typed)
      * anything that is not A-Z: digits, spaces, symbols, and also letters
        such as E with an accent, which str.isalpha() would let through
      * a code the player has already tried on this panel
    """
    if guess == "":
        return "You didn't type anything. The code has 5 letters."
    if len(guess) < 5:
        return f"Too short: {len(guess)} letter(s). The code has 5 letters."
    if len(guess) > 5:
        return f"Too long: {len(guess)} characters. The code has 5 letters."
    for letter in guess:
        if letter not in LETTERS:
            return f"'{letter}' is not allowed. Use the letters A-Z only."
    for old_guess, _ in guesses:
        if guess == old_guess:
            return f"You already tried {guess}. Try a different code."
    return ""


def code_panel(found_clue, found_letter):
    """Returns True (right code), False (out of guesses) or None (BACK)."""
    guesses = []
    message = ""

    def draw():
        print(BOLD + YELLOW + "=== SELF-DESTRUCT PANEL ===" + RESET)
        print()
        if found_clue:
            print("Clue: The last letter of the Greek alphabet - the end of everything.")
        else:
            print("Clue: ??? (maybe the commander wrote it down somewhere)")
        print("Code: _ _ _ G _" if found_letter else "Code: _ _ _ _ _")
        print()
        for guess, result in guesses:
            print("    " + tiles(guess, result))
        for _ in range(MAX_GUESSES - len(guesses)):
            print("     _   _   _   _   _")
        print()
        left = MAX_GUESSES - len(guesses)
        if left == 1:
            print(RED + "LAST GUESS! (type BACK to search the room first)" + RESET)
        else:
            print(f"Guesses left: {left}   (type BACK to leave the panel)")
        print(message)

    while len(guesses) < MAX_GUESSES:
        screen.wait_for_size()        # pause if the window is under 80 x 24
        clear()
        draw()
        # screen.ask() pauses at once if the window shrinks while typing,
        # then calls draw() again (see screen.py).
        guess = screen.ask("Type the 5-letter code > ", draw).strip().upper()

        if guess == BACK:
            return None
        message = check_code(guess, guesses)
        if message:                   # invalid code: explain, no guess used
            message = RED + message + RESET
            continue
        guesses.append((guess, score_guess(guess, CODE)))
        if guess == CODE:
            return True
    return False


# The control room

def control_room():
    found_clue = False
    found_letter = False
    message = "You reach the CONTROL ROOM. Find the self-destruct code!"

    def draw():
        print(BOLD + YELLOW + "[ LEVEL 3: CONTROL ROOM ]" + RESET)

        print()
        print("Blinking consoles everywhere. In the middle stands the")
        print("SELF-DESTRUCT PANEL. A log and a broken screen are nearby.")
        print()
        print(message)
        print()
        print("1. Read the commander's log")
        print("2. Check the broken screen")
        print("3. Use the self-destruct panel")

    while True:
        screen.wait_for_size()        # pause if the window is under 80 x 24
        clear()
        draw()
        choice = screen.ask("> ", draw).strip()

        if choice == "1":
            found_clue = True
            message = ("COMMANDER'S LOG: \"The code is the last letter of the Greek\n"
                       "alphabet - the end of everything.\"")

        elif choice == "2":
            found_letter = True
            message = "The broken screen flickers: CODE  _ _ _ G _"

        elif choice == "3":
            result = code_panel(found_clue, found_letter)
            if result is True:
                return True
            if result is None:            # player typed BACK
                message = "You step away from the panel. Look around for clues."
            else:                         # all guesses used up
                message = RED + "WRONG CODE! Alarms blare. Try again!" + RESET

        elif choice == "":
            message = "You didn't choose anything. Type 1, 2 or 3 and press ENTER."
        else:
            message = f"'{choice[:20]}' is not an option. Choose 1, 2 or 3."



# Ending animation: the ship flies away and the station explodes
#
# The animation plays by itself (no ENTER between frames).
# Change FRAME_DELAY to make the ship fly faster or slower.

FRAME_DELAY = 0.12      # seconds per frame while the ship flies
BOOM_DELAY = 0.35       # seconds per explosion frame (slower = more dramatic)
SCENE_WIDTH = 78        # stay inside the 80-column screen

SHIP = "==[>"
SHIP_ROW = 2            # which line of the scene the ship flies on
SHIP_START = 30         # column where the ship starts (next to the station)

STATION = [
    r"      _.-=========-._",
    r"   .-'   \   |   /  '-.",
    r"  <=[|== IRONWAKE ==|]=>",
    r"   '-.   /   |   \  .-'",
    r"      `'-=========-'`",
]

# Each explosion frame replaces the station, one after another.
EXPLOSION = [
    [
        r"      _.-=========-._",
        r"   .-'   \ * | * /  '-.",
        r"  <=[|== IRONWAKE ==|]=>",
        r"   '-.   / * | * \  .-'",
        r"      `'-=========-'`",
    ],
    [
        r"          \  |  /",
        r"       -- ( *** ) --",
        r"      --  ( BOOM ) --",
        r"       -- ( *** ) --",
        r"          /  |  \ ",
    ],
    [
        r"     \    \  |  /    /",
        r"   --  ( * BOOM!! * )  --",
        r"  --- ( *** BOOM!! *** ) ---",
        r"   --  ( * BOOM!! * )  --",
        r"     /    /  |  \    \ ",
    ],
    [
        r"   .   *   '   ,   *   .",
        r" '   .   *   .   '   *   ",
        r"   *   '   .   *   ,   . ",
        r" .   ,   *   '   .   *   ",
        r"   '   *   .   ,   '   . ",
    ],
    [
        r"     .       '       .",
        r"         *       ,",
        r"   '         .        *",
        r"        ,        '",
        r"     *       .       '",
    ],
    ["", "", "", "", ""],
]


def draw_scene(title, picture, ship_x):
    """Draw one frame: a title, the station (or explosion) and the ship.

    ship_x is the column of the ship; None means the ship is not shown.
    "\033[H" moves the cursor to the top-left, so the new frame is drawn
    over the old one (smoother than clearing the whole screen).
    """
    screen.wait_for_size()            # animation pauses if the window shrinks
    lines = [BOLD + YELLOW + title + RESET, ""]
    for row, art in enumerate(picture):
        line = art.ljust(SCENE_WIDTH)
        if row == SHIP_ROW and ship_x is not None and ship_x + len(SHIP) <= SCENE_WIDTH:
            line = line[:ship_x] + SHIP + line[ship_x + len(SHIP):]
        lines.append(line)
    print("\033[H" + "\n".join(line + "\033[K" for line in lines), flush=True)


def ending():
    clear()

    # 1. Countdown while the ship is still next to the station
    for number in ["3", "2", "1"]:
        draw_scene("CODE ACCEPTED. SELF-DESTRUCT IN " + number + "...",
                   STATION, SHIP_START)
        time.sleep(1)

    # 2. The ship flies away, 2 columns per frame
    ship_x = SHIP_START
    while ship_x < 50:
        draw_scene("Punch it! Fly, FLY!", STATION, ship_x)
        time.sleep(FRAME_DELAY)
        ship_x += 2

    # 3. The station explodes while the ship keeps flying
    for picture in EXPLOSION:
        draw_scene("*** KABOOM ***", picture, ship_x)
        time.sleep(BOOM_DELAY)
        ship_x += 4

    # 4. The ship flies off the right edge of the screen
    while ship_x + len(SHIP) <= SCENE_WIDTH:
        draw_scene("", EXPLOSION[-1], ship_x)
        time.sleep(FRAME_DELAY)
        ship_x += 2
    draw_scene("", EXPLOSION[-1], None)

    def last_frame():
        draw_scene("", EXPLOSION[-1], None)
        print()
        print(BOLD + YELLOW + "The station is gone. You escaped! MISSION COMPLETE!"
              + RESET)

    print()
    print(BOLD + YELLOW + "The station is gone. You escaped! MISSION COMPLETE!" + RESET)
    screen.ask("(press ENTER)", last_frame)


def play():
    """Run level 3 once (used by main.py). Returns True when the player escapes."""
    if control_room():
        ending()
        return True
    return False


def main():
    while True:
        if control_room():
            ending()
        else:
            clear()
            print(RED + BOLD + "CAUGHT! The guards drag you away. GAME OVER." + RESET)
        if screen.ask("\nPlay again? (y/n) ").strip().lower() != "y":
            break


if __name__ == "__main__":
    main()