from args import parse_args
from config import load_config
from handle_duplicates import find_duplicates
from handle_empty import find_empty
from handle_namesakes import find_namesakes
from handle_mode import find_mode
from handle_symbols import find_symbols
from handle_endings import find_endings
from flat_walk import flat_walk_chained
from pathlib import Path

def main():
    args = parse_args()
    config = load_config()

main()

def listing():
    config = load_config()

    all_files = list(flat_walk_chained(Path('X'), Path('Y1'), Path('Y2')))

    print("namesakes")
    for fs in find_namesakes(all_files):
        print(f'   {fs[0]}', end='')
        for f in fs[1:]:
            print(f'; {f}', end='')
        print()

    print("duplicates")
    for fs in find_duplicates(all_files):
        print(f'   {fs[0]}', end='')
        for f in fs[1:]:
            print(f'; {f}', end='')
        print()

    print("empty")
    for f in find_empty(all_files):
        print(f"   {f}")

    print("endings")
    for f in find_endings(all_files, config.endings):
        print(f"   {f}")

    print("symbols")
    for f in find_symbols(all_files, config.symbols):
        print(f"   {f}")

    print("mode")
    for f in find_mode(all_files, config.pattern):
        print(f"   {f}")