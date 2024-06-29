#!/usr/bin/env python
import argparse
import os
import random
import string

from collections import ChainMap
from configparser import ConfigParser
from types import SimpleNamespace

WRAPCHARS = ('()', '[]', '{}', '<>', '""', "''", '//')
SPECIALS = '!@#$%^&*'

class XKCDPassError(Exception):
    pass


def random_insert(word, char):
    """
    Randomly insert a character to the beginning or end of a word.
    """
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
    start_with_letter = False,
):
    """
    Generate a password, XKCD-style.

    :param population:
        List of words to use in random password generation.
    :param nwords:
        Number of words in password.
    :param separator:
        Words separator.
    :param number:
        Randomly insert a number to the beginning or end of a word.
    :param special:
        Randomly insert a special character to the beginning or end of a word.
    :param wrap:
        Randomly wrap a word with wrapping characters like parenthesis.
    :capitalize:
        Randomly capitalize a word.
    :start_with_letter:
        Password will start with a letter.
    """
    words = random.sample(population, nwords)
    # use list of indexes and (usually) pop to avoid applying the special
    # character applications to the same word
    indexes = list(range(len(words)))
    random.shuffle(indexes)

    # apply optional capitalize first, so that we don't have to consider if the
    # word has uncapitalizable first character
    if capitalize:
        # peek to allow using word again
        index = indexes[-1]
        words[index] = words[index].capitalize()

    if number:
        # randomly add number to end of number
        index = indexes.pop()
        word = words[index]
        digit = random.choice(string.digits)
        if start_with_letter and index == 0:
            # always add to end for option
            words[index] += digit
        else:
            words[index] = random_insert(word, digit)

    if special:
        index = indexes.pop()
        word = words[index]
        special = random.choice(SPECIALS)
        if start_with_letter and index == 0:
            # always add to end for option
            words[index]  = word + special
        else:
            words[index] = random_insert(word, special)

    if wrap:
        index = indexes.pop()
        # pop until not first item for option
        # let empty list raise
        while start_with_letter and index == 0:
            index = indexes.pop()
        lchar, rchar = random.choice(WRAPCHARS)
        word = words[index]
        words[index] = lchar + word + rchar

    return separator.join(words)

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

def main(argv=None):
    """
    Generate xkcd passwords.
    """
    args = parse_args(argv)

    # check for attribute instead of truthy to avoid false for --seed 0 where
    # zero would be falsey
    if hasattr(args, 'seed'):
        random.seed(args.seed)

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
        args.starts_with_letter,
    )

    for _ in range(args.numpasswords):
        password = generate_password(*genargs)
        print(password)

if __name__ == '__main__':
    main()
