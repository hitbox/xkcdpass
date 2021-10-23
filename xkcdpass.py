#!/usr/bin/env python
import argparse
import os
import random
import string

WRAPPERS = dict(('()', '[]', '{}', '""', '//'))
WRAPPERS.update({v:k for k, v in WRAPPERS.items()})

SPECIALS = '!@#$%^&*'

class XKCDPassError(Exception):
    pass


def main(argv=None):
    """
    Generate xkcd passwords.
    """
    parser = argparse.ArgumentParser(description=main.__doc__, prog='xkcdpass')
    parser.add_argument('-n', '--num', type=int, default=10,
                        help='Number of passwords to generate. Default: %(default)s')
    parser.add_argument('--nwords', type=int, default=4,
                        help='Number of words in a password. Default: %(default)s')
    parser.add_argument('--minletters', type=int, default=4,
                        help='Minimum number of letters per word. Default: %(default)s')
    parser.add_argument('--maxletters', type=int, default=6,
                        help='Maximum number of letters per word. Default: %(default)s')
    parser.add_argument('-s', '--separator', default=' ',
                        help='Word separator. Default: "%(default)s"')
    parser.add_argument('-N', '--number', action='store_true',
                        help='Randomly add a number.')
    parser.add_argument('-S', '--special', action='store_true',
                        help='Randomly place a special character on a word.')
    parser.add_argument('-W', '--wrap', action='store_true',
                        help='Randomly wrap a word in a wrapper, like brackets.')
    parser.add_argument('-C', '--capitalize', action='store_true',
                        help='Randomly capitalize one of the words.')

    args = parser.parse_args(argv)
    if args.wrap and not args.special:
        args.special = True

    def wordsize(word):
        return args.minletters <= len(word) <= args.maxletters

    words_path = os.path.join(os.path.dirname(__file__), 'words_alpha.txt')
    with open(words_path) as words_file:
        population = (line.strip() for line in words_file)
        population = [word for word in population if wordsize(word)]

    nspecial = sum([args.number, args.special, args.wrap, args.capitalize])

    for _ in range(args.num):
        words = random.sample(population, args.nwords)
        # choosing indexes to avoid modifying the same word
        indexes = random.sample(range(len(words)), nspecial)
        if args.number:
            # randomly add number to end of number
            index = indexes.pop()
            words[index] += str(random.randint(0, 9))

        if args.special:
            index = indexes.pop()
            word = words[index]
            special = random.choice(SPECIALS)
            # randomly beginning or end
            if random.choice([True, False]):
                words[index] = word + special
            else:
                words[index] = special + word

        if args.wrap:
            index = indexes.pop()
            lchar = random.choice(list(WRAPPERS))
            rchar = WRAPPERS[lchar]
            lchar, rchar = sorted((lchar, rchar))
            word = words[index]
            words[index] = lchar + word + rchar

        if args.capitalize:
            index = indexes.pop()
            words[index] = words[index].capitalize()

        if indexes:
            raise XKCDPassError('Random index(s) left over.')

        print(args.separator.join(words))

if __name__ == '__main__':
    main()
