#!/usr/bin/env python
import argparse
import os
import random
import string

from collections import UserList

WRAPPERS = dict(('()', '[]', '{}', '""', '//'))
WRAPPERS.update({v:k for k, v in WRAPPERS.items()})

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
        random.shuffle(self)

    def pop(self, i=-1):
        if not self:
            self.extend(self.initlist)
            random.shuffle(self)
        return super().pop(i)


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

    for _ in range(args.num):
        words = random.sample(population, args.nwords)
        # choosing indexes to avoid modifying the same word
        word_indexes = InfiniteShuffle(range(len(words)))

        if args.number:
            # randomly add number to end of number
            index = word_indexes.pop()
            words[index] += str(random.randint(0, 9))

        if args.special:
            index = word_indexes.pop()
            word = words[index]
            special = random.choice(SPECIALS)
            # randomly beginning or end
            if random.choice([True, False]):
                words[index] = word + special
            else:
                words[index] = special + word

        if args.wrap:
            index = word_indexes.pop()
            lchar = random.choice(list(WRAPPERS))
            rchar = WRAPPERS[lchar]
            lchar, rchar = sorted((lchar, rchar))
            word = words[index]
            words[index] = lchar + word + rchar

        if args.capitalize:
            index = word_indexes.pop()
            words[index] = capitalize(words[index])

        print(args.separator.join(words))

if __name__ == '__main__':
    main()
