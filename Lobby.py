import screen
from screen import BOLD, CYAN, RESET, YELLOW

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


def run():
    welcome = (BOLD + YELLOW + TITLE[1:] + RESET + "\n" + TAGLINE + "\n"
               + CYAN + STATION[1:] + RESET).split("\n")
    screen.show(welcome, " " * 29 + BOLD + "Press ENTER to play" + RESET)
    screen.show(HOW_TO_PLAY, "  Press ENTER to start> ")


def heading(text):
    return "  " + BOLD + YELLOW + text + RESET


HOW_TO_PLAY = [
    BOLD + "HOW TO PLAY".center(79) + RESET,
    heading("THE STORY"),
    "  You were captured and brought aboard the battle station IRONWAKE. You",
    "  slipped away from your guards. The last ship leaves at midnight!",
    "",
    heading("LEVEL 1 - THE BLASTER RANGE"),
    "  Shoot every trooper on a 3 x 3 grid of doors without hitting a prisoner.",
    "  Type r1-r3 (a row), c1-c3 (a column) or 1-9 (one door).",
    "",
    heading("LEVEL 2 - THE MAINTENANCE TUNNELS"),
    "  Walk through a maze to the exit EX. Use the arrow keys or w a s d",
    "  (hold a key to keep going). No ENTER needed.",
    "",
    heading("LEVEL 3 - THE CONTROL ROOM"),
    "  Search the room for clues, then guess the 5-letter self-destruct code.",
    "  Green [A] = right spot, yellow (A) = wrong spot, gray A = not in the code.",
    "",
    "  Type quit in any level to give up (the guards catch you).",
    "  Ctrl+C leaves the game at any time.",
]


if __name__ == "__main__":
    run()
