from pathlib import Path
from flat_walk import flat_walk
from prompt import prompt


def _endings_iter(iter, endings):
    """
    Returns an iterator over files that have specific name endings.
    """
    for f in iter:
        for ending in endings:
            if str(f).endswith(ending):
                yield f


def find_endings(iter, endings):
    """
    Returns a list of files that have specific name endings.
    """
    return list(_endings_iter(iter, endings))


def handle_endings(target, global_option, endings):
    """
    Performs actions on temporary files.
    """
    files = flat_walk(target)
    for_removal = []

    for file in _endings_iter(files, endings):
        global_option = _handle(for_removal, global_option, file)
        if global_option == "skip":
            break

    for f in for_removal:
        f.unlink()


def _handle(for_removal, global_option, file: Path):
    """
    Handles a single temporary file.
    """
    option = global_option

    if option == "interact":
        (all, option) = prompt(_prep_message(file), _answer_handler)
        if all:
            global_option = option

    if option == "rm-all":
        for_removal.append(file)

    return global_option


def _prep_message(file: Path):
    """
    Perpares prompt message.
    """
    return f"""\
File `{file}` is temporary.
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
