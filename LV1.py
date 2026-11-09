# Lv 1 : PLACEHOLDER - teammate will replace this with the real level.
#
# Contract with main.py: keep a function play() that returns
#   True  -> player cleared the level (game moves on to level 2)
#   False -> player failed / quit     (game over)

import screen

BOLD = "\033[1m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def clear():
    print("\033[2J\033[H", end="")


def play():
    message = ""

    def draw():
        print(BOLD + YELLOW + "[ LEVEL 1: HOLDING CELL ]" + RESET)
        print()
        print("(Level 1 is still under construction.)")
        print()
        print("1. Escape the cell")
        print("2. Give up")
        print(message)

    while True:
        screen.wait_for_size()        # pause if the window is under 80 x 24
        clear()
        draw()
        choice = screen.ask("> ", draw).strip()
        if choice == "1":
            return True
        if choice == "2":
            return False
        message = "Choose 1 or 2."


if __name__ == "__main__":
    play()
