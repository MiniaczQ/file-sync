import argparse
from pathlib import Path

def args():
    '''
    Parses and validates command line arguments.
    '''

    parser = argparse.ArgumentParser(description="File synchronization utility.")
    parser.add_argument('target', help="Target directory.")
    parser.add_argument('-s', "--source", dest="sources", action="append", help="Source directories.")
    parser.add_argument('-m', '--move', action='store_true', help="Move missing files to target directory.")
    parser.add_argument('-d', '--duplicates', action='store_true', help="Check for files that have the same content.")
    parser.add_argument('-e', '--empty', action='store_true', help="Check for files that are empty.")
    parser.add_argument('-n', '--name', action='store_true', help="Check for files that have the same name.")
    parser.add_argument('-t', '--temporary', action='store_true', help="Check for files that are temporary.")
    parser.add_argument('-r', '--rights', action='store_true', help="Check for unusual rights in files metadata.")
    parser.add_argument('-c', '--characters', action='store_true', help="Check for problematic characters in file names.")
    parser.add_argument('-a', '--all', action='store_true', help="Perform all suggested actions without asking.")

    args = parser.parse_args()

    if not Path(args.target).is_dir():
        print(f"Target `{args.target}` is not a valid path.")
        exit()

    for source in args.sources:
        if not Path(source).is_dir():
            print(f"Source `{source}` is not a valid path.")
            exit()
    
    return args
