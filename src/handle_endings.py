def _endings_iter(iter, endings):
    '''
    Returns an iterator over files that have specific name endings.
    '''
    for f in iter:
        for ending in endings:
            if str(f).endswith(ending):
                yield f

def find_endings(iter, endings):
    '''
    Returns a list of files that have specific name endings.
    '''
    return list(_endings_iter(iter, endings))
