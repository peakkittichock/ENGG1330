import time

import screen
from screen import BOLD, RED, RESET, YELLOW

CODE = "OMEGA"
MAX_GUESSES = 6

GREEN_TILE = "\033[42;30m"
YELLOW_TILE = "\033[43;30m"
GRAY_TILE = "\033[47;30m"


def score_guess(guess, answer):
    result = ["_"] * 5
    unused = {}
    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = "G"
        else:
            unused[answer[i]] = unused.get(answer[i], 0) + 1
    for i in range(5):
        if result[i] == "_" and unused.get(guess[i], 0) > 0:
            result[i] = "Y"
            unused[guess[i]] -= 1
    return result


def tiles(guess, result):
    out = ""
    for letter, mark in zip(guess, result):
        if mark == "G":
            out += GREEN_TILE + f"[{letter}]" + RESET + " "
        elif mark == "Y":
            out += YELLOW_TILE + f"({letter})" + RESET + " "
        else:
            out += GRAY_TILE + f" {letter} " + RESET + " "
    return out


def check_code(guess, guesses):
    if guess == "":
        return "You didn't type anything. The code has 5 letters."
    if len(guess) != 5:
        return f"That has {len(guess)} characters. The code has 5 letters."
    for letter in guess:
        if not "A" <= letter <= "Z":
            return f"'{letter}' is not allowed. Use the letters A-Z only."
    if guess in [old for old, _ in guesses]:
        return f"You already tried {guess}."
    return ""


def code_panel(found_clue, found_letter, max_guesses=MAX_GUESSES):
    guesses = []
    message = ""
    while len(guesses) < max_guesses:
        lines = [BOLD + YELLOW + "=== SELF-DESTRUCT PANEL ===" + RESET, ""]
        if found_clue:
            lines.append("Clue: The last letter of the Greek alphabet - the end of everything.")
        else:
            lines.append("Clue: ??? (maybe the commander wrote it down somewhere)")
        lines += ["Code: _ _ _ G _" if found_letter else "Code: _ _ _ _ _", ""]
        for guess, result in guesses:
            lines.append("    " + tiles(guess, result))
        for _ in range(max_guesses - len(guesses)):
            lines.append("     _   _   _   _   _")
        left = max_guesses - len(guesses)
        lines += ["", f"Guesses left: {left}   (type BACK to leave the panel)", message]

        guess = screen.show(lines, "Type the 5-letter code > ").strip().upper()
        if guess == "BACK":
            return None
        message = check_code(guess, guesses)
        if message:
            message = RED + message + RESET
            continue
        guesses.append((guess, score_guess(guess, CODE)))
        if guess == CODE:
            return True
    return False


def control_room(max_guesses=MAX_GUESSES):
    found_clue = False
    found_letter = False
    message = "You reach the CONTROL ROOM. Find the self-destruct code!"
    while True:
        lines = [BOLD + YELLOW + "[ LEVEL 3: CONTROL ROOM ]" + RESET, "",
                 "Blinking consoles everywhere. In the middle stands the",
                 "SELF-DESTRUCT PANEL. A log and a broken screen are nearby.", "",
                 message, "",
                 "1. Read the commander's log",
                 "2. Check the broken screen",
                 "3. Use the self-destruct panel",
                 "quit = give up"]
        choice = screen.show(lines, "> ").strip().lower()

        if choice == "1":
            found_clue = True
            message = ("COMMANDER'S LOG: \"The code is the last letter of the Greek\n"
                       "alphabet - the end of everything.\"")
        elif choice == "2":
            found_letter = True
            message = "The broken screen flickers: CODE  _ _ _ G _"
        elif choice == "3":
            result = code_panel(found_clue, found_letter, max_guesses)
            if result is True:
                return True
            if result is None:
                message = "You step away from the panel. Look around for clues."
            else:
                message = RED + "WRONG CODE! Alarms blare. Try again!" + RESET
        elif choice == "quit":
            return False
        else:
            message = f"'{choice[:20]}' is not an option. Choose 1, 2 or 3."


STATION = [
    r"      _.-=========-._",
    r"   .-'   \   |   /  '-.",
    r"  <=[|== IRONWAKE ==|]=>       ==[>",
    r"   '-.   /   |   \  .-'",
    r"      `'-=========-'`",
]

BOOM = [
    r"     \    \  |  /    /",
    r"   --  ( * BOOM!! * )  --",
    r"  --- ( *** BOOM!! *** ) ---                   ==[>",
    r"   --  ( * BOOM!! * )  --",
    r"     /    /  |  \    \ ",
]


def ending():
    for title, picture in [("SELF-DESTRUCT IN 3...", STATION),
                           ("SELF-DESTRUCT IN 2...", STATION),
                           ("SELF-DESTRUCT IN 1...", STATION)]:
        screen.wait_for_size()
        print(screen.CLEAR + BOLD + YELLOW + title + RESET + "\n")
        print("\n".join(picture))
        time.sleep(1)
    screen.show([BOLD + YELLOW + "*** KABOOM ***" + RESET, ""] + BOOM
                + ["", BOLD + YELLOW + "The station is gone. You escaped! "
                   "MISSION COMPLETE!" + RESET], "(press ENTER) ")


def play(extra_guesses=0):
    if control_room(MAX_GUESSES + extra_guesses):
        ending()
        return True
    return False


if __name__ == "__main__":
    print("Escaped!" if play() else "Caught!")
