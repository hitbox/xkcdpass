from .argument_parser import parse_args
from .core import generate_password
from .core import print_all_passwords
from .core import read_population

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
