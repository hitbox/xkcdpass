import argparse
import os

from collections import ChainMap
from configparser import ConfigParser
from types import SimpleNamespace

from .constant import RIGHT_HAND_SEPARATORS

def argument_parser():
    parser = argparse.ArgumentParser(
        description = 'Generate xkcd passwords.',
        prog = 'xkcdpass',
    )
    # TODO
    # - the default will fail when running from an installed location like ~/.local/bin
    parser.add_argument(
        '--words-file',
        type = argparse.FileType(),
        help = 'Line separated words file.',
    )
    parser.add_argument(
        '-p', '--numpasswords',
        type = int,
        default = 10,
        help = 'Number of passwords to generate. Default: %(default)s',
    )
    parser.add_argument(
        '-n', '--nwords',
        type = int,
        default = 4,
        help = 'Number of words in a password. Default: %(default)s',
    )
    parser.add_argument(
        '--minletters',
        type = int,
        default = 4,
        help = 'Minimum number of letters per word. Default: %(default)s',
    )
    parser.add_argument(
        '--maxletters',
        type = int,
        default = 6,
        help = 'Maximum number of letters per word. Default: %(default)s',
    )
    parser.add_argument(
        '-s', '--separators',
        default = RIGHT_HAND_SEPARATORS,
        help = 'Word separator(s). Default: "%(default)s"',
    )
    parser.add_argument(
        '--seed',
        type = int,
        help = 'Set the random seed from integer.',
    )

    # flags
    parser.add_argument(
        '-C', '--capitalize',
        action = 'store_true',
        help = 'Randomly capitalize one of the words.',
    )
    parser.add_argument(
        '-N', '--number',
        action = 'store_true',
        help = 'Randomly add a number.',
    )
    parser.add_argument(
        '-S', '--special',
        action = 'store_true',
        help = 'Randomly place a special character on a word.',
    )
    parser.add_argument(
        '-W', '--wrap',
        action = 'store_true',
        help = 'Randomly wrap a word, with like brackets or quotes.',
    )
    parser.add_argument(
        '--starts-with-letter',
        action = 'store_true',
        help = 'Password must start with a letter.',
    )
    parser.add_argument(
        '--easy-wrap',
        action = 'store_true',
        help = 'Use easier to type wrapping characters.',
    )
    parser.add_argument(
        '--score',
        action = 'store_true',
        help = 'Show password score. Requires zxcvbn.',
    )
    parser.add_argument(
        '--min-length',
        type = int,
        default = 14,
        help = 'Minimum password length. Default: %(default)s',
    )
    parser.add_argument(
        '--ideas',
        action = 'store_true',
        help = 'Run with ideas. Experimental.',
    )
    return parser

def parse_args(argv=None):
    """
    Parse command line arguments.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)
    system_config = '/etc/xkcdpass/xkcdpass.ini'
    user_config = os.path.expanduser('~/.config/xkcdpass/xkcdpass.ini')
    # Read keys from ini to act as fallback for command line arguments.
    cp = ConfigParser()
    cp.read([system_config, user_config])
    section = cp['xkcdpass']
    args_dict = {k: v for k, v in vars(args).items() if v is not None}
    result = SimpleNamespace(**ChainMap(args_dict, dict(section)))
    return result
