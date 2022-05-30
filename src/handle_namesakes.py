from collections import defaultdict
from itertools import count
from pathlib import Path
from .flat_walk import flat_walk
from .prompt import prompt

from .utility import order_files


def _namesake_groups_iter(iter):
    """
    Returns an iterator over pairs of namesake group id and file.
    """
    id = count(0, 1)
    name_groups = {}

    for f in iter:
        name = f.name
        if name not in name_groups:
            name_groups[name] = next(id)
        yield (name_groups[name], f)


def find_namesakes(iter):
    """
    Returns a list of groups of files that have the same name.
    """
    name_groups = _namesake_groups_iter(iter)

    groups = defaultdict(list)
    for id, file in name_groups:
        groups[id].append(file)

    return [g for g in groups.values() if len(g) > 1]


def handle_namesakes(target, global_option):
    """
    Performs actions on pairs of namesake files.
    """
    files = flat_walk(target)

    groups = {}
    for id, file in _namesake_groups_iter(files):
        if id not in groups:
            groups[id] = file
        else:
            (global_option, new_path) = _handle_pair(
                global_option, groups[id], file
            )
            groups[id] = new_path
            if global_option == "skip":
                break


def _handle_pair(global_option, file1: Path, file2: Path):
    """
    Handles a pair of namesake files.
    """
    (young, old) = order_files(file1, file2)

    option = global_option

    if option == "interact":
        (all, option) = prompt(_prep_message(young, old), _answer_handler)
        if all:
            global_option = option

    if option == "rm-young":
        young.unlink()
        return (global_option, old)
    elif option == "rm-old":
        old.unlink()
        return (global_option, young)
    else:
        return (global_option, file1)


def _prep_message(young: Path, old: Path):
    """
    Perpares prompt message.
    """
    return f"""\
Files have the same name.
`{young}` is younger than `{old}`.
What to do?
[a]y - delete [all] younger
[a]o - delete [all] older
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
    if answer == "y":
        return (all, "rm-young")
    elif answer == "o":
        return (all, "rm-old")
    elif answer == "s":
        return (all, "skip")
    return None
