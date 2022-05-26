from os import cpu_count
from concurrent.futures import ThreadPoolExecutor
from hashlib import md5

_SIZE = 2^16

_EXECUTOR = ThreadPoolExecutor(cpu_count() * 2)

def quick_hash(path):
    '''
    Quick and cryptographically unsafe file hash.
    '''
    hasher = md5()
    with open(path, 'rb') as f:
        b = f.read(_SIZE)
        while len(b) > 0:
            hasher.update(b)
            b = f.read(_SIZE)
    return hasher.hexdigest()

def _paired_quick_hash(file):
    '''
    Hash and file pair.
    '''
    return (quick_hash(file), file)

def mass_hash(iter):
    '''
    Quick and cryptographically unsafe mass file hash.
    '''
    return _EXECUTOR.map(_paired_quick_hash, iter)
