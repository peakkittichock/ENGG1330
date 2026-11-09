"""
Automated tests for GALAXY ESCAPE.

Run from the project folder:   python3 -m unittest -v test_game.py

Standard library only (unittest + unittest.mock). The tests never need a real
keyboard: input() is replaced by a list of pre-typed answers, time.sleep is
switched off so animations finish instantly, and screen output is captured so
the test log stays readable.

What is covered:
  * Level 3 Wordle scoring, including repeated letters (the tricky case)
  * Level 3 panel and control room: normal play, invalid input, running out
    of guesses, and the win condition
  * Level 2 maze: always solvable, walls on the border, enough dead ends
  * Screen size: every fixed screen fits inside 80 x 24
  * Stealth event: no guard, right letter, wrong letter, too slow
  * main.py flow: win, fail at each level, play again / quit
  * Invalid actions / boundary cases: Level 3 code checks (empty, 4 and 6
    letters, non A-Z, repeats, BACK, last guess), maze quit confirmation and
    footer messages, how-to-play feedback, play-again re-asking, Ctrl+D
  * Typing (screen.ask): answers stop at the end of the prompt's row, wide
    characters count double, the stealth timer pauses while the window is small
  * Small window: the pause message fits any size, the game waits until the
    window is 80 x 24 again, and the maze notices a resize while waiting
"""

import contextlib
import io
import unittest
from unittest import mock

import Endcredit
import Lobby
import LV1
import LV2
import LV3
import Stealth
import main
import screen


def run_quietly(function, answers, *args):
    """Call function(*args) with input() answering from `answers`.

    Output is thrown away and time.sleep does nothing. If the function asks
    for more input than we planned, StopIteration is raised, so a test can
    never hang waiting for the keyboard.
    """
    with mock.patch("builtins.input", side_effect=list(answers)), \
            mock.patch("time.sleep"), \
            contextlib.redirect_stdout(io.StringIO()):
        return function(*args)


# ---------------------------------------------------------------------------
# Level 3: Wordle scoring
# ---------------------------------------------------------------------------
class TestScoreGuess(unittest.TestCase):

    def test_correct_code_is_all_green(self):
        self.assertEqual(LV3.score_guess("OMEGA", "OMEGA"), list("GGGGG"))

    def test_no_letters_in_common_is_all_gray(self):
        self.assertEqual(LV3.score_guess("BUILT", "OMEGA"), list("_____"))

    def test_right_letters_wrong_places_are_yellow(self):
        self.assertEqual(LV3.score_guess("GAMMO", "OMEGA"), list("YYY_Y"))   # second M: OMEGA has one M

    def test_repeated_guess_letter_only_coloured_once(self):
        # OMEGA has one E. Only the E in the right spot is green; the other
        # four E's must be gray, not yellow.
        self.assertEqual(LV3.score_guess("EEEEE", "OMEGA"), list("__G__"))

    def test_green_is_counted_before_yellow(self):
        # MAMMA: last A is green, so the first A must NOT also be yellow
        # (OMEGA has only one A). The first M is yellow, the other M's gray.
        self.assertEqual(LV3.score_guess("MAMMA", "OMEGA"), list("Y___G"))

    def test_mixed_green_and_yellow(self):
        self.assertEqual(LV3.score_guess("GAMMA", "OMEGA"), list("Y_Y_G"))


# ---------------------------------------------------------------------------
# Level 3: self-destruct panel and control room
# ---------------------------------------------------------------------------
WRONG_WORDS = ["BUILT", "CRANE", "PLUSH", "DIRTY", "FJORD", "WOVEN"]   # all different


