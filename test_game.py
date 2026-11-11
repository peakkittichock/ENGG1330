import contextlib
import io
import os
import re
import unittest
from collections import deque
from unittest import mock

import Endcredit
import Lobby
import LV1
import LV2
import LV3
import main
import screen


class FakePlayer:

    def __init__(self, test, answers):
        self.test = test
        self.answers = list(answers)

    def show(self, lines, prompt="> "):
        rows = "\n".join(lines).split("\n")
        self.test.assertLessEqual(len(rows), 22, "screen too tall")
        for row in rows + [prompt]:
            self.test.assertLessEqual(len(re.sub(r"\033\[[0-9;]*m", "", row)), 79, row)
        if not self.answers:
            raise AssertionError("the game asked for more input than planned")
        return self.answers.pop(0)


def play(test, function, answers, *args):
    player = FakePlayer(test, answers)
    with mock.patch.object(screen, "show", player.show), \
            mock.patch("time.sleep"), \
            contextlib.redirect_stdout(io.StringIO()):
        result = function(*args)
    test.assertEqual(player.answers, [], "not every answer was used")
    return result


def solution(level):
    return LV1.find_plan(LV1.make_grid(level), level["shots"])


def perfect_run():
    answers = [""]
    for level in LV1.LEVELS:
        typed = [m[1] if m[0] == "d" else m for m in solution(level)]
        answers += typed + [""]
    return answers + [""]


class TestLevel1(unittest.TestCase):

    def test_each_round_needs_exactly_its_shots(self):
        for level in LV1.LEVELS:
            grid = LV1.make_grid(level)
            self.assertIsNotNone(solution(level), level["title"])
            self.assertIsNone(LV1.find_plan(grid, level["shots"] - 1), level["title"])

    def test_parse_move(self):
        self.assertEqual(LV1.parse_move("r1"), "r1")
        self.assertEqual(LV1.parse_move(" C 2 "), "c2")
        self.assertEqual(LV1.parse_move("5"), "d5")
        for bad in ["", "r4", "c0", "0", "10", "x1", "fire"]:
            self.assertIsNone(LV1.parse_move(bad), bad)

    def test_armored_trooper_needs_two_hits(self):
        grid = [list("A.."), list("..."), list("...")]
        self.assertEqual(LV1.fire(grid, "d1"), (0, 1, 0))
        self.assertEqual(LV1.fire(grid, "d1"), (1, 0, 0))
        self.assertEqual(LV1.count_troopers(grid), 0)

    def test_perfect_run_earns_bonus(self):
        self.assertTrue(play(self, LV1.play, perfect_run()))
        self.assertTrue(LV1.earned_bonus)

    def test_invalid_shots_cost_nothing(self):
        answers = perfect_run()
        answers[1:1] = ["zzz", "r9", "", "4", "hint"]
        self.assertTrue(play(self, LV1.play, answers))

    def test_hitting_a_prisoner_fails_the_round(self):
        answers = perfect_run()
        answers[1:1] = ["c2", ""]
        self.assertTrue(play(self, LV1.play, answers))
        self.assertFalse(LV1.earned_bonus)

    def test_running_out_of_shots_retries_the_round(self):
        answers = perfect_run()
        answers[1:1] = ["1", "2", ""]
        self.assertTrue(play(self, LV1.play, answers))
        self.assertTrue(LV1.earned_bonus)

    def test_quit(self):
        self.assertFalse(play(self, LV1.play, ["quit"]))
        self.assertFalse(play(self, LV1.play, ["", "quit"]))


def route(grid, start, goal):
    came_from = {start: None}
    queue = deque([start])
    while queue:
        pos = queue.popleft()
        for key, (dr, dc) in LV2.MOVES.items():
            nxt = (pos[0] + dr, pos[1] + dc)
            if grid[nxt[0]][nxt[1]] == LV2.PATH and nxt not in came_from:
                came_from[nxt] = (pos, key)
                queue.append(nxt)
    if goal not in came_from:
        return None
    keys = ""
    while came_from[goal]:
        goal, key = came_from[goal]
        keys = key + keys
    return keys


START = (1, 1)
GOAL = (LV2.GRID_H - 2, LV2.GRID_W - 2)


class TestLevel2(unittest.TestCase):

    def test_border_is_wall(self):
        grid = LV2.carve_maze()
        for c in range(LV2.GRID_W):
            self.assertEqual(grid[0][c], LV2.WALL)
            self.assertEqual(grid[-1][c], LV2.WALL)
        for row in grid:
            self.assertEqual(row[0], LV2.WALL)
            self.assertEqual(row[-1], LV2.WALL)

    def test_exit_can_always_be_reached(self):
        for _ in range(20):
            self.assertIsNotNone(route(LV2.carve_maze(), START, GOAL))

    def test_wall_stops_the_walk(self):
        grid = LV2.carve_maze()
        path, hit_wall = LV2.walk(grid, START, "w", GOAL)
        self.assertEqual(path, [])
        self.assertTrue(hit_wall)

    def test_win_with_bad_input_and_new_maze(self):
        grid = LV2.carve_maze()
        keys = route(grid, START, GOAL)
        answers = ["", "xyz", "w", "r", keys, ""]
        with mock.patch.object(LV2, "carve_maze", return_value=grid):
            self.assertTrue(play(self, LV2.play, answers))

    def test_quit(self):
        self.assertFalse(play(self, LV2.play, ["quit"]))
        self.assertFalse(play(self, LV2.play, ["q", "q"]))

    def test_one_q_only_asks(self):
        grid = LV2.carve_maze()
        answers = ["q", "r", "q", route(grid, START, GOAL), ""]
        with mock.patch.object(LV2, "carve_maze", return_value=grid):
            self.assertTrue(play(self, LV2.play, answers))

    def test_arrow_keys(self):
        import os
        read_end, write_end = os.pipe()
        os.write(write_end, b"\x1b[A\x1b[B\x1b[C\x1b[DD\x1b")
        keys = [LV2.read_key(read_end) for _ in range(6)]
        os.close(write_end)
        os.close(read_end)
        self.assertEqual(keys, ["w", "s", "d", "a", "d", ""])


