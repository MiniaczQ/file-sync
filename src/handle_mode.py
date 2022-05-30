from pathlib import Path
from flat_walk import flat_walk
from prompt import prompt


def _create_matcher(pattern):
    """
    Returns a function that can decide whether an `ST_MODE` fits the pattern.
    """
    mask = 0b111111111
    high = 0
    low = 0

    for (p, c) in zip(pattern, "rwxrwxrwx"):
        high = high << 1
        low = low << 1

        if p == c:
            high += 1
            low += 1
        elif p == "_":
            high += 1

    def matcher(x):
        x = x & mask
        return (high ^ x) & (low ^ x)

    return matcher


def _mode_iter(iter, matcher):
    """
    Returns an iterator over files that don't match.
    """
    for f in iter:
        if matcher(f.stat().st_mode) != 0:
            yield f


def handle_mode(target, global_option, pattern):
    """
    Performs actions on files with invalid modes.
    """
    files = flat_walk(target)
    matcher = _create_matcher(pattern)

    for file in _mode_iter(files, matcher):
        global_option = _handle(global_option, file, matcher)
        if global_option == "skip":
            break


def _handle(global_option, file: Path, matcher):
    """
    Handles a single file with invalid mode.
    """
    option = global_option

    if option == "interact":
        (all, option) = prompt(_prep_message(file, matcher), _answer_handler)
        if all:
            global_option = option

    if option == "ch-all":
        new_mode = _fit_mode(file, matcher)
        file.chmod(new_mode)

    return global_option


def _prep_message(file: Path, matcher):
    """
    Perpares prompt message.
    """
    return f"""\
File `{file}` has unusual mode `{_mode2str(file.stat().st_mode)}`.
Change to `{_mode2str(_fit_mode(file, matcher))}`?
[a]c - change [all]
[a]s - skip [all]\
"""


def _answer_handler(answer):
    """
    Validates and processes user input.
    """
    if len(answer) == 0:
        return None
    all = answer.startswith("a")
    answer = answer[-1]
    if answer == "c":
        return (all, "ch-all")
    elif answer == "s":
        return (all, "skip")
    return None


def _mode2str(mode):
    """
    Turns binary mode representation into string.
    """
    s = ""
    for y in "rwxrwxrwx":
        if mode & 0b100000000 == 0b100000000:
            s += y
        else:
            s += "-"
        mode = mode << 1
    return s


def _fit_mode(file: Path, matcher):
    """
    Returns an adjusted mode for the provided file, to fit the pattern.
    """
    m = file.stat().st_mode
    return m ^ matcher(m) & 0b111111111
