from collections import deque
from pathlib import Path
from shutil import copy
from .flat_walk import flat_walk
from .handle_duplicates import DuplicateGroupsIter
from .hash import mass_hash
from .prompt import prompt


def consume(iterator):
    deque(iterator, maxlen=0)


def _missing_iter(target, sources):
    target_dupes = DuplicateGroupsIter(mass_hash(flat_walk(target)))
    consume(target_dupes)
    id_threshold = max(target_dupes.groups.keys())
    predecessor = target_dupes

    for source in sources:
        source_dupes = DuplicateGroupsIter(mass_hash(flat_walk(source)))
        source_dupes.successor(predecessor)

        for (i, file) in source_dupes:
            if i > id_threshold:
                yield (source, file)

        predecessor = source_dupes


def handle_copy(target, sources, option):
    print("Indexing target directory, please wait...")
    missing = _missing_iter(target, sources)

    global_option = option

    for (source, file) in missing:
        global_option = _handle(global_option, file, target, source)
        if global_option == "skip":
            break


def _handle(global_option, file: Path, target: Path, source: Path):
    """
    Handles a single temporary file.
    """
    option = global_option

    new_file = target / file.relative_to(source)

    if option == "interact":
        (all, option) = prompt(_prep_message(file, new_file), _answer_handler)
        if all:
            global_option = option

    if option == "cp-all":
        if not new_file.exists():
            copy(file, new_file)
        else:
            print(f"Cannot copy file `{file}`, because `{new_file}` already exists.")

    return global_option


def _prep_message(file: Path, new_file: Path):
    """
    Perpares prompt message.
    """
    return f"""\
File `{file}` is missing from target directory.
Copy it to `{new_file}`?
[a]c - copy [all]
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
        return (all, "cp-all")
    elif answer == "s":
        return (all, "skip")
    return None
