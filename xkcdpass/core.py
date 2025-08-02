import random
import string

from .constant import EASYWRAPCHARS
from .constant import SPECIALS
from .constant import WRAPCHARS

try:
    from zxcvbn import zxcvbn
except ImportError:
    zxcvbn = None

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
    separators,
    number = None,
    special = None,
    wrap = None,
    capitalize = None,
    start_with_letter = False,
    easy_wrap = False,
):
    """
    Generate an XKCD style password. https://xkcd.com/936/

    :param population:
        List of words to use in random password generation.
    :param nwords:
        Number of words in password.
    :param separators:
        Words separators.
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
    :easy_wrap:
        Use wrapping chars that don't require shift.
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
        if easy_wrap:
            wrapchars = EASYWRAPCHARS
        else:
            wrapchars = WRAPCHARS
        lchar, rchar = random.choice(wrapchars)
        word = words[index]
        words[index] = lchar + word + rchar

    password = ''
    for nth, word in enumerate(words, start=1):
        password += word
        if nth != len(words):
            password += random.choice(separators)

    return password

def read_population(filename):
    """
    Read words from file.
    """
    if isinstance(filename, str):
        with open(filename) as words_file:
            population = (line.strip() for line in words_file.readlines())
    else:
        population = (line.strip() for line in filename)
    return population

def print_all_passwords(
    population,
    numpasswords,
    min_length,
    show_score,
    nwords,
    separators,
    number,
    special,
    wrap,
    capitalize,
    starts_with_letter,
    easy_wrap,
):
    n = 0
    while n < numpasswords:
        try:
            password = generate_password(
                population,
                nwords,
                separators,
                number,
                special,
                wrap,
                capitalize,
                starts_with_letter,
                easy_wrap,
            )
        except IndexError:
            pass
        else:
            if len(password) >= min_length:
                if zxcvbn:
                    result = zxcvbn(password)
                    if show_score:
                        print(f'{result["score"]}/4 - {result["password"]}')
                    else:
                        print(password)
                else:
                    print(password)
                n += 1
