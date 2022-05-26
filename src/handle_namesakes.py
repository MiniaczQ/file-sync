from collections import defaultdict
from itertools import count

def _namesake_groups_iter(iter):
    '''
    Returns an iterator over pairs of namesake group id and file.
    '''
    id = count(0, 1)
    name_groups = {}

    for f in iter:
        name = f.name
        if name not in name_groups:
            name_groups[name] = next(id)
        yield (name_groups[name], f)

def find_namesakes(iter):
    '''
    Returns a list of groups of files that have the same name.
    '''
    name_groups = _namesake_groups_iter(iter)

    groups = defaultdict(list)
    for id, file in name_groups:
        groups[id].append(file)

    return [g for g in groups.values() if len(g) > 1]
