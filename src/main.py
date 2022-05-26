from find_duplicates import find_duplicates
from find_empty import find_empty
from find_namesakes import find_namesakes
from find_mode import find_mode
from find_symbols import find_symbols
from find_endings import find_endings
from flat_walk import flat_walk_chained
from itertools import chain
from pathlib import Path

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
for f in find_endings(all_files, ['.temp', '~']):
    print(f"   {f}")

print("symbols")
for f in find_symbols(all_files, '"\':;*?$#|\\'):
    print(f"   {f}")

print("mode")
for f in find_mode(all_files, '_rw-rw-rw-'):
    print(f"   {f}")
