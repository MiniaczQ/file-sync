from collections import defaultdict
import filecmp
from itertools import count

from hash import mass_hash

def _cmp(a, b) -> bool:
    '''
    Deeply compares files `a` and `b`.
    '''
    return filecmp.cmp(a, b, shallow=False)

def _find(h, p):
    '''
    Finds the key of first element that fits the predicate.
    '''
    i = (k for k, v in h if p(v))
    r = next(i)
    return r if r != StopIteration else None

def _suspect_groups_iter(iter):
    '''
    Groups all files by their hashes.
    Files with the same hash are suspected to be duplicates.
    '''
    id = count(0, 1)

    suspect_groups = {}
    for hash, file in mass_hash(iter):
        if hash not in suspect_groups:
            suspect_groups[hash] = next(id)
        yield (suspect_groups[hash], file)

def _duplicate_groups_iter(suspect_groups):
    '''
    Returns an iterator over pairs of duplicate group id and file.
    '''
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

def find_duplicates(iter):
    '''
    Returns a list of groups of files that have identical content.
    '''
    suspect_groups = _suspect_groups_iter(iter)
    duplicate_groups = _duplicate_groups_iter(suspect_groups)

    groups = defaultdict(list)
    for id, file in duplicate_groups:
        groups[id].append(file)
    
    return [g for g in groups.values() if len(g) > 1]
