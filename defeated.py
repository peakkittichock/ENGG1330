from screen import BOLD, RED, RESET

# Game-over picture, shown in white every time the player loses.
DEAD = r"""
                  +###################+.
             -###+.        -#+        .+###-
          ####         .##########         +###
       .###         +#####+++++#####+         +##-
      ###    ##+-#########     +########+.##-   +##.
    +###########+#########     #########-############
   -##   .#####    .######-   .+####+     +####+   ##+
   ##.   -+##-                            .+##++    ##.
  +##     .#########-               +#########.     ###
  +##     .#########+               -#########-     ###
  -##      #######+.                  .+######.     ##+
   ##-   #####        -.         .+.       -####-  -##
    ##.   #####-   +######-   .#######-   #####-  .##-
     #####################     #####################.
      +##-   -+  +#######+     .#######+  .#   .###
        +##+         .++##########+-         +##+
           ###+        -##########        +###.
              -####+.      .#+      .+####-
                    -###############+"""

CAUGHT = "[You are caught and executed by the EMPIRE]"


def game_over_lines():
    """The picture in white with the caught message in red underneath."""
    lines = DEAD.split("\n")[1:]
    lines.append("")
    lines.append(" " * 9 + BOLD + RED + CAUGHT + RESET)
    return lines


if __name__ == "__main__":
    print("\n".join(game_over_lines()))
