"""
Screen-size guard shared by every screen of GALAXY ESCAPE.

The game is drawn for an 80 x 24 terminal. The project brief says: if the
terminal is smaller, PAUSE the game (do not quit) and show a resize message
that itself fits in the small window.

How to use it: call wait_for_size() right before drawing a screen.
  * Window big enough -> returns False at once, nothing happens.
  * Window too small  -> shows a short message, waits until the player makes
                         the window bigger, clears the screen and returns
                         True (so the caller knows it must redraw).
"""

import os
import re
import sys
import time
import unicodedata

if os.name != "nt":
    import select

MIN_COLS = 80          # the game needs at least this many columns...
MIN_ROWS = 24          # ...and this many rows
CHECK_EVERY = 0.3      # seconds between size checks while paused

CLEAR = "\033[0m\033[2J\033[H"   # reset colours, clear screen, cursor top-left


def current_size():
    """Return (columns, rows) of the terminal window right now.

    os.get_terminal_size() asks the terminal itself. (shutil's version would
    first trust the COLUMNS/LINES variables, which can be out of date after
    the player resizes the window.)
    """
    try:
        size = os.get_terminal_size(sys.stdout.fileno())
        return size.columns, size.lines
    except (OSError, ValueError, AttributeError):
        return MIN_COLS, MIN_ROWS          # not a real terminal: assume OK


def too_small():
    """True if the window is smaller than 80 x 24.

    When the output is not a terminal (automated tests, output sent to a
    file) there is no window to resize, so we never pause.
    """
    if not sys.stdout.isatty():
        return False
    cols, rows = current_size()
    return cols < MIN_COLS or rows < MIN_ROWS


def resize_message(cols, rows):
    """The pause message, cut down so it fits inside a cols x rows window.

    Each line is at most cols - 1 characters (a line that fills the last
    column can make some terminals wrap), and there are at most `rows` lines.
    """
    lines = [
        "WINDOW TOO SMALL",
        f"Need {MIN_COLS}x{MIN_ROWS}, now {cols}x{rows}.",
        "Make the window bigger",
        "to keep playing.",
        "(Game is paused.)",
    ]
    width = max(cols - 1, 1)
    return [line[:width] for line in lines[:max(rows, 1)]]


def forget_typed_keys():
    """Throw away keys typed while the game was paused, so they don't count."""
    if not sys.stdin.isatty():
        return                             # not a real keyboard: nothing to do
    if os.name == "nt":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getwch()
    else:
        import termios
        try:
            termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)
        except termios.error:
            pass


def wait_for_size():
    """Pause until the window is at least 80 x 24.

    Returns False if no pause was needed, True if we paused (the screen has
    been cleared, so the caller should draw its screen again).
    """
    if not too_small():
        return False

    last_size = None
    while too_small():
        size = current_size()
        if size != last_size:              # only redraw when the size changes
            cols, rows = size              # (stops the message flickering)
            # No newline after the last line, so the message never scrolls.
            sys.stdout.write(CLEAR + "\n".join(resize_message(cols, rows)))
            sys.stdout.flush()
            last_size = size
        time.sleep(CHECK_EVERY)

    sys.stdout.write(CLEAR)                # big enough again: wipe the message
    sys.stdout.flush()
    forget_typed_keys()                    # keys pressed while paused don't count
    return True


# ======================================================================
# ask(): our own input(), safe for the 80 x 24 area
#
# Python's input() has two problems for this game:
#   1. It waits for ENTER and cannot be interrupted, so a window made
#      smaller WHILE the player is typing was only noticed after ENTER.
#   2. It lets the player type as much as they like. A long answer wraps
#      onto the next row and, at the bottom of the screen, scrolls the
#      whole display - the brief says input must never do that.
#
# ask() reads one key at a time instead (like the maze does), so it can
# check the window size every 0.25 s and refuse keys that would not fit
# on the prompt's row.
# ======================================================================

ANSI_CODE = re.compile(r"\033\[[0-9;?]*[A-Za-z]")   # colour / cursor codes
KEY_WAIT = 0.25          # seconds between window-size checks while typing
BACKSPACE_KEYS = ("\x7f", "\x08")
ENTER_KEYS = ("\r", "\n")
END_OF_INPUT = "\x04"    # Ctrl+D


