def validate_mode_pattern(pattern) -> bool:
    '''
    Returns `True` if pattern can be used for filtering.
    `False` otherwise.
    '''
    if len(pattern) != 10:
        return False
    for (p, c) in zip(pattern, 'drwxrwxrwx'):
        if p != c and p != '_':
            return False
    return True
