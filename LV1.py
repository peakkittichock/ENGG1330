import screen

CLEAR = "\033[2J\033[H"
MOVES = "r1 r2 r3 c1 c2 c3 d1 d2 d3 d4 d5 d6 d7 d8 d9".split()
MAX_ALLY_HITS = 2

SPRITES = {
    "S": (" [o o] ", "  |=|  ", "1;97"),
    "A": ("=[o o]=", " |###| ", "1;36"),
    "R": (" .-=-. ", " |___| ", "1;33"),
    ".": ("       ", "   .   ", "2"),
}

LEVELS = [
    {"title": "Warm up", "shots": 2, "belts": [], "grid": ["SSS", ".R.", "S.."],
     "tip": "Tip: one bolt hits a whole row or a whole column."},
    {"title": "Armor plating", "shots": 4, "belts": [], "grid": ["SRA", "...", "RSA"],
     "tip": "Tip: armored stormtroopers take 2 hits. The first hit cracks them."},
    {"title": "The conveyor", "shots": 3, "belts": [1], "grid": ["RSS", ".S.", "SR."],
     "tip": "Tip: a row marked >> slides one door right after every shot."},
    {"title": "Double trouble", "shots": 4, "belts": [1], "grid": ["SSR", "..S", "R.A"],
     "tip": "Tip: armor and a sliding belt together. Think two shots ahead."},
]

LEGEND = "[o o] stormtrooper   =[o o]= armored (2 hits)   .-=-. rebel pilot"
COMMANDS = "Commands: r1 r2 r3, c1 c2 c3, 1 to 9, hint, reset, help, quit"


class Quit(Exception):
    pass


# ---------------------------------------------------------------- game rules
def parse_move(text):
    text = text.replace(" ", "").lower()
    if len(text) == 1 and text in "123456789":
        return "d" + text                       # a bare number means one door
    if len(text) == 2 and text[0] in "rcd" and text[1] in "123456789":
        if text[0] != "d" and text[1] > "3":    # there are only 3 rows and 3 columns
            return None
        return text
    return None


