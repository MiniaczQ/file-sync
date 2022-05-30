from os import path
from pathlib import Path
from flat_walk import flat_walk

from prompt import prompt


def _empty_iter(iter):
    """
    Returns an iterator over empty files.
    """
    for f in iter:
        if path.getsize(f) == 0:
            yield f


def find_empty(iter):
    """
    Returns a list of empty files.
    """
    return list(_empty_iter(iter))


def handle_empty(target, global_option):
    """
    Performs actions on empty files.
    """
    files = flat_walk(target)

    for file in _empty_iter(files):
        global_option = _handle(global_option, file)
        if global_option == "skip":
            break


def _handle(global_option, file: Path):
    """
    Handles a single empty file.
    """
    option = global_option

    if option == "interact":
        (all, option) = prompt(_prep_message(file), _answer_handler)
        if all:
            global_option = option

    if option == "rm-all":
        file.unlink()

    return global_option


def _prep_message(file: Path):
    """
    Perpares prompt message.
    """
    return f"""\
File `{file}` is empty.
Remove?
[a]r - remove [all]
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
    if answer == "r":
        return (all, "rm-all")
    elif answer == "s":
        return (all, "skip")
    return None