class TestLevel3(unittest.TestCase):

    def test_right_code_first_try_wins(self):
        self.assertTrue(run_quietly(LV3.code_panel, ["omega"], True, True))

    def test_invalid_codes_do_not_use_up_guesses(self):
        # Too short, too long, digits, empty, symbols: all rejected without
        # costing a guess, then 5 wrong guesses + the right one still wins.
        bad = ["abc", "toolong", "12345", "", "om ga", "OM3GA"]
        wrong = WRONG_WORDS[:LV3.MAX_GUESSES - 1]
        self.assertTrue(run_quietly(LV3.code_panel, bad + wrong + ["OMEGA"], False, False))

    def test_running_out_of_guesses_returns_false(self):
        wrong = WRONG_WORDS[:LV3.MAX_GUESSES]
        self.assertFalse(run_quietly(LV3.code_panel, wrong, True, True))

    def test_control_room_invalid_menu_choice_then_win(self):
        answers = ["9", "hello", "", "1", "2", "3", "OMEGA"]
        self.assertTrue(run_quietly(LV3.control_room, answers))

    def test_control_room_retry_after_failed_panel(self):
        answers = ["3"] + WRONG_WORDS[:LV3.MAX_GUESSES] + ["3", "OMEGA"]
        self.assertTrue(run_quietly(LV3.control_room, answers))

    # --- invalid actions and boundary cases on the panel -----------------

    def test_check_code_messages(self):
        self.assertIn("didn't type", LV3.check_code("", []))
        self.assertIn("Too short: 4", LV3.check_code("OMEG", []))       # 4 = one short
        self.assertIn("Too long: 6", LV3.check_code("OMEGAS", []))      # 6 = one long
        self.assertIn("'3'", LV3.check_code("OM3GA", []))
        self.assertIn("' '", LV3.check_code("OM GA", []))
        self.assertEqual(LV3.check_code("OMEGA", []), "")               # exactly 5: OK

    def test_accented_letters_rejected(self):
        # "ÉCLAT".isalpha() is True, but it can never be the code.
        self.assertIn("A-Z", LV3.check_code("ÉCLAT", []))

    def test_repeated_guess_does_not_cost_a_guess(self):
        # BUILT twice: the second one is rejected, so 5 different wrong words
        # + OMEGA still fit inside the 6 guesses.
        answers = ["BUILT", "BUILT"] + WRONG_WORDS[1:5] + ["OMEGA"]
        self.assertTrue(run_quietly(LV3.code_panel, answers, True, True))

    def test_last_guess_can_still_win(self):
        answers = WRONG_WORDS[:LV3.MAX_GUESSES - 1] + ["OMEGA"]
        self.assertTrue(run_quietly(LV3.code_panel, answers, True, True))

    def test_back_leaves_panel_without_losing(self):
        self.assertIsNone(run_quietly(LV3.code_panel, ["back"], False, False))
        self.assertIsNone(run_quietly(LV3.code_panel, ["  Back "], False, False))

    def test_back_then_search_then_win(self):
        # Open the panel too early, step back, find the clues, then win.
        answers = ["3", "BUILT", "back", "1", "2", "3", "OMEGA"]
        self.assertTrue(run_quietly(LV3.control_room, answers))

    def test_play_returns_true_after_ending_animation(self):
        # "3", "OMEGA", then ENTER at the end of the animation.
        self.assertTrue(run_quietly(LV3.play, ["3", "OMEGA", ""]))

    def test_ending_art_fits_scene_width(self):
        for art in [LV3.STATION] + LV3.EXPLOSION:
            for line in art:
                self.assertLessEqual(len(line), LV3.SCENE_WIDTH)