def cells(move):
    n = int(move[1]) - 1
    if move[0] == "r":
        return [(n, c) for c in range(3)]
    if move[0] == "c":
        return [(r, n) for r in range(3)]
    return [(n // 3, n % 3)]


def name(move):
    return {"r": "row", "c": "column", "d": "door"}[move[0]] + " " + move[1]


def left(grid):
    return sum(row.count("S") + row.count("A") for row in grid)


def fire(grid, move):
    troopers = allies = 0
    for r, c in cells(move):
        if grid[r][c] in "SA":
            troopers += 1
            grid[r][c] = "." if grid[r][c] == "S" else "S"
        elif grid[r][c] == "R":
            allies += 1
            grid[r][c] = "."
    return troopers, allies


def slide(grid, belts):
    for r in belts:
        grid[r] = [grid[r][-1]] + grid[r][:-1]


def find_plan(grid, shots, belts):
    if left(grid) == 0:
        return []
    if shots == 0:
        return None
    for move in MOVES:
        hit = [grid[r][c] for r, c in cells(move)]
        if "R" in hit or ("S" not in hit and "A" not in hit):
            continue                            # would hit an ally, or no trooper
        copy = [row[:] for row in grid]
        fire(copy, move)
        slide(copy, belts)
        rest = find_plan(copy, shots - 1, belts)
        if rest is not None:
            return [move] + rest
    return None


# ------------------------------------------------------------------- drawing
def paint(text, code):
    if screen.COLOR and code and text:
        return "\033[" + code + "m" + text + "\033[0m"
    return text


def centered(text, code=""):
    return paint(text.center(79).rstrip(), code)


def board_lines(grid, belts):
    pad = " " * 27
    lines = [pad + "   c1      c2      c3"]
    for r in range(3):
        top, upper, lower = pad + "+", "", ""
        # On a belt row the walls become arrows: everything moves one door right.
        wall = paint(">", "1;33") if r in belts else "|"
        for c in range(3):
            first, second, code = SPRITES[grid[r][c]]
            top += "-%d:%s---+" % (r * 3 + c + 1, paint(grid[r][c], code))
            upper += paint(first, code) + wall
            lower += paint(second, code) + "|"
        if r in belts:
            upper += paint(" door %d wraps to door %d" % (r * 3 + 3, r * 3 + 1), "1;33")
        label = "r%d%s" % (r + 1, ">>" if r in belts else "  ")
        lines += [top, pad[:-4] + label + "|" + upper, pad[:-4] + "    |" + lower]
    return lines + [pad + "+-------+-------+-------+"]


def round_screen(number, level, grid, shots, strikes, message, footer):
    title = "STAGE 1: BLASTER TRAINING   Round %d of %d: %s" % (
        number, len(LEVELS), level["title"])
    status = "Shots left: %d    Allies hit: %d/%d    Stormtroopers left: %d" % (
        shots, strikes, MAX_ALLY_HITS, left(grid))
    return ([centered(title, "1;33"), centered(status), ""]
            + board_lines(grid, level["belts"])
            + ["", centered(LEGEND), centered(level["tip"], "36"), "",
               "  " + paint(message[0], message[1]), "", centered(footer[0], footer[1])])


def show(lines, prompt):
    screen.wait_for_size()
    print(CLEAR + "\n".join(lines + [""] * (22 - len(lines))))
    answer = input(prompt).strip().lower()
    if answer == "quit":
        raise Quit
    return answer


# ----------------------------------------------------------------- game flow
INTRO = [
    centered("STAGE 1: BLASTER STRATEGY GAME", "1;33"), "",
    "  Cadet, the Empire has captured you, A REBEL! Only the right final code",
    "  can help you escape. First, you need to prove you can handle a blaster.",
    "  Hit every stormtrooper target, but hold your fire on our REBEL allies.",
    "  I will give you the access card to enter the base.", "",
    "  HOW TO PLAY", centered(LEGEND),
    "  Every shot costs 1 charge and hits everything in its line, friend or foe.",
    "  Armored stormtroopers need 2 hits. IMPORTANT! Rows marked >> slide right",
    "  by one position after every shot.",
    "    r1 r2 r3   fire along a row         c1 c2 c3   fire down a column",
    "    1 to 9     fire at one door (numbered row by row)",
    "    hint, reset, help and quit also work.",
    "  Clear every stormtrooper. Hitting %d allies fails the round." % MAX_ALLY_HITS,
    "  Pass all %d rounds to earn the access card." % len(LEVELS)]


def play_round(number, level):
    allies_hit = 0
    while True:                                 # each pass is one attempt
        grid = [list(row) for row in level["grid"]]
        shots, strikes = level["shots"], 0
        message = ("Instructor: Fire when ready, cadet. Type help for commands.", "36")
        while True:
            answer = show(round_screen(number, level, grid, shots, strikes, message,
                                       (COMMANDS, "")), "Fire> ")
            move = parse_move(answer)
            if answer == "reset":
                break
            elif answer == "help":
                show(INTRO, "Press Enter to go back> ")
                message = ("Back on the range.", "36")
            elif answer == "hint":
                plan = find_plan(grid, shots, level["belts"])
                text = ("Hint: a safe shot is " + name(plan[0]) + "." if plan
                        else "No safe plan is left. Type reset to try again.")
                message = (text, "36")
            elif move is None:
                message = ("'" + answer[:10] + "' is not a valid command. "
                           "Try r1, c2, 5 or help.", "33")
            elif all(grid[r][c] == "." for r, c in cells(move)):
                message = ("Nothing to hit at " + name(move) + ". Shot not used.", "33")
            else:
                # A real shot: fire, then let the belts slide.
                shots -= 1
                stormtroopers, allies = fire(grid, move)
                slide(grid, level["belts"])
                strikes += allies
                allies_hit += allies
                text = "Fired at %s. Stormtroopers hit: %d." % (name(move), stormtroopers)
                if allies:
                    text += " Allies hit: %d!" % allies
                if level["belts"]:
                    text += " Belt slides right."
                message = (text, "1;31" if allies else "1;32")

                # Is the round over?
                footer = None
                if strikes >= MAX_ALLY_HITS:
                    footer = ("ROUND FAILED: too many allies hit.", "1;31")
                elif left(grid) == 0:
                    footer = ("ROUND CLEARED!", "1;32")
                elif shots == 0:
                    footer = ("ROUND FAILED: out of charge.", "1;31")
                if footer:
                    show(round_screen(number, level, grid, shots, strikes, message,
                                      footer), "Press Enter to continue> ")
                    if "CLEARED" in footer[0]:
                        return allies_hit
                    break                       # failed: the round starts again


def win_screen(allies_hit):
    card = ["+---------------------+", "|  ACCESS CARD EARNED |", "+---------------------+"]
    lines = [centered(line, "1;32") for line in card] + [
        "", "  Good shooting, cadet! Take this access card and press ENTER to use it to",
        "  enter the next level. The next level will involve a tunnel/maze, be",
        "  careful of the countdown. Be quick to find the STAR, which leads to the",
        "  final vault. There will be a purple orb, which is a crystal, which gives A HINT to the final",
        "  stage. Collect it by passing through it!",
        "  Use WASD and/or arrow keys to navigate. GOOD LUCK!", "",
        "  Allies hit: %d" % allies_hit]
    if allies_hit == 0:
        lines += ["", "  " + paint("Bonus: one extra guess in the final battle!", "1;32")]
    return lines


def run_stage1():
    allies_hit = 0
    try:
        show(INTRO, "Press Enter to begin> ")
        for number, level in enumerate(LEVELS, start=1):
            allies_hit += play_round(number, level)
        show(win_screen(allies_hit), "Press Enter to enter the base> ")
    except (Quit, EOFError, KeyboardInterrupt):
        print(CLEAR + "Training ended. Run the program again to restart.")
        return {"passed": False, "bonus_guess": False}
    return {"passed": True, "bonus_guess": allies_hit == 0}


if __name__ == "__main__":
    print(CLEAR + "Stage 1 finished. Result: " + str(run_stage1()))