import argparse

def argument_parser():
    parser = argparse.ArgumentParser(
        description = 'Generate passwords, xkcd style.',
    )

    parser.add_argument(
        '--words',
        help = 'Path to words file.',
    )

    parser.add_argument(
        '--separators',
        help = 'String of characters to randomly choose a separator.',
    )

    parser.add_argument(
        '--nwords',
        type = int,
        help = 'Number of words in passwords.',
    )

    parser.add_argument(
        '--npasswords',
        type = int,
        help = 'Number of passwords to generate.',
    )

    parser.add_argument(
        '--minimum-length',
        type = int,
        help = 'Minimum length of password.',
    )

    parser.add_argument(
        '--min-word-length',
        type = int,
        help = 'Minimum length of words.',
    )

    parser.add_argument(
        '--max-word-length',
        type = int,
        help = 'Maximum length of words.',
    )

    return parser