# ---------------------------------------------------------------------------
# Level 2: maze generation
# ---------------------------------------------------------------------------
class TestMaze(unittest.TestCase):

    def test_many_mazes_are_solvable_and_valid(self):
        for _ in range(30):                       # random, so try many
            grid, start, goal, par = LV2.generate_maze()
            self.assertEqual(len(grid), LV2.GRID_H)
            self.assertTrue(all(len(row) == LV2.GRID_W for row in grid))
            self.assertEqual(grid[start[0]][start[1]], LV2.PATH)
            self.assertEqual(grid[goal[0]][goal[1]], LV2.PATH)
            self.assertIsNotNone(par)
            self.assertEqual(par, LV2.shortest_path_length(grid, start, goal))
            self.assertGreaterEqual(LV2.count_dead_ends(grid, start, goal),
                                    LV2.MIN_DEAD_ENDS)

    def test_border_is_solid_wall(self):
        grid, _, _, _ = LV2.generate_maze()
        for c in range(LV2.GRID_W):
            self.assertEqual(grid[0][c], LV2.WALL)
            self.assertEqual(grid[-1][c], LV2.WALL)
        for r in range(LV2.GRID_H):
            self.assertEqual(grid[r][0], LV2.WALL)
            self.assertEqual(grid[r][-1], LV2.WALL)

    def test_shortest_path_on_tiny_hand_made_grid(self):
        W, P = LV2.WALL, LV2.PATH
        grid = [[W, W, W, W, W],
                [W, P, P, P, W],
                [W, W, W, P, W],
                [W, W, W, W, W]]
        self.assertEqual(LV2.shortest_path_length(grid, (1, 1), (2, 3)), 3)
        blocked = [row[:] for row in grid]
        blocked[1][2] = W
        self.assertIsNone(LV2.shortest_path_length(blocked, (1, 1), (2, 3)))

    def test_keys_map_to_actions(self):
        self.assertEqual(LV2._plain_key("w"), "UP")
        self.assertEqual(LV2._plain_key("A"), "LEFT")      # caps lock still works
        self.assertEqual(LV2._plain_key("q"), "QUIT")
        self.assertIsNone(LV2._plain_key("x"))             # unknown key ignored

    def run_maze(self, keys):
        """Play the maze with a fixed list of keys; return (result, footers)."""
        footers = []
        real_draw = LV2.draw

        def record(*args):
            footers.append(args[-1] if len(args) == 9 else LV2.HELP_LINE)
            with contextlib.redirect_stdout(io.StringIO()):
                real_draw(*args)

        with mock.patch.object(LV2, "next_key", side_effect=keys), \
                mock.patch.object(LV2, "draw", side_effect=record), \
                mock.patch.object(screen, "wait_for_size"):
            return LV2.play(), footers

    def test_one_q_only_asks_two_q_quits(self):
        result, footers = self.run_maze(["QUIT", "QUIT"])
        self.assertFalse(result)                           # quit before exit
        self.assertEqual(footers[-1], LV2.CONFIRM_QUIT_LINE)

    def test_other_key_cancels_quit(self):
        # Q, then x (cancel), then Q, Q.
        result, footers = self.run_maze(["QUIT", None, "QUIT", "QUIT"])
        self.assertEqual(footers[2], LV2.UNKNOWN_LINE)
        self.assertFalse(result)

    def test_wall_bump_and_unknown_key_messages(self):
        # Start (1,1) is in the top-left corner: UP and LEFT are always walls.
        result, footers = self.run_maze(["UP", "LEFT", None, "QUIT", "QUIT"])
        self.assertEqual(footers[1:4], [LV2.WALL_LINE, LV2.WALL_LINE,
                                        LV2.UNKNOWN_LINE])

    def test_footer_lines_fit(self):
        for line in [LV2.HELP_LINE, LV2.WALL_LINE, LV2.UNKNOWN_LINE,
                     LV2.CONFIRM_QUIT_LINE]:
            self.assertLessEqual(len(line), 79)

    def test_maze_fits_80_by_24(self):
        self.assertLessEqual(LV2.SCREEN_W, 80)
        self.assertLessEqual(LV2.SCREEN_H, 24)


# ---------------------------------------------------------------------------
# Screens fit inside 80 x 24
# ---------------------------------------------------------------------------
class TestScreenSize(unittest.TestCase):

    def test_welcome_art_fits(self):
        art = [Lobby.TITLE[1:], Lobby.TAGLINE, Lobby.STATION[1:]]
        lines = "\n".join(art).split("\n")
        self.assertLessEqual(len(lines) + 1, 24)          # +1 for the prompt
        for line in lines:
            self.assertLessEqual(len(line), 80)

    def test_how_to_play_pages_fit_in_box(self):
        for title, lines in Lobby.PAGES:
            self.assertLessEqual(len(lines), Lobby.CONTENT_ROWS, title)
            for line in lines:
                self.assertLessEqual(Lobby.visible_length(line), Lobby.INSIDE,
                                     f"too wide on page {title!r}: {line!r}")

    def test_how_to_play_back_and_invalid_keys(self):
        # b on page 1 stays on page 1; junk redraws; ENTER x3 leaves.
        run_quietly(Lobby.show_how_to_play, ["b", "zzz", "", "b", "", "", ""])

    def test_how_to_play_feedback_messages(self):
        with mock.patch.object(Lobby, "draw_page") as draw, \
                mock.patch("builtins.input", side_effect=["b", "zzz", "", "", ""]):
            Lobby.show_how_to_play()
        messages = [call.args[1] for call in draw.call_args_list]
        self.assertIn("first page", messages[1])
        self.assertIn("'zzz' is not a command", messages[2])
        self.assertEqual(messages[3], "")                  # cleared after ENTER
        for text in messages:
            self.assertLessEqual(Lobby.visible_length("  " + text), 79)

    def test_credit_lines_fit_when_spread_out(self):
        for line in Endcredit.CREDITS:
            self.assertLessEqual(len(Endcredit.spread(line)), Endcredit.WIDTH, line)


