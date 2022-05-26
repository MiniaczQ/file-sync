def _symbols_iter(iter, symbols):
    '''
    Returns an iterator over files that names contain any of the provided symbols.
    '''
    for f in iter:
        if any(s in f.name for s in symbols):
            yield f

def find_symbols(iter, symbols):
    '''
    Returns a list of files that names contain ant of the provided symbols.
    '''
    return list(_symbols_iter(iter, symbols))
