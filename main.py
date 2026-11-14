import defeated
import Endcredit
import Lobby
import LV1
import LV2
import LV3
import screen
import Stealth
from screen import RESET


def play_once():
    Lobby.run()
    level1 = LV1.run_level1()
    if not level1["passed"]:
        return False
    if not Stealth.quicktime():
        return False
    if not LV2.play():
        return False
    if not Stealth.quicktime():
        return False
    return LV3.play(extra_guesses=1 if level1["bonus_guess"] else 0,
                    has_hint=LV2.found_hint)


def ask_play_again(lines):
    note = ""
    while True:
        answer = screen.show(lines + [note], "Play again? (y/n) ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        note = "Please type y (play again) or n (quit)."


def main():
    try:
        while True:
            if play_once():
                Endcredit.play_credits()
                lines = ["You escaped from the Death Star!", ""]
            else:
                lines = defeated.game_over_lines()
            if not ask_play_again(lines):
                break
    except (KeyboardInterrupt, EOFError):
        pass
    print(RESET + "\nThanks for playing!")


if __name__ == "__main__":
    main()