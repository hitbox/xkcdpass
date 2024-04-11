#!/usr/bin/env python
import argparse
import os
import random
import string

from collections import ChainMap
from collections import UserList
from configparser import ConfigParser
from types import SimpleNamespace

WRAPCHARS = ('()', '[]', '{}', '<>', '""', "''", '//')
SPECIALS = '!@#$%^&*'

class XKCDPassError(Exception):
    pass


class InfiniteShuffle(UserList):
    """
    An infinite shuffle list.
    """

    def __init__(self, initlist):
        super().__init__(initlist)
        self.initlist = list(self)

    def _reset(self):
        self.extend(self.initlist)
        random.shuffle(self)

    def pop(self, i=-1):
        if not self:
            self._reset()
        return super().pop(i)

    def peek(self, i=-1):
        return self[i]


def capitalize(word):
    """
    Capitalize function that capitalizes the first letter character.
    """
    for i, c in enumerate(word):
        if c in string.ascii_letters:
            break
    else:
        raise XKCDPassError('Letter not found')
    return word[:i] + word[i:].capitalize()

def argument_parser():
    parser = argparse.ArgumentParser(
        description = main.__doc__,
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
        '-s', '--separator',
        default = ' ',
        help = 'Word separator. Default: "%(default)s"',
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
    return parser

def parse_args(argv=None):
    """
    Parse command line arguments.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)
    system_config = '/etc/xkcdpass/xkcdpass.ini'
    user_config = os.path.expanduser('~/.config/xkcdpass/xkcdpass.ini')
    cp = ConfigParser()
    cp.read([system_config, user_config])
    section = cp['xkcdpass']
    args_dict = {k: v for k, v in vars(args).items() if v is not None}
    result = SimpleNamespace(**ChainMap(args_dict, dict(section)))
    return result

def random_insert(word, char):
    if random.choice([True, False]):
        return word + char
    else:
        return char + word

def generate_password(
    population,
    nwords,
    separator,
    number = None,
    special = None,
    wrap = None,
    capitalize = None,
):
    words = random.sample(population, nwords)
    indexes = InfiniteShuffle(range(len(words)))

    if capitalize:
        # peek to allow used again
        index = indexes.peek()
        words[index] = words[index].capitalize()

    if number:
        # randomly add number to end of number
        index = indexes.pop()
        word = words[index]
        digit = random.choice(string.digits)
        words[index] = random_insert(word, digit)

    if special:
        index = indexes.pop()
        word = words[index]
        special = random.choice(SPECIALS)
        words[index] = random_insert(word, special)

    if wrap:
        index = indexes.pop()
        lchar, rchar = random.choice(WRAPCHARS)
        word = words[index]
        words[index] = lchar + word + rchar

    return separator.join(words)

def main(argv=None):
    """
    Generate xkcd passwords.
    """
    args = parse_args(argv)

    def wordsize(word):
        return args.minletters <= len(word) <= args.maxletters

    if isinstance(args.words_file, str):
        with open(args.words_file) as words_file:
            population = [line.strip() for line in words_file.readlines()]
    else:
        population = (line.strip() for line in args.words_file)

    population = [word for word in population if wordsize(word)]

    genargs = (
        population,
        args.nwords,
        args.separator,
        args.number,
        args.special,
        args.wrap,
        args.capitalize,
    )

    for _ in range(args.numpasswords):
        password = generate_password(*genargs)
        print(password)

if __name__ == '__main__':
    main()
