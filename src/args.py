import argparse
from collections import deque
from pathlib import Path


class MyAction(argparse.Action):
    def __init__(self, option_strings, name="", options=[], **kwargs):
        kwargs["nargs"] = "?"
        kwargs["default"] = None
        self.dest = "action_queue"
        self.name = name
        self.options = options
        super().__init__(option_strings, **kwargs)

    def __call__(self, p: argparse.ArgumentParser, n, v, s):
        q = getattr(n, "action_queue", None)
        if q is None:
            q = deque()
        if v is None:
            q.append((self.name, "interact"))
            setattr(n, "action_queue", q)
        else:
            v = v.lower()
            if v in self.options:
                q.append((self.name, v))
                setattr(n, "action_queue", q)
            else:
                p.error(f"Flag `{s}` does not accept value `{v}`.")


def parse_args():
    """
    Parses and validates command line arguments.
    """

    parser = argparse.ArgumentParser(description="File synchronization utility.")
    parser.add_argument("target", help="Target directory.")
    parser.add_argument(
        "-s",
        "--source",
        dest="source",
        action="append",
        default=[],
        help="A source directory. Use multiple times for multiple source directories.",
    )
    parser.add_argument(
        "--config",
        dest="config",
        action="store",
        help="Custom configuration file.",
    )
    parser.add_argument(
        "-c",
        "--copy",
        name="copy",
        dest="rm-all",
        options=["cp-all"],
        action=MyAction,
        help="Copy missing (content-wise) files from source directories to target directory. Add `cp-all` to copy all.",
    )
    parser.add_argument(
        "-d",
        "--duplicates",
        name="duplicates",
        dest="rm-old|rm-young",
        options=["rm-old", "rm-young"],
        action=MyAction,
        help="Check for files that have the same content in target directory. Add `rm-old` or `rm-young` to remove all.",
    )
    parser.add_argument(
        "-e",
        "--empty",
        name="empty",
        dest="rm-all",
        options=["rm-all"],
        action=MyAction,
        help="Check for files that are empty in target directory. Add `rm-all` to remove all.",
    )
    parser.add_argument(
        "-n",
        "--namesakes",
        name="namesakes",
        dest="rm-old|rm-young",
        options=["rm-old", "rm-young"],
        action=MyAction,
        help="Check for files that have the same name in target directory. Add `rm-old` or `rm-young` to remove all.",
    )
    parser.add_argument(
        "-t",
        "--temporary",
        name="endings",
        dest="rm-all",
        options=["rm-all"],
        action=MyAction,
        help="Check for files that are temporary in target directory. Add `rm-all` to remove all.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        name="mode",
        dest="ch-all",
        options=["ch-all"],
        action=MyAction,
        help="Check for unusual file modes (like rwxrwxrwx) in target directory. Add `ch-all` to change all.",
    )
    parser.add_argument(
        "-i",
        "--illnamed",
        name="illnamed",
        dest="re-all",
        options=["re-all"],
        action=MyAction,
        help="Check for illnamed (using blacklisted characters) files in target directory. Add `re-all` to rename all.",
    )

    args = parser.parse_args()

    if getattr(args, "action_queue", None) is None:
        print("No actions provided.")
        exit()

    if len(args.source) == 0 and any(x[0] == "copy" for x in args.action_queue):
        print(f"Copy action is invalid without source directories.")
        exit()

    if len(args.source) > 0 and all(x[0] != "copy" for x in args.action_queue):
        print(f"Source directories are invalid without copy action.")
        exit()

    if not Path(args.target).is_dir():
        print(f"Target directory `{args.target}` is invalid.")
        exit()

    for source in args.source:
        if not Path(source).is_dir():
            print(f"Source directory `{source}` is invalid.")
            exit()

    return args
