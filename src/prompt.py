_yes = ['y', 'yes']
_no = ['n', 'no']
_yes_or_no = _yes + _no

def prompt(txt: str) -> bool:
    '''
    Prompts user for yes or no with provided text.
    '''
    _prompt_print(txt)
    answer = input()
    while answer not in _yes_or_no:
        print("Invalid answer, try again.")
        _prompt_print(txt)
        answer = input()
    answer in _yes

def _prompt_print(txt: str):
    '''
    Prints the prompt and possible answers.
    '''
    print(txt)
    print("[y]es / [n]o")
