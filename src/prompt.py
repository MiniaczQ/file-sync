def prompt(message, handler):
    """
    Prompts user for yes or no with provided text.
    """
    answer = _grab(message)
    res = handler(answer)
    while res is None:
        print("Invalid answer, try again.")
        answer = _grab(message)
        res = handler(answer)
    return res


def _grab(message):
    print()
    print(message)
    return input()
