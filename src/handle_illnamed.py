from pathlib import Path
from .flat_walk import flat_walk
from .prompt import prompt


def _symbols_iter(iter, symbols):
    """
    Returns an iterator over files that names contain any of the provided symbols.
    """
    for f in iter:
        if any(s in f.name for s in symbols):
            yield f


def find_symbols(iter, symbols):
    """
    Returns a list of files that names contain ant of the provided symbols.
    """
    return list(_symbols_iter(iter, symbols))


def handle_illnamed(target, global_option, symbols, substitute):
    """
    Performs actions on ill-named files.
    """
    files = flat_walk(target)

    for file in _symbols_iter(files, symbols):
        global_option = _handle(global_option, file, symbols, substitute)
        if global_option == "skip":
            break


def _handle(global_option, file: Path, symbols, substitute):
    """
    Handles a single ill-named file.
    """
    option = global_option

    if option == "interact":
        (all, option) = prompt(
            _prep_message(file, symbols, substitute), _answer_handler
        )
        if all:
            global_option = option

    if option == "re-all":
        name = _renamed(file, symbols, substitute)
        renamed = file.with_name(name)
        if not renamed.exists():
            file.rename(renamed)
        else:
            print(
                f"File `{file}` cannot be renamed, because `{renamed}` already exists."
            )

    return global_option


def _prep_message(file: Path, symbols, substitute):
    """
    Perpares prompt message.
    """
    return f"""\
File `{file}` is ill-named.
Rename to {_renamed(file, symbols, substitute)}?
[a]r - rename [all]
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
        return (all, "re-all")
    elif answer == "s":
        return (all, "skip")
    return None


def _renamed(file: Path, symbols, substitute):
    """
    File after substituting all the symbols.
    """
    name = file.name
    for s in symbols:
        name = name.replace(s, substitute)
    return name
