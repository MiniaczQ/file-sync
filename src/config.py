import json

def _validate_mode_pattern(pattern) -> bool:
    '''
    Returns if pattern can be used for filtering.
    Exits otherwise.
    '''
    if len(pattern) != 10:
        print('Mode pattern has to be 10 characters long!')
        exit()
    for (p, c) in zip(pattern, 'drwxrwxrwx'):
        if p != c and p != '-' and p != '_':
            print("Mode pattern can only consist of '-', '_' or 'drwxrwxrwx' in respective places.")
            exit()

class Config:
    '''
    Structure that holds configuration data.
    '''
    def __init__(self, pattern, symbols, endings, substitute):
        self.pattern = pattern
        self.symbols = symbols
        self.endings = endings
        self.substitute = substitute

def load_config():
    '''
    Loads and validates the config file.
    '''
    with open('config.json', 'r') as f:
        config = json.load(f)
        
        pattern = config.pop('pattern', '__________')
        if type(pattern) != str:
            print('Configuration parameter `pattern` has to be a string.')
            exit()
        _validate_mode_pattern(pattern)
        
        symbols = config.pop('symbols', '')
        if type(symbols) != str:
            print('Configuration parameter `symbols` has to be a string.')
            exit()
        
        endings = config.pop('endings', [])
        if type(endings) != list:
            print('Configuration parameter `endings` has to be a list of strings.')
            exit()
        for ending in endings:
            if type(ending) != str:
                print('Configuration parameter `endings` has to be a list of strings.')
                exit()
        
        substitute = config.pop('substitute', '_')
        if type(substitute) != str:
            print('Configuration parameter `substitute` has to be a string.')
            exit()
        if len(substitute) != 1:
            print('Configuration parameter `substitute` has to be exactly 1 character.')
            exit()

        for key in config.keys():
            print(f'Invalid configuration parameter `{key}`.')
            exit()

        return Config(pattern, symbols, endings, substitute)
