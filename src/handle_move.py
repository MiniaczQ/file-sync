from pathlib import Path
from flat_walk import flat_walk_chained
from handle_duplicates import DuplicateGroupsIter


def handle_move(target, sources, option):
    existing = set()
    missing = {}

    #Path.

    all_files = flat_walk_chained(target, *sources)

    for (i, file) in DuplicateGroupsIter(all_files):
        #file.
        pass
