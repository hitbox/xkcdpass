#!/usr/bin/env python
import argparse
import os
import random
import string

WRAPPERS = dict(('()', '[]', '{}', '""', '//'))
WRAPPERS.update({v:k for k, v in WRAPPERS.items()})

def main(argv=None):
    """
    Generate xkcd passwords.
    """
    parser = argparse.ArgumentParser(description=main.__doc__, prog='xkcdpass')
    parser.add_argument('-n', '--num', type=int, default=10,
                        help='Number of passwords to generate. Default: %(default)s')
    parser.add_argument('--nwords', type=int, default=4,
                        help='Number of words in a password. Default: %(default)s')
    parser.add_argument('--minimum', type=int, default=4,
                        help='Minimum number of letters per word. Default: %(default)s')
    parser.add_argument('--maximum', type=int, default=6,
                        help='Maximum number of letters per word. Default: %(default)s')
    parser.add_argument('-s', '--separator', default=' ',
                        help='Word separator. Default: "%(default)s"')
    parser.add_argument('-N', '--number', action='store_true',
                        help='Randomly add a number.')
    parser.add_argument('-S', '--special', action='store_true',
                        help='Randomly insert a special character.')
    parser.add_argument('-W', '--wrap', action='store_true',
                        help='When the randomly selected special character is a'
                             ' wrapper, wrap the randomly selected word with'
                             ' it. Requires --special.')
    parser.add_argument('-C', '--capitalize', action='store_true',
                        help='Randomly capitalize one of the words.')

    args = parser.parse_args(argv)
    if args.wrap and not args.special:
        args.special = True

    with open(os.path.join(os.path.dirname(__file__), 'words_alpha.txt')) as wordsfile:
        population = set(
            map(lambda word: word.strip(),
                filter(lambda word: args.minimum <= len(word) <= args.maximum,
                       wordsfile)))

    for _ in range(args.num):
        words = random.sample(population, args.nwords)
        indexes = random.sample(range(len(words)), 3)
        if args.number:
            words[indexes[0]] += str(random.randint(0, 9))
        if args.special:
            word = words[indexes[1]]
            if args.wrap:
                lchar = random.choice(list(WRAPPERS))
                rchar = WRAPPERS[lchar]
                lchar, rchar = sorted((lchar, rchar))
                words[indexes[1]] = lchar + word + rchar
            else:
                char = random.choice(string.punctuation)
                if random.randint(0,1):
                    words[indexes[1]] = word + char
                else:
                    words[indexes[1]] = char + word
        if args.capitalize:
            words[indexes[2]] = words[indexes[2]].capitalize()
        print(args.separator.join(words))

if __name__ == '__main__':
    main()
