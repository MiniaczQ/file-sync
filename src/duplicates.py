from collections import defaultdict
import filecmp

from hash import mass_hash

def _cmp(a, b) -> bool:
    '''
    Deeply compares files `a` and `b`.
    '''
    return filecmp.cmp(a, b, shallow=False)

def _find(l, p):
    '''
    Find the index of first element that fits the predicate.
    '''
    i = (idx for idx, v in enumerate(l) if p(v))
    r = next(i)
    i.close()
    return r if r != StopIteration else None

def _find_suspects(iter):
    '''
    Groups all files by their hashes.
    Files with the same hash are suspected to be duplicates.
    '''
    suspects = defaultdict(list)
    for hash, file in mass_hash(iter):
        suspects[hash].append(file)

    suspect_groups = filter(lambda l: len(l) > 1, suspects.values())

    return suspect_groups

def _clash_suspects(suspects):
    '''
    Compares file of files with the same hash.
    '''
    duplicate_groups = []

    for files in suspects:
        file = files[0]
        local_groups = [[file]]

        for file in files[1:]:
            r = _find(local_groups, lambda g: _cmp(g[0], file))
            if r is not None:
                local_groups[r].append(file)
            else:
                local_groups.append([file])
        
        duplicate_groups.extend(local_groups)
    
    return duplicate_groups

def find_duplicates(iter):
    '''
    Returns a list of groups of files that have identical content.
    '''
    suspect_groups = _find_suspects(iter)
    return _clash_suspects(suspect_groups)
