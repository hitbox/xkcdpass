import os

from collections import ChainMap

SEPARATORS = '-./:;@_|'

DEFAULTS = {
    'words': '/usr/share/dict/words',
    'separators': SEPARATORS,
    'nwords': 3,
    'npasswords': 10,
    'minimum_length': 14,
    'min_word_length': 3,
    'max_word_length': 8,
}

ENVVARS = {
    'words': os.getenv('XKCDPASS_WORDS'),
    'separators': os.getenv('XKCDPASS_SEPARATORS'),
}

def strip_none(dict_):
    return {k: v for k, v in dict_.items() if v is not None}

def config_from_args(args):
    config = ChainMap(
        strip_none(vars(args)),
        strip_none(ENVVARS),
        strip_none(DEFAULTS),
    )
    return config
