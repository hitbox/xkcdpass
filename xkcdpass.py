#!/usr/bin/env python
import argparse
import random
import string
from pathlib import Path

wordspath = Path('/usr/share/dict/words')

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
    parser.add_argument('-l', '--length', type=int, default=10,
                        help='Select only words with this or less length.'
                             ' Default: %(default)s')
    args = parser.parse_args()

    if not wordspath.exists():
        parser.error('%s must exist.' % wordspath)

    punctuation = set(string.punctuation)
    words = list(set(word.lower().strip()
                     for word in open(wordspath)
                     if punctuation.isdisjoint(word)
                     and len(word) <= args.length))
    passwords = list(' '.join(random.sample(words, args.words))
                     for _ in range(args.num))
    print('\n'.join(passwords))

if __name__ == '__main__':
    main()