# ---------------------------------------------------------------------------
# Stealth event
# ---------------------------------------------------------------------------
class TestStealth(unittest.TestCase):

    def test_no_guard_when_chance_is_zero(self):
        # Must not ask for any input at all.
        self.assertTrue(run_quietly(Stealth.quicktime, [], 0.0))

    def typed(self, answer, seconds_taken):
        """Run the non-terminal fallback with a fake clock."""
        clock = iter([100.0, 100.0 + seconds_taken])
        with mock.patch("time.time", side_effect=lambda: next(clock)):
            return run_quietly(Stealth.wait_for_key_typed, [answer], "k")

    def test_right_letter_in_time(self):
        self.assertTrue(self.typed("k", 1.0))

    def test_capital_letter_and_spaces_accepted(self):
        self.assertTrue(self.typed("  K ", 1.0))

    def test_wrong_letter(self):
        self.assertFalse(self.typed("j", 1.0))

    def test_too_slow(self):
        self.assertFalse(self.typed("k", Stealth.TIME_LIMIT + 0.5))


# ---------------------------------------------------------------------------
# main.py: whole-game flow (levels replaced by fakes)
# ---------------------------------------------------------------------------
class TestMainFlow(unittest.TestCase):

    def play_once_with(self, lv1=True, lv2=True, lv3=True, stealth=True):
        with mock.patch.object(Lobby, "run"), \
                mock.patch.object(LV1, "play", return_value=lv1), \
                mock.patch.object(LV2, "run_level", return_value=lv2), \
                mock.patch.object(LV3, "play", return_value=lv3), \
                mock.patch.object(Stealth, "quicktime", return_value=stealth):
            return run_quietly(main.play_once, [""])

    def test_clearing_every_level_wins(self):
        self.assertTrue(self.play_once_with())

    def test_failing_any_step_is_game_over(self):
        self.assertFalse(self.play_once_with(lv1=False))
        self.assertFalse(self.play_once_with(lv2=False))
        self.assertFalse(self.play_once_with(lv3=False))
        self.assertFalse(self.play_once_with(stealth=False))

    def test_play_again_then_quit(self):
        # Lose twice: answer "y" (play again), then "n" (quit).
        with mock.patch.object(main, "play_once", return_value=False) as play:
            run_quietly(main.main, ["y", "n"])
        self.assertEqual(play.call_count, 2)

    def test_invalid_play_again_answer_asks_again(self):
        # "maybe", "", "1" are invalid: asked again, NOT quit by accident.
        with mock.patch.object(main, "play_once", return_value=False) as play:
            run_quietly(main.main, ["maybe", "", "1", "YES", "no"])
        self.assertEqual(play.call_count, 2)

    def test_ctrl_d_exits_cleanly(self):
        # Ctrl+D makes input() raise EOFError: must not crash the game.
        with mock.patch.object(main, "play_once", side_effect=EOFError):
            with contextlib.redirect_stdout(io.StringIO()) as out:
                main.main()
        self.assertIn("Thanks for playing", out.getvalue())

    def test_level_contract_functions_exist(self):
        # main.py relies on these names (see GAME_PLAN.md section 2).
        for module, name in [(Lobby, "run"), (LV1, "play"), (LV2, "run_level"),
                             (LV3, "play"), (Stealth, "quicktime"),
                             (Endcredit, "play_credits")]:
            self.assertTrue(callable(getattr(module, name, None)),
                            f"{module.__name__}.{name}() is missing")


