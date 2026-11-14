import time

import screen
from screen import BOLD, RESET, YELLOW

ROWS = 22
WIDTH = 79
SPEED = 0.35

# The Ironwake blows up. Each entry is (frame, seconds to hold it).
# Strings use ''' because the ship drawing contains """.
EXPLOSION = [
    (r'''
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
                             '                           .             .''', 1.5),
    (r'''
             .                                          '       .
                               _.-""""""""-._    .                   *
                  .          .' .-=-.______|_'.
        '                   /--( <>  )-|----|--\            .
                           |____'-=-'____|____|_|
      .              '     |---|--------|-------|    *                   '
            .               \-----|------|--|--/
       .                .    '-_---|---|-+--_-'    .               .
                *               '-=======|-'             .             *
      '    .                                       '           .
                             '                           .             .''', 0.5),
    (r'''
             .                                          '       .
                               _.-""""""""-._    .                   *
                  .          .' .-=-.______|_'.
        '                   /--( <>  )-|----|--\            .
                           |____'-=-'____|____|_|
      .              '     |---|--------\-------|    *                   '
            .               \-----|----(\|/)/--/
       .                .    '-_---|--((-o-))-'    .               .
                *               '-======/|\'             .             *
      '    .                          /' | '\      '           .
                             '                           .             .''', 0.5),
    (r'''
             .                                          '       .
                               _.-""""""""-._    .                   *
                  .          .' .-=-.______|_'.
        '                   /--( <>  )-|----|--\            .
                           |____'-=-'____|____|_|
      .              '     |---|--------\--]]]--|    *                   '
            .               \-----|----(\|/)/--/ ]]
       .            -------------[[[[[(({G-})-]]]]-----------      .
                *            == '-=[[[==/|\'\.}}} ===    .             *
      '    .                  <.   .'./' | '\.\\  ""           .
                             '    // /  /  \   \\\       .             .''', 0.5),
    (r'''
             .                   #       |              '       .
                               _.#"""""""|-._    .                   *
                  .          .' .#=##____|_|_'.
        '             ========-(#{} #)===|\=============      .
                           |____#-##'/--[[]]}-\-________
      .              '     |---|--#-{[}]##-]]]--|    *                   '
            .               \-----[{[{######/--/ ]]
       .    ------------=========[#[[####O####]]]]==========----------
                *            == '-=[[[=######.}}} ===    .             *
      '    .                  <.   .'./' | '\.\\  ""           .
                             '    // /  /  \   \\\       .             .''', 0.5),
    (r'''
             .                   #       |              '       .
                               _.#"""""""|-._    .                   *
                  .          .' .#=##____|_|_'.
        '             ========-(#{} #)===|\=============      .
                           |____#-##'/--[[]]}-\-________
      .              '     |---|--#-{[}]##-]]]--|    *                   '
            .               \-----[{[{######/--/ ]]
       .    ------------=========[#[[####O####]]]]==========----------
                *            == '-=[[[=######.}}} ===    .             *
      '    .                  -.   .'./' | '\.\\  ""           .
                             '  / /   / /  \    \ \      .             .''', 0.5),
    (r'''
             .                                          '       .
                               _.##"""""" -._    .                   *
                  .          .'###=###___|_|_'.
        '    ----=============(=+{#}=####\=============---------
                           |__###-##'####[]]}-\-________
      .              '     |---|\_&&/[}]##-]]]--|    *                   '
            .               \-----[{[{######/--/ ]]
       .    ------------=========[#[[#**#*##****]]==========----------
                *             :   - \ =+==++ "/  >- .    .             *
      '    .                   .       - _ . '  '              .
                             '  .     "    .        -    .             .''', 0.6),
    (r'''
             .                                          '       .
                               _.__"'""''-. ,    .                   *
                  .          .'#########
        '    --  ======   ===#####0########   #=====  =----   --
                           |___########-[[]]}-\-________
      .              '     |---|\_&&/[}]##-]]]--|    *                   '
            .                  --= +* `~-   ~--/ -..
       .    --  ----    === === '/.  " <  / ` ~ -   ====  =--- ---- -
                *                 - \ =  =+  "   `       .             *
      '    .                             ,                     .
                                                    '    .             .''', 0.7),
    (r'''
             .                                          '       .
                               _ _     ' -. ,    .                   *
                  .          .  /#######    .
        '          -=     ==################## =  -=  =
                           ####################-__
      .              '     ##*-#\_&&/##]##-]]###|    *                   '
            .                # --= +* #~-   #--/ -#.
       .          --    =    -  #-   .  ,#    ~ -   =        - -
                *                                        .             *
      '    .                                                   .
                                                         .             .''', 1.0),
    (r'''
             .                                          '       .
                                 _     '         .                   *
                  .          .   #######    .
        '                   ##################
                           #%%##^#%%%%###$$##^#
      .              '    ~`# &%--+== _ &%=- $@      *                   '
            .

       .
                *                                        .             *
      '    .                                                   .
                                                         .             .''', 1.0),
    (r'''
             .                                          '       .
                                                 .                   *
                  .              #######
        '                   ##%^#%#%%#^-%%%%##
                           #^. @''`  - `  & +=$_
      .              '                               *                   '
            .

       .
                *                                        .             *
      '    .                                                   .
                                                         .             .''', 1.0),
    (r'''
             .                                          '       .
                                                 .                   *
                  .              _-##*##^
        '                   -  +=`  ~  % $@ ! .


      .              '                               *                   '
            .

       .
                *                                        .             *
      '    .                                                   .
                                                         .             .''', 1.0),
    (r'''
             .                                          '       .
                                                 .                   *
                  .                -# #*
        '



      .              '                               *                   '
            .

       .
                *                                        .             *
      '    .                                                   .
                                                         .             .''', 1.0),
    (r'''
             .                                          '       .
                                                 .                   *
                  .
        '



      .              '                               *                   '
            .

       .
                *                                        .             *
      '    .                                                   .
                                                         .             .''', 1.5),
    (r'''
             .           .        '                     '       .
                                       `         .                   *
                  .        +
        '                    .             +
                                   '
      .              '                        .      *                   '
            .
       .                .      '    +     `
                *                                        .             *
      '    .                +               .                  .
                                              +          .             .''', 1.0),
    (r'''
             .           .        '                     '       .
                                       `         .                   *
                  .       *
        '                    .             *
                                   '
      .              '                        .      *                   '
            .
       .                .      '    *     `
                *                                        .             *
      '    .                *               .                  .
                                              *          .             .''', 1.0),
]


