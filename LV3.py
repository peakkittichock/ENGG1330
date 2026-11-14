import screen
from screen import BOLD, GREEN, RED, RESET, YELLOW

CODE = "KYBER"
MAX_GUESSES = 4

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


def board(found_clue, found_letter, guesses, max_guesses):
    lines = [BOLD + YELLOW + "=== SELF-DESTRUCT PANEL ===" + RESET, ""]
    if found_clue:
        lines.append("Clue: Think lightsaber.")
    else:
        lines.append("Clue: ??? (maybe the commander wrote it down somewhere)")
    lines += ["Code: _ _ _ E _" if found_letter else "Code: _ _ _ _ _", ""]
    for guess, result in guesses:
        lines.append("    " + tiles(guess, result))
    for _ in range(max_guesses - len(guesses)):
        lines.append("     _   _   _   _   _")
    return lines


def code_panel(found_clue, found_letter, guesses, max_guesses=MAX_GUESSES):
    # guesses is kept by the caller, so leaving the panel does not reset it.
    message = ""
    while len(guesses) < max_guesses:
        lines = board(found_clue, found_letter, guesses, max_guesses)
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
            # Show the all-green row before the credits roll.
            lines = board(found_clue, found_letter, guesses, max_guesses)
            lines += ["", GREEN + BOLD + "CODE ACCEPTED! Self-destruct sequence started." + RESET]
            screen.show(lines, "Press ENTER to escape> ")
            return True
    # Out of guesses: show the last board, then the level is lost.
    lines = board(found_clue, found_letter, guesses, max_guesses)
    lines += ["", RED + BOLD + "WRONG CODE! Alarms blare. Stormtroopers storm the room!" + RESET]
    screen.show(lines, "Press ENTER> ")
    return False


def control_room(max_guesses=MAX_GUESSES, has_hint=False):
    found_clue = False
    found_letter = has_hint
    guesses = []
    if has_hint:
        message = ("You reach the CONTROL ROOM. The hint you found in the tunnels\n"
                   "reads: CODE  _ _ _ E _")
    else:
        message = "You reach the CONTROL ROOM. Find the self-destruct code!"
    while True:
        lines = [BOLD + YELLOW + "[ LEVEL 3: CONTROL ROOM ]" + RESET, "",
                 "Blinking consoles everywhere. In the middle stands the",
                 "SELF-DESTRUCT PANEL. The commander's log lies nearby.", "",
                 message, "",
                 "1. Read the commander's log",
                 "2. Use the self-destruct panel",
                 "quit = give up"]
        choice = screen.show(lines, "> ").strip().lower()

        if choice == "1":
            found_clue = True
            message = "COMMANDER'S LOG: \"Think lightsaber.\""
        elif choice == "2":
            result = code_panel(found_clue, found_letter, guesses, max_guesses)
            if result is True:
                return True
            if result is False:
                return False
            message = "You step away from the panel. Look around for clues."
        elif choice == "quit":
            return False
        else:
            message = f"'{choice[:20]}' is not an option. Choose 1 or 2."


def play(extra_guesses=0, has_hint=False):
    return control_room(MAX_GUESSES + extra_guesses, has_hint)


if __name__ == "__main__":
    screen.start()
    print("Escaped!" if play() else "Caught!")