def visible_width(text):
    """Columns `text` takes on screen.

    Colour codes take no space. Most characters take 1 column, Chinese /
    Japanese / Korean characters take 2, and accent or Thai vowel marks
    that sit on top of the previous letter take 0.
    """
    width = 0
    for ch in ANSI_CODE.sub("", text):
        if unicodedata.combining(ch):
            continue
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return width


def edit_line(typed, key, room):
    """Apply one key to the text typed so far.

    Returns (new_text, finished). `room` is how many columns are free after
    the prompt. Keys that would go past it are ignored, so the answer can
    never wrap onto the next row.
    """
    if key in ENTER_KEYS:
        return typed, True
    if key in BACKSPACE_KEYS:
        return typed[:-1], False
    if not key.isprintable():              # Esc, Tab, arrow-key codes, ...
        return typed, False
    if visible_width(typed + key) > room:   # boundary: row is full
        return typed, False
    return typed + key, False


def _key_waiting(fd, wait):
    """True if a key is pressed within `wait` seconds."""
    return bool(select.select([fd], [], [], wait)[0])


def _read_char(fd, decoder):
    """Read one typed character (a Thai or accented letter is several bytes)."""
    while True:
        data = os.read(fd, 1)
        if not data:                       # stdin closed
            return END_OF_INPUT
        text = decoder.decode(data)
        if text:
            return text


def _skip_escape_sequence(fd):
    """Arrow keys send ESC [ A etc. Throw the rest of that sequence away.

    Stops at the sequence's last byte (a letter or ~), so keys typed right
    after it are kept. A lone Esc press has nothing after it.
    """
    if not _key_waiting(fd, 0.05):
        return                             # a lone Esc
    if os.read(fd, 1) not in (b"[", b"O"):
        return
    while _key_waiting(fd, 0.05):
        if 0x40 <= os.read(fd, 1)[0] <= 0x7E:   # end of the sequence
            return


def ask(prompt, redraw=None):
    """Like input(prompt), but stays inside 80 x 24.

    * If the window becomes smaller than 80 x 24 while the player is typing,
      the game pauses at once. When it is big enough again, redraw() (if
      given) draws the screen again and the prompt comes back with the text
      typed so far.
    * The answer cannot be longer than the space left on the prompt's row.
    * Ctrl+D raises EOFError and Ctrl+C raises KeyboardInterrupt, the same
      as input(), so main.py can exit cleanly.

    Without a real terminal (automated tests, input from a file) or on
    Windows it simply calls input().
    """
    if os.name == "nt" or not (sys.stdin.isatty() and sys.stdout.isatty()):
        return input(prompt)

    import codecs
    import termios
    import tty

    prompt_row = prompt.split("\n")[-1]    # the part on the same row as typing
    room = MIN_COLS - 1 - visible_width(prompt_row)
    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
    fd = sys.stdin.fileno()
    saved = termios.tcgetattr(fd)
    typed = ""

    sys.stdout.write(prompt)
    sys.stdout.flush()
    try:
        tty.setcbreak(fd)                  # one key at a time, no echo
        while True:
            if not _key_waiting(fd, KEY_WAIT):
                if too_small():            # window shrank while typing
                    wait_for_size()
                    if redraw is not None:
                        redraw()
                    sys.stdout.write(prompt_row + typed)
                    sys.stdout.flush()
                continue
            key = _read_char(fd, decoder)
            if key == END_OF_INPUT and typed == "":
                raise EOFError
            if key == "\x1b":
                _skip_escape_sequence(fd)
                continue
            typed, finished = edit_line(typed, key, room)
            # Rewrite the whole row: simpler than working out how many
            # columns a deleted Thai or Chinese character used.
            sys.stdout.write("\r" + prompt_row + typed + "\033[K")
            if finished:
                sys.stdout.write("\n")
                sys.stdout.flush()
                return typed
            sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, saved)


# Try it: run this file, then drag the window smaller and bigger.
if __name__ == "__main__":
    print("Make the window smaller than 80x24 to see the pause message.")
    print("Press Ctrl+C to stop.")
    try:
        while True:
            if wait_for_size():
                print("Window is big enough again. Press Ctrl+C to stop.")
            time.sleep(CHECK_EVERY)
    except KeyboardInterrupt:
        print()
