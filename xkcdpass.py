import argparse
import random
import secrets
import string

WRAPPERS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
    '"': '"',
}
WRAPPERS.update({v:k for k, v in WRAPPERS.items()})

class add_number:

    def __call__(self, word):
        return f'{word}{random.randrange(10)}'


class add_special:

    def __init__(self, wrap=False):
        self.wrap = wrap

    def __call__(self, word):
        char = secrets.choice(string.punctuation)
        if self.wrap and char in WRAPPERS:
            opp = WRAPPERS[char]
            left, right = sorted([char, opp])
            return f'{left}{word}{right}'
        else:
            return f'{word}{char}'


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
    parser.add_argument('--separator', default=' ',
                        help='Word separator. Default: %(default)s')
    parser.add_argument('-N', '--number', action='store_true',
                        help='Randomly add a number.')
    parser.add_argument('-S', '--special', action='store_true',
                        help='Randomly insert a special character.')
    parser.add_argument('-W', '--wrap', action='store_true',
                        help='When the randomly selected special character is a'
                             ' wrapper, wrap the randomly selected word with'
                             ' it. Requires --special.')
    args = parser.parse_args(argv)
    if args.wrap and not args.special:
        parser.error('option --wrap requires -S/--special')

    modifiers = []
    if args.number:
        modifiers.append(add_number())
    if args.special:
        modifiers.append(add_special(wrap=args.wrap))

    has_punctuation = set(string.punctuation).intersection
    def predicate(word):
        return (args.minimum <= len(word) <= args.maximum
                and not has_punctuation(word))

    def post(word):
        return word.strip().lower()

    with open('/usr/share/dict/words') as dictfile:
        population = set(map(post, filter(predicate, dictfile)))

    def indexed_modifiers(words):
        indexes = random.sample(range(len(words)), len(modifiers))
        return zip(indexes, modifiers)

    def apply_modifiers(words):
        for index, modify in indexed_modifiers(words):
            words[index] = modify(words[index])

    for _ in range(args.num):
        words = random.sample(population, args.nwords)
        apply_modifiers(words)
        print(args.separator.join(words))

if __name__ == '__main__':
    main()
