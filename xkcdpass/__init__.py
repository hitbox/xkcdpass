#!/usr/bin/env python
import argparse
import random
import string
from pathlib import Path

def main():
    """
    Generate xkcd passwords.
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-w', '--words', type=int, default=4,
                        help='Number of words in passwords.'
                             ' Default: %(default)s')
    parser.add_argument('-n', '--num', type=int, default=10,
                        help='Number of passwords to generate.'
                             ' Default: %(default)s')
    parser.add_argument('-l', '--length', type=int, default=6,
                        help='Select only words with this or less length.'
                             ' Default: %(default)s')
    parser.add_argument('-p', '--no-punctuation', action='store_true',
                        help='No punctuation characters. Default: %(default)s')
    parser.add_argument('--wordspath', default=Path('/usr/share/dict/words'),
                        help='Path to words. Default: %(default)s')
    args = parser.parse_args()

    if not args.wordspath.exists():
        parser.error('%s must exist.' % wordspath)

    if args.no_punctuation:
        def predicate(word):
            return len(word) <= args.length
    else:
        punctuation = set(string.punctuation)
        def predicate(word):
            return punctuation.isdisjoint(word) and len(word) <= args.length

    words = set(word.lower().strip() for word in open(args.wordspath) if predicate(word))
    passwords = (' '.join(random.sample(words, args.words)) for _ in range(args.num))
    print('\n'.join(passwords))
