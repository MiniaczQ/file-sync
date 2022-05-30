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


class DuplicateGroupsIter:
    """
    Iterator over pairs of duplicate group id and file.
    """
    def __init__(self, iter):
        self.id = count(0, 1)
        self.groups = defaultdict(dict)
        self.hash_idx = {}
        self.iter = iter
    
    def __iter__(self):
        return self
    
    def __next__(self):
        (si, file) = next(self.iter)
        if si not in self.groups:
            i = next(self.id)
            self.groups[si][i] = file
            self.hash_idx[i] = si
            return (i, file)
        else:
            r = _find(self.groups[si].items(), lambda f: _cmp(f, file))
            if r is None:
                i = next(self.id)
                self.groups[si][i] = file
                self.hash_idx[i] = si
                return (i, file)
            else:
                i = r
                return (i, file)
    
    def get_group(self, i):
        return self.groups[self.hash_idx[i]][i]
    
    def set_group(self, i, v):
        self.groups[self.hash_idx[i]][i] = v


def handle_duplicates(target, global_option):
    """
    Performs actions on pairs of duplicate files.
    """
    files = flat_walk(target)
    suspect_groups = _suspect_groups_iter(files)
    duplicate_groups = DuplicateGroupsIter(suspect_groups)

    for id, file in duplicate_groups:
        if id in duplicate_groups.groups:
            (global_option, new_path) = _handle_pair(
                global_option, duplicate_groups.get_group(id), file
            )
            duplicate_groups.set_group(id, new_path)
            if global_option == "skip":
                break


def _handle_pair(global_option, file1: Path, file2: Path):
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
