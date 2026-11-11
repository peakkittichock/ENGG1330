import screen
from screen import BOLD, CYAN, GREEN, RED, RESET, YELLOW

TROOPER = "S"
ARMORED = "A"
PRISONER = "P"
EMPTY = "."

WHITE = "\033[97m"
DIM = "\033[2m"

SPRITES = {
    TROOPER: ([" [o o] ", "  |=|  "], BOLD + WHITE),
    ARMORED: (["=[o o]=", " |###| "], BOLD + CYAN),
    PRISONER: ([" .-=-. ", " |___| "], BOLD + YELLOW),
    EMPTY: (["       ", "   .   "], DIM),
}

MOVES = ["r1", "r2", "r3", "c1", "c2", "c3"] + ["d" + str(n) for n in range(1, 10)]

LEVELS = [
    {"title": "Warm up", "shots": 2,
     "grid": ["SSS",
              ".P.",
              "S.."]},
    {"title": "Armor plating", "shots": 4,
     "grid": ["SPA",
              "...",
              "PSA"]},
    {"title": "Double trouble", "shots": 4,
     "grid": ["ASA",
              "SPS",
              "A.A"]},
]

earned_bonus = False


def make_grid(level):
    return [list(row) for row in level["grid"]]


def parse_move(text):
    text = text.replace(" ", "").lower()
    if text in MOVES[:6]:
        return text
    if len(text) == 1 and text in "123456789":
        return "d" + text
    return None


def cells_hit(move):
    n = int(move[1])
    if move[0] == "r":
        return [(n - 1, col) for col in range(3)]
    if move[0] == "c":
        return [(row, n - 1) for row in range(3)]
    return [((n - 1) // 3, (n - 1) % 3)]


def count_troopers(grid):
    return sum(row.count(TROOPER) + row.count(ARMORED) for row in grid)


def fire(grid, move):
    downed = cracked = prisoners = 0
    for r, c in cells_hit(move):
        if grid[r][c] == TROOPER:
            grid[r][c] = EMPTY
            downed += 1
        elif grid[r][c] == ARMORED:
            grid[r][c] = TROOPER
            cracked += 1
        elif grid[r][c] == PRISONER:
            grid[r][c] = EMPTY
            prisoners += 1
    return downed, cracked, prisoners


def find_plan(grid, shots):
    if count_troopers(grid) == 0:
        return []
    if shots == 0:
        return None
    for move in MOVES:
        hit = [grid[r][c] for r, c in cells_hit(move)]
        if PRISONER in hit or (TROOPER not in hit and ARMORED not in hit):
            continue
        copy = [row[:] for row in grid]
        fire(copy, move)
        rest = find_plan(copy, shots - 1)
        if rest is not None:
            return [move] + rest
    return None


def describe(move):
    return {"r": "row ", "c": "column ", "d": "door "}[move[0]] + move[1]


def board_lines(grid):
    pad = " " * 24
    lines = [pad + "       c1      c2      c3"]
    for r in range(3):
        doors = [str(r * 3 + c + 1) for c in range(3)]
        lines.append(pad + "    +---" + "---+---".join(doors) + "---+")
        for k in range(2):
            label = "r" + str(r + 1) + "  " if k == 0 else "    "
            cells = [SPRITES[grid[r][c]][1] + SPRITES[grid[r][c]][0][k] + RESET
                     for c in range(3)]
            lines.append(pad + label + "|" + "|".join(cells) + "|")
    lines.append(pad + "    +-------+-------+-------+")
    return lines


def round_lines(number, level, grid, shots, message):
    title = f"LEVEL 1: THE BLASTER RANGE    Round {number} of {len(LEVELS)}: {level['title']}"
    status = f"Shots left: {shots}    Troopers left: {count_troopers(grid)}"
    legend = ("[o o] trooper    =[o o]= armored (2 hits)    "
              ".-=-. prisoner (don't shoot!)")
    return ([BOLD + YELLOW + title.center(79) + RESET, status.center(79), ""]
            + board_lines(grid)
            + ["", legend.center(79), "", "  " + message, "",
               "  r1-r3 = row   c1-c3 = column   1-9 = one door   hint   quit"])


INTRO = [
    BOLD + YELLOW + "LEVEL 1: THE BLASTER RANGE".center(79) + RESET,
    "",
    "  You grab a blaster from a sleeping guard. Ahead is the cell block:",
    "  nine doors, some with troopers in front, some with prisoners inside.",
    "",
    "  Shoot every trooper. Never hit a prisoner.",
    "  A bolt flies along a whole row or column, so pick your lines well.",
    "  Armored troopers need 2 hits. Each round gives you only a few shots.",
    "",
    "    r1 r2 r3    shoot along a row",
    "    c1 c2 c3    shoot down a column",
    "    1 to 9      shoot one door (numbered row by row)",
    "    hint        show one safe shot",
    "    quit        give up",
    "",
    "  Clear all " + str(len(LEVELS)) + " rounds without hitting a prisoner and you get",
    "  one extra guess at the self-destruct panel in Level 3.",
]


def play_round(number, level):
    grid = make_grid(level)
    shots = level["shots"]
    message = "Fire when ready."
    while True:
        answer = screen.show(round_lines(number, level, grid, shots, message), "Fire> ")
        command = answer.strip().lower()
        if command == "quit":
            return "quit"
        if command == "hint":
            plan = find_plan(grid, shots)
            if plan:
                message = "Hint: try " + describe(plan[0]) + "."
            else:
                message = "No safe plan left. Waste your shots to restart the round."
            continue

        move = parse_move(command)
        if move is None:
            message = YELLOW + f"'{command[:15]}' is not a shot. Try r1, c2 or 5." + RESET
            continue
        if all(grid[r][c] == EMPTY for r, c in cells_hit(move)):
            message = YELLOW + "Nothing to hit there. That shot was not used." + RESET
            continue

        shots -= 1
        downed, cracked, prisoners = fire(grid, move)
        message = (f"You shot {describe(move)}: {downed} down, "
                   f"{cracked} armor cracked.")

        if prisoners:
            result = "prisoner"
            message = RED + "You hit a prisoner! ROUND FAILED." + RESET
        elif count_troopers(grid) == 0:
            result = "cleared"
            message = GREEN + message + " ROUND CLEARED!" + RESET
        elif shots == 0:
            result = "failed"
            message = RED + message + " Out of shots. ROUND FAILED." + RESET
        else:
            continue

        prompt = "Press ENTER to continue> " if result == "cleared" else "Press ENTER to retry> "
        answer = screen.show(round_lines(number, level, grid, shots, message), prompt)
        if answer.strip().lower() == "quit":
            return "quit"
        return result


def play():
    global earned_bonus
    earned_bonus = False
    hit_prisoner = False

    if screen.show(INTRO, "Press ENTER to start> ").strip().lower() == "quit":
        return False
    for number, level in enumerate(LEVELS, start=1):
        while True:
            result = play_round(number, level)
            if result == "quit":
                return False
            if result == "prisoner":
                hit_prisoner = True
            if result == "cleared":
                break

    earned_bonus = not hit_prisoner
    lines = ["", GREEN + BOLD + "  The cell block is clear!" + RESET, "",
             "  The prisoners point you to a hatch in the floor:",
             "  the maintenance tunnels lead to the control room."]
    if earned_bonus:
        lines += ["", GREEN + "  No prisoner was hurt. Bonus: one extra guess in Level 3!" + RESET]
    screen.show(lines, "Press ENTER to enter the tunnels> ")
    return True


if __name__ == "__main__":
    print("Cleared!" if play() else "You gave up.")
