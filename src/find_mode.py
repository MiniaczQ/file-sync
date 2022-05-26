def _create_matcher(pattern):
    '''
    Returns a function that can decide whether an `ST_MODE` fits the pattern.
    '''
    mask = 0b1111111111
    high = 0
    low = 0

    for (p, c) in zip(pattern, 'drwxrwxrwx'):
        high = high << 1
        low = low << 1

        if p == c:
            high += 1
            low += 1
        elif p == '_':
            high += 1
    
    def matcher(x):
        x = x & mask
        return (high ^ x) & (low ^ x) == 0
    
    return matcher

def _mode_iter(iter, pattern):
    '''
    Returns an iterator over files that don't match the pattern.
    '''
    matcher = _create_matcher(pattern)

    for f in iter:
        if not matcher(f.stat().st_mode):
            yield f
        

def find_mode(iter, pattern):
    '''
    Returns a list of files that have incorrect `ST_MODE`.
    '''
    return list(_mode_iter(iter, pattern))
