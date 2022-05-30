from pathlib import Path
from args import parse_args
from config import load_config
from handle_duplicates import handle_duplicates
from handle_empty import handle_empty
from handle_copy import handle_copy
from handle_namesakes import handle_namesakes
from handle_mode import handle_mode
from handle_illnamed import handle_illnamed
from handle_endings import handle_endings


def run_action(action, option, target, sources, config):
    if action == "duplicates":
        handle_duplicates(target, option)
    elif action == "empty":
        handle_empty(target, option)
    elif action == "endings":
        handle_endings(target, option, config.endings)
    elif action == "mode":
        handle_mode(target, option, config.pattern)
    elif action == "copy":
        handle_copy(target, sources, option)
    elif action == "namesakes":
        handle_namesakes(target, option)
    elif action == "illnamed":
        handle_illnamed(target, option, config.symbols, config.substitute)


def main():
    args = parse_args()
    config = load_config(args.config)

    target = Path(args.target)
    sources = (Path(s) for s in args.source)

    for (action, option) in args.action_queue:
        run_action(action, option, target, sources, config)


if __name__ == "__main__":
    main()
