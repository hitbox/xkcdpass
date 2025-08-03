import random

from .argument_parser import parse_args
from .core import generate_password
from .core import print_all_passwords
from .core import read_population
from .password import xkcd_password_builder as password_builder

try:
    from zxcvbn import zxcvbn
except ImportError:
    zxcvbn = None

def ideas(args, population):
    for _ in range(args.numpasswords):
        word_list = random.sample(population, args.nwords)
        password_builder(word_list)

        separator = random.choice('_/')
        password = separator.join(word_list)

        if zxcvbn:
            result = zxcvbn(password)
            output = f'{result["score"]}/4 {password}'
        else:
            output = password

        print(output)

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

    population = [word for word in read_population(args.words_file) if wordsize(word)]

    if args.ideas:
        # TODO
        # React to chosen wrapper to make programmer-friendly passwords.
        # - if [] chosen: lower_case["Capitalized"]
        # - if {} chosen: lower_case={"word": "Capitalized"}
        # React to math chars:
        # - if +: one+two=three
        # - if -: three-two=one
        # React to others:
        # - if /: regex/some_random_words/
        #         word/Capitalized/another_word
        ideas(args, population)
    else:
        print_all_passwords(
            population = population,
            numpasswords = args.numpasswords,
            min_length = args.min_length,
            show_score = args.score,
            nwords = args.nwords,
            separators = args.separators,
            number = args.number,
            special = args.special,
            wrap = args.wrap,
            capitalize = args.capitalize,
            starts_with_letter = args.starts_with_letter,
            easy_wrap = args.easy_wrap,
        )