STARS = EXPLOSION[-1][0].split("\n")[1:]

CREDITS = [
    "THE DEATHSTAR FALLS SILENT",
    "",
    "Before it exploded, you found a ship...",
    "You found an X-Wing outside the final vault...",
    "and FLEW OFF the death star,",
    "into the galaxy, far, far away",
    "",
    "Against all odds, one small ship",
    "slips out of the hangar at midnight",
    "and disappears into the stars.",
    "",
    "The GALAXY is safe.",
    "",
    "",
    "* DEATHSTAR ESCAPE *",
    "",
    "",
    "A GAME BY",
    "ENGG1330 GROUP 7  -  SUBCLASS 1B",
    "",
    "Krittichok Khanthithao",
    "Leung Ho Long Ryan",
    "Lord Mensah Kojo Tandoh",
    "Antonio Sutowo",
    "",
    "",
    "Made for ENGG1330 Group Project",
    "The University of Hong Kong, 2026",
    "",
    "",
    "THANK YOU FOR PLAYING",
]


def fit(line):
    return line.rstrip()[:WIDTH].ljust(WIDTH)


def frame_lines(art):
    lines = [fit(line) for line in art.split("\n")[1:]]
    top = (ROWS - len(lines)) // 2
    return [" " * WIDTH] * top + lines + [" " * WIDTH] * (ROWS - top - len(lines))


def star_row(row):
    return fit(STARS[row % len(STARS)])


def over_stars(row, text, colour=YELLOW):
    # Put centred text on top of the starfield row, keeping stars on both sides.
    stars = star_row(row)
    if not text:
        return stars
    text = " " + text + " "
    start = (WIDTH - len(text)) // 2
    return stars[:start] + colour + text + RESET + stars[start + len(text):]


def draw(lines):
    print("\033[H" + "\n".join(lines), flush=True)


def play_explosion():
    for art, delay in EXPLOSION:
        draw(frame_lines(art))
        time.sleep(delay)


def play_scroll():
    for step in range(len(CREDITS) + ROWS):
        lines = []
        for row in range(ROWS):
            i = row + step - ROWS
            text = CREDITS[i] if 0 <= i < len(CREDITS) else ""
            lines.append(over_stars(row, text))
        draw(lines)
        time.sleep(SPEED)


def play_credits():
    print(screen.CLEAR, end="")
    play_explosion()
    play_scroll()
    lines = [over_stars(row, "") for row in range(ROWS)]
    lines[ROWS // 2] = over_stars(ROWS // 2, "[ THE END ]", BOLD + YELLOW)
    screen.show(lines, " " * 29 + "Press ENTER to finish")


if __name__ == "__main__":
    screen.start()
    play_credits()
