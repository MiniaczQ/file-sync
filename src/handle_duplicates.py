from collections import defaultdict
import filecmp
from functools import lru_cache
from itertools import count
from pathlib import Path
from flat_walk import flat_walk

from hash import mass_hash
from prompt import prompt
from utility import order_files


@lru_cache(None)
def _cmp(a, b) -> bool:
    """
    Deeply compares files `a` and `b`.
    """
    return filecmp.cmp(a, b, shallow=False)


def _find(h, p):
    """
    Finds the key of first element that fits the predicate.
    """
    i = (k for k, v in h if p(v))
    r = next(i)
    return r if r != StopIteration else None


def _suspect_groups_iter(iter):
    """
    Groups all files by their hashes.
    Files with the same hash are suspected to be duplicates.
    """
    id = count(0, 1)

    suspect_groups = {}
    for hash, file in mass_hash(iter):
        if hash not in suspect_groups:
            suspect_groups[hash] = next(id)
        yield (suspect_groups[hash], file)


def _duplicate_groups_iter(suspect_groups):
    """
    Returns an iterator over pairs of duplicate group id and file.
    """
    id = count(0, 1)
    duplicate_groups = defaultdict(dict)

    for si, file in suspect_groups:
        if si not in duplicate_groups:
            i = next(id)
            duplicate_groups[si][i] = file
            yield (i, file)
        else:
            r = _find(duplicate_groups[si].items(), lambda f: _cmp(f, file))
            if r is None:
                i = next(id)
                duplicate_groups[si][i] = file
                yield (i, file)
            else:
                i = r
                yield (i, file)


def handle_duplicates(target, global_option):
    """
    Performs actions on pairs of duplicate files.
    """
    files = flat_walk(target)
    suspect_groups = _suspect_groups_iter(files)
    duplicate_groups = _duplicate_groups_iter(suspect_groups)
    for_removal = []

    groups = {}
    for id, file in duplicate_groups:
        if id not in groups:
            groups[id] = file
        else:
            (global_option, new_path) = _handle_pair(
                for_removal, global_option, groups[id], file
            )
            groups[id] = new_path
            if global_option == "skip":
                break

    for f in for_removal:
        f.unlink()


def _handle_pair(for_removal, global_option, file1: Path, file2: Path):
    """
    Handles a pair of duplicate files.
    """
    (young, old) = order_files(file1, file2)

    option = global_option

    if option == "interact":
        (all, option) = prompt(_prep_message(young, old), _answer_handler)
        if all:
            global_option = option

    if option == "rm-young":
        for_removal.append(young)
        return (global_option, old)
    elif option == "rm-old":
        for_removal.append(old)
        return (global_option, young)
    else:
        return (global_option, file1)


def _prep_message(young: Path, old: Path):
    """
    Perpares prompt message.
    """
    return f"""\
Files have the same content.
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