# ---------------------------------------------------------------------------
# Window smaller than 80 x 24 (screen.py)
# ---------------------------------------------------------------------------
class TestSmallWindow(unittest.TestCase):

    def test_message_fits_every_small_size(self):
        # Boundary cases: from a 1 x 1 window up to 79 x 23.
        for cols in range(1, 80):
            for rows in range(1, 24):
                lines = screen.resize_message(cols, rows)
                self.assertGreaterEqual(len(lines), 1)
                self.assertLessEqual(len(lines), rows)
                for line in lines:
                    self.assertLess(len(line), max(cols, 2))

    def test_message_shows_the_current_size(self):
        self.assertIn("60x20", "\n".join(screen.resize_message(60, 20)))

    def test_no_pause_when_window_is_big_enough(self):
        with mock.patch.object(screen, "too_small", return_value=False), \
                mock.patch("time.sleep") as sleep:
            self.assertFalse(screen.wait_for_size())
        sleep.assert_not_called()

    def test_pauses_until_window_is_enlarged(self):
        # Too small for 3 checks, then big enough.
        checks = [True, True, True, False]
        with mock.patch.object(screen, "too_small", side_effect=checks), \
                mock.patch.object(screen, "current_size", return_value=(60, 20)), \
                mock.patch("time.sleep") as sleep, \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertTrue(screen.wait_for_size())
        self.assertEqual(sleep.call_count, 2)
        self.assertIn("WINDOW TOO SMALL", out.getvalue())

    def test_exact_80_by_24_is_not_too_small(self):
        fake_stdout = mock.Mock(isatty=lambda: True)
        with mock.patch.object(screen.sys, "stdout", fake_stdout):
            for size, small in [((80, 24), False), ((79, 24), True),
                                ((80, 23), True), ((200, 60), False)]:
                with mock.patch.object(screen, "current_size", return_value=size):
                    self.assertEqual(screen.too_small(), small, size)

    def test_never_pauses_when_output_is_not_a_terminal(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(screen.too_small())

    # --- screen.ask(): typing can never wrap or scroll the 80 x 24 area ---

    def test_typing_stops_at_end_of_row(self):
        typed = ""
        for _ in range(100):                       # hold a key down
            typed, done = screen.edit_line(typed, "x", 10)
        self.assertEqual(typed, "x" * 10)          # boundary: exactly fills
        self.assertFalse(done)

    def test_wide_characters_count_as_two_columns(self):
        self.assertEqual(screen.visible_width("ab"), 2)
        self.assertEqual(screen.visible_width("\033[1mab\033[0m"), 2)  # colour = 0
        self.assertEqual(screen.visible_width("中文"), 4)
        self.assertEqual(screen.visible_width("ก้"), 1)   # Thai mark sits on top
        typed, _ = screen.edit_line("中文中文", "中", 9)   # 8 + 2 > 9: refused
        self.assertEqual(typed, "中文中文")

    def test_backspace_enter_and_control_keys(self):
        self.assertEqual(screen.edit_line("abc", "\x7f", 50), ("ab", False))
        self.assertEqual(screen.edit_line("", "\x7f", 50), ("", False))  # empty
        self.assertEqual(screen.edit_line("abc", "\r", 50), ("abc", True))
        self.assertEqual(screen.edit_line("abc", "\t", 50), ("abc", False))

    def test_every_prompt_leaves_room_to_type(self):
        prompts = ["Type the 5-letter code > ", "> ",
                   "  ENTER = start the game    b = back  > "]
        for prompt in prompts:
            room = screen.MIN_COLS - 1 - screen.visible_width(prompt)
            self.assertGreaterEqual(room, 5, prompt)   # a 5-letter code fits

    def test_ask_uses_input_without_a_real_terminal(self):
        with mock.patch("builtins.input", return_value="omega"), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(screen.ask("> "), "omega")

    def test_stealth_timer_pauses_while_window_is_small(self):
        # Window small for one check: wait_for_size + redraw are called, and
        # the player still gets the right key in afterwards.
        redraw = mock.Mock()
        with mock.patch.object(screen, "too_small", side_effect=[True, False]), \
                mock.patch.object(screen, "wait_for_size") as wait, \
                mock.patch.object(Stealth, "key_waiting", return_value=True), \
                mock.patch.object(Stealth, "read_one_key", return_value="k"), \
                mock.patch.object(Stealth, "throw_away_old_keys"), \
                mock.patch.object(Stealth.termios, "tcgetattr"), \
                mock.patch.object(Stealth.termios, "tcsetattr"), \
                mock.patch.object(Stealth.tty, "setcbreak"), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(Stealth.wait_for_key_timed("k", redraw))
        wait.assert_called_once()
        redraw.assert_called_once()

    def test_maze_reports_resize_while_waiting_for_a_key(self):
        with mock.patch.object(LV2, "key_ready", return_value=False), \
                mock.patch.object(screen, "too_small", return_value=True):
            self.assertEqual(LV2.next_key(), "RESIZE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
