import argparse
from collections import deque
from pathlib import Path
from queue import Queue

class MyAction(argparse.Action):
    def __init__(self, option_strings, name='', options=[], **kwargs):
        kwargs['nargs'] = '?'
        kwargs['dest'] = 'action_queue'
        kwargs['default'] = None
        self.dest = 'action_queue'
        self.name = name
        self.options = options
        super().__init__(option_strings, **kwargs)

    def __call__(self, p: argparse.ArgumentParser, n, v, s):
        q = getattr(n, 'action_queue', None)
        if q is None:
            q = deque()
        if v is None:
            q.append((self.name, 'interact'))
            setattr(n, 'action_queue', q)
        else:
            if v in self.options:
                q.append((self.name, v))
                setattr(n, 'action_queue', q)
            else:
                p.error(f'Flag `{s}` does not accept value `{v}`.')

def parse_args():
    '''
    Parses and validates command line arguments.
    '''

    parser = argparse.ArgumentParser(description="File synchronization utility.")
    parser.add_argument('target', help="Target directory.")
    parser.add_argument('-s', '--source', dest='sources', action='append', default=[], help='Source directories.')
    parser.add_argument('-m', '--move', action=MyAction, options=['all'], name='move', help="Move missing files from source directories to target directory.")
    parser.add_argument('-d', '--duplicates', action=MyAction, options=['rm-old', 'rm-young'], name='duplicate', help="Check for files that have the same content in target directory.")
    parser.add_argument('-e', '--empty', action=MyAction, options=['all'], name='empty', help="Check for files that are empty in target directory.")
    parser.add_argument('-n', '--namesakes', action=MyAction, options=['rm-old', 'rm-young'], name='namesakes', help="Check for files that have the same name in target directory.")
    parser.add_argument('-t', '--temporary', action=MyAction, options=['all'], name='temporary', help="Check for files that are temporary in target directory.")
    parser.add_argument('-r', '--rights', action=MyAction, options=['all'], name='mode', help="Check for unusual rights in files metadata in target directory.")
    parser.add_argument('-c', '--characters', action=MyAction, options=['all'], name='symbols', help="Check for problematic characters in file names in target directory.")

    args = parser.parse_args()

    if len(args.sources) == 0 and any(x[0] == 'move' for x in args.action_queue):
        print(f'Move action is invalid with no sources.')
        exit()

    if not Path(args.target).is_dir():
        print(f"Target `{args.target}` is not a valid path.")
        exit()

    for source in args.sources:
        if not Path(source).is_dir():
            print(f"Source `{source}` is not a valid path.")
            exit()
    
    return args
