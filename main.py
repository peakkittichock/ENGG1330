import Endcredit
import Lobby
import LV1
import LV2
import LV3
import screen
import Stealth
from screen import BOLD, RED, RESET


def play_once():
    Lobby.run()
    if not LV1.play():
        return False
    if not Stealth.quicktime(1):
        return False
    if not LV2.play():
        return False
    if not Stealth.quicktime(0.5):
        return False
    return LV3.play(extra_guesses=1 if LV1.earned_bonus else 0)


def ask_play_again(message):
    note = ""
    while True:
        answer = screen.show([message, "", note], "Play again? (y/n) ").strip().lower()
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
                message = "You escaped from IRONWAKE!"
            else:
                message = RED + BOLD + "CAUGHT! The guards drag you away. GAME OVER." + RESET
            if not ask_play_again(message):
                break
    except (KeyboardInterrupt, EOFError):
        pass
    print(RESET + "\nThanks for playing!")


if __name__ == "__main__":
    main()
