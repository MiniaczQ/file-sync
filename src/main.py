from duplicates import find_duplicates
from flat_walk import flat_walk
from itertools import chain
from pathlib import Path

#print(args())
#prompt("Hello")

all_files = list(chain(flat_walk(Path('X')), flat_walk('Y1'), flat_walk('Y2')))

print(find_duplicates(all_files))
