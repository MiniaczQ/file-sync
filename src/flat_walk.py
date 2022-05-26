from os import walk, path
from pathlib import Path

def flat_walk(root):
    '''
    Flattens nested calls of `os.walk`.
    Returns all files.
    '''
    return map(lambda p: Path(p), _inner_flat_walk(root))    

def _inner_flat_walk(root):
    for root, dirs, files in walk(root):
        ancestors = root
        for file in files:
            yield path.join(ancestors, file)
        for dir in dirs:
            ancestors = path.join(root, dir)
            for file in flat_walk(dir):
                yield path.join(ancestors, file)
