from os import path

def _empty_iter(iter):
    '''
    Returns an iterator over empty files.
    '''
    for f in iter:
        if path.getsize(f) == 0:
            yield f
    
def find_empty(iter):
    '''
    Returns a list of empty files.
    '''
    return list(_empty_iter(iter))
