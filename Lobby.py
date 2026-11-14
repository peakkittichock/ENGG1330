import os
import select
import sys

import screen
from screen import BOLD, CYAN, RESET, YELLOW

TITLEf1 = r"""
   .              .          '       *                 '           .       .
         .     ____  ___   _  _____ _   _   _________  _   ___
              |  _ \| __| /_\|_   _| |_| | / ____   _|/_\ | _ \
.             | |_) | _| / _ \ | | |  _  | \__ \ | | / _ \|   /____    .      .
              |____/|___|_/ \_\|_| |_| |_| |___/ |_|/_/ \_|__\_____|         .
                   *                                     .                    *
    '                     ___ ___  ___   _   ___ ___
                         | __/ __|/ __| /_\ | _ \ __|                '
                  '      | _|\__ \ (__ / _ \|  _/ _|____        .
          *              |_______/\___/_/ \_\_| |_______|          .         *
                                .              .          '               .  ."""

TITLEf2 = r"""
   .              .          '       '                 *           .       .
         .     ____  ___   _  _____ _   _   _________  _   ___
              |  _ \| __| /_\|_   _| |_| | / ____   _|/_\ | _ \
.             | |_) | _| / _ \ | | |  _  | \__ \ | | / _ \|   /____    .      .
              |____/|___|_/ \_\|_| |_| |_| |___/ |_|/_/ \_|__\_____|         .
                   '                                     .                    '
    *                     ___ ___  ___   _   ___ ___
                         | __/ __|/ __| /_\ | _ \ __|                *
                  '      | _|\__ \ (__ / _ \|  _/ _|____        .
          '              |_______/\___/_/ \_\_| |_______|          .         '
                                .              .          *               .  ."""

TAGLINE = "                      ~ Reach the X-wing within this station ~  *       *"

STATIONf1 = r'''
             .                                          *       .
                               _.-""""""""-._    .                   '
                  .          .' .-=-.______|_'.
        *                   /--( <>  )-|----|--\            .
                           |____'-=-'____|____|_|
      .              *     |---|--------|-------|    '                   *
            .               \-----|---------|--/
       .                .    '-_---|---|----_-'    .               .
                '               '-========-'             .             '
      *    .                                       *           .
                             *                           .             .'''

STATIONf2 = r'''
             .                                          '       .
                               _.-""""""""-._    .                   *
                  .          .' .-=-.______|_'.
        '                   /--( <>  )-|----|--\            .
                           |____'-=-'____|____|_|
      .              '     |---|--------|-------|    *                   '
            .               \-----|---------|--/
       .                .    '-_---|---|----_-'    .               .
                *               '-========-'             .             *
      '    .                                       '           .
                             '                           .             .'''

timegap = 1


def frame(title, station):
    return (BOLD + YELLOW + title[1:] + RESET + "\n" + TAGLINE + "\n"
            + CYAN + station[1:] + RESET).split("\n")


PLAY_PROMPT = " " * 29 + BOLD + "Press ENTER to play" + RESET


def twinkle():
    frames = [frame(TITLEf1, STATIONf1), frame(TITLEf2, STATIONf2)]
    if os.name == "nt" or not sys.stdin.isatty():
        screen.show(frames[0], PLAY_PROMPT)
        return
    print(screen.CLEAR, end="")
    i = 0
    while True:
        sys.stdout.write("\033[H" + "\n".join(frames[i % 2]) + "\n" + PLAY_PROMPT)
        sys.stdout.flush()
        if select.select([sys.stdin], [], [], timegap)[0]:
            sys.stdin.readline()
            return
        i += 1


def run():
    twinkle()
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
    "  Shoot every trooper on a 3 x 3 grid of doors without hitting an ally.",
    "  Type r1-r3 (a row), c1-c3 (a column) or 1-9 (one door).",
    "",
    heading("LEVEL 2 - THE MAINTENANCE TUNNELS"),
    "  Reach the exit (bottom-right) in 45 seconds. Arrow keys or w a s d, no",
    "  ENTER needed. Grab the crystal on the way: it reveals a code letter.",
    "",
    heading("LEVEL 3 - THE CONTROL ROOM"),
    "  Find clues, then guess the 5-letter self-destruct code in 4 tries.",
    "  Green [A] = right spot, yellow (A) = wrong spot, gray A = not in the code.",
    "",
    "  Between levels a guard may come: press the letter shown, fast!",
    "  Type quit in any level to give up (the guards catch you).",
    "  Ctrl+C leaves the game at any time.",
]


if __name__ == "__main__":
    screen.start()
    run()
