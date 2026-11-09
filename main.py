"""
GALAXY ESCAPE - full game.

Run:  python3 main.py

Flow:  Lobby  ->  Level 1  ->  Level 2 (maze)  ->  Level 3 (self-destruct code)
       ->  End credits (only if the player escapes)
"""

import Endcredit
import Lobby
import LV1
import LV2
import LV3
import Stealth
import screen

STEALTH_CHANCE = 0.5     # chance a guard shows up between two levels

RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def game_over():
    screen.wait_for_size()
    print("\033[2J\033[H", end="")
    print(RED + BOLD + "CAUGHT! The guards drag you away. GAME OVER." + RESET)


def credits():
    screen.ask("\n(press ENTER for the credits) ")
    try:
        Endcredit.play_credits()
    except KeyboardInterrupt:          # Ctrl+C skips the credits
        print(RESET + "\033[2J\033[H", end="")


def ask_play_again():
    """Ask "Play again?" until the answer is yes or no.

    Accepts y / yes / n / no in any capitals, with spaces around. Anything
    else (empty, "maybe", "1", ...) is an invalid answer: the game explains
    and asks again, instead of quitting by accident.
    """
    while True:
        answer = screen.ask("\nPlay again? (y/n) ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y (play again) or n (quit).")


def play_once():
    """One full run. Returns True if the player escapes."""
    Lobby.run()

    if not LV1.play():
        return False

    screen.wait_for_size()
    print("\033[2J\033[H", end="")
    screen.ask("Level 1 cleared! Level 2: find your way through the maze. "
               "(press ENTER) ")
    if not Stealth.quicktime(STEALTH_CHANCE):   # a guard may show up on the way
        return False
    if not LV2.run_level():
        return False

    if not Stealth.quicktime(STEALTH_CHANCE):   # ...and again before level 3
        return False
    return LV3.play()


def main():
    try:
        while True:
            if play_once():
                credits()
            else:
                game_over()
            if not ask_play_again():
                break
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C (KeyboardInterrupt) or Ctrl+D / end of input (EOFError):
        # leave cleanly instead of crashing with a traceback.
        print(RESET)
    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