WRONG = ["BUILT", "CRANE", "PLUSH", "DIRTY", "FJORD", "WOVEN"]


class TestLevel3(unittest.TestCase):

    def score(self, guess, answer):
        return "".join(LV3.score_guess(guess, answer))

    def test_scoring(self):
        self.assertEqual(self.score("OMEGA", "OMEGA"), "GGGGG")
        self.assertEqual(self.score("BUILT", "OMEGA"), "_____")
        self.assertEqual(self.score("AGEMO", "OMEGA"), "YYGYY")

    def test_repeated_letters(self):
        self.assertEqual(self.score("EEEEE", "OMEGA"), "__G__")
        self.assertEqual(self.score("LLAMA", "HELLO"), "YY___")
        self.assertEqual(self.score("AAXXX", "BAAAC"), "YG___")

    def test_check_code(self):
        self.assertIn("didn't type", LV3.check_code("", []))
        self.assertIn("4 characters", LV3.check_code("OMEG", []))
        self.assertIn("6 characters", LV3.check_code("OMEGAS", []))
        self.assertIn("'3'", LV3.check_code("OM3GA", []))
        self.assertIn("A-Z", LV3.check_code("ÉCLAT", []))
        self.assertIn("already", LV3.check_code("BUILT", [("BUILT", "_____")]))
        self.assertEqual(LV3.check_code("OMEGA", []), "")

    def test_bad_codes_cost_no_guess(self):
        answers = ["abc", "12345", "", "BUILT", "BUILT"] + WRONG[1:5] + ["OMEGA"]
        self.assertTrue(play(self, LV3.code_panel, answers, True, True))

    def test_out_of_guesses(self):
        self.assertFalse(play(self, LV3.code_panel, WRONG, True, True))

    def test_bonus_gives_a_seventh_guess(self):
        self.assertTrue(play(self, LV3.code_panel, WRONG + ["OMEGA"], True, True, 7))

    def test_back_leaves_the_panel(self):
        self.assertIsNone(play(self, LV3.code_panel, [" back "], False, False))

    def test_control_room(self):
        answers = ["9", "", "3", "back", "1", "2", "3"] + WRONG + ["3", "OMEGA"]
        self.assertTrue(play(self, LV3.control_room, answers))

    def test_quit(self):
        self.assertFalse(play(self, LV3.play, ["quit"]))

    def test_play_shows_ending(self):
        self.assertTrue(play(self, LV3.play, ["3", "OMEGA", ""]))


class TestGame(unittest.TestCase):

    def test_welcome_and_how_to_play_fit(self):
        play(self, Lobby.run, ["", ""])

    def test_credits_fit(self):
        for line in Endcredit.CREDITS:
            self.assertLessEqual(len(line), 79)
        play(self, Endcredit.play_credits, [""])

    def test_whole_game_win_with_bonus(self):
        grid = LV2.carve_maze()
        answers = (["", ""] + perfect_run()
                   + [route(grid, START, GOAL), ""]
                   + ["3"] + WRONG + ["OMEGA", ""]
                   + ["", "n"])
        with mock.patch.object(LV2, "carve_maze", return_value=grid):
            play(self, main.main, answers)

    def test_give_up_then_play_again_then_quit(self):
        answers = ["", "", "quit", "maybe", "y", "", "", "quit", "no"]
        play(self, main.main, answers)

    def test_ctrl_d_exits_cleanly(self):
        with mock.patch.object(main, "play_once", side_effect=EOFError), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            main.main()
        self.assertIn("Thanks for playing", out.getvalue())


class TestScreen(unittest.TestCase):

    def test_resize_message_fits_every_small_window(self):
        for cols in range(1, 80):
            self.assertLess(len(screen.resize_message(cols)), max(cols, 2))

    def test_80_by_24_is_big_enough(self):
        fake_stdout = mock.Mock(isatty=lambda: True)
        with mock.patch.object(screen.sys, "stdout", fake_stdout):
            for size, small in [((80, 24), False), ((79, 24), True),
                                ((80, 23), True), ((200, 60), False)]:
                with mock.patch("os.get_terminal_size",
                                return_value=os.terminal_size(size)):
                    self.assertEqual(screen.too_small(), small, size)

    def test_pauses_until_window_is_bigger(self):
        with mock.patch.object(screen, "too_small", side_effect=[True, True, False]), \
                mock.patch("os.get_terminal_size", return_value=os.terminal_size((60, 20))), \
                mock.patch("time.sleep"), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertTrue(screen.wait_for_size())
        self.assertIn("Window too small", out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
