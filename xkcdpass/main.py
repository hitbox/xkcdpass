from string import ascii_lowercase

from .argument_parser import argument_parser
from .character_filter import CharacterFilter
from .config import config_from_args
from .external import zxcvbn
from .password import create_password
from .words import resolve_words

def main(argv=None):
    """
    Generate xkcd passwords.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)
    config = config_from_args(args)

    separators = config['separators']
    npasswords = config['npasswords']
    nwords = config['nwords']
    minimum_length = config['minimum_length']
    min_word_length = config['min_word_length']
    max_word_length = config['max_word_length']

    filter_ = CharacterFilter(valid=ascii_lowercase, invalid_if_all='xvi')
    words = resolve_words(config['words'])
    words = [
        word for word in words
        if min_word_length <= len(word) <= max_word_length
        and filter_(word)
    ]

    passwords = []
    for _ in range(npasswords):
        password = create_password(words, nwords, separators, minimum_length)

        if zxcvbn:
            result = zxcvbn(password)
            output = (password, result['score'])
        else:
            output = (password, None)

        passwords.append(output)

    passwords = sorted(passwords, key=lambda item: (len(item[0]), item[1]))
    for password, score in passwords:
        if score is not None:
            print(f'{score}/4 {password}')
        else:
            print(password)
