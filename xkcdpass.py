import argparse
import functools
import secrets
import string

def between(a, b):
    def _(word):
        return a <= len(word) <= b
    return _

def doesnot(f):
    functools.wraps(f)
    def wrapper(word):
        return not f(word)
    return wrapper

def has_punctuation(word):
    return set(string.punctuation).intersection(word)

class XKCDPass:

    def __init__(self,
                nwords = 4,
                pretransforms = None,
                prefilters = None,
                dictfile = '/usr/share/dict/words',
            ):
        """
        :param nwords: number of words in a password
        :param pretransforms: sequence of callables cummulatively called on
                              each word when loaded.
        :param prefilters: sequence of callables, any of which throws out a
                           word after pretransforms.
        :param dictfile: path to dictionary file.
        """
        self.nwords = nwords
        if pretransforms is None:
            pretransforms = [str.strip, str.lower]
        self.pretransforms = pretransforms
        if prefilters is None:
            prefilters = [between(4, 6), doesnot(has_punctuation)]
        self.prefilters = prefilters
        self.words = None
        self.dictfile = dictfile
        self.load_words()

    def _pretransforms(self, word):
        s = word
        for func in self.pretransforms:
            s = func(s)
        return s

    def _prefilters(self, word):
        return all(func(word) for func in self.prefilters)

    def load_words(self):
        with open(self.dictfile) as f:
            self.words = (self._pretransforms(word) for word in f)
            self.words = [word for word in self.words if self._prefilters(word)]

    def password(self):
        password = ' '.join(secrets.choice(self.words) for i in range(self.nwords))
        return password

def main(argv=None):
    """
    Generate xkcd passwords.
    """
    parser = argparse.ArgumentParser(description=main.__doc__, prog='xkcdpass')
    parser.add_argument('-n', '--num', type=int, default=10,
                        help='Number of passwords to generate. Default: %(default)s')
    args = parser.parse_args(argv)
    xkcdpass = XKCDPass()
    passwords = (xkcdpass.password() for _ in range(args.num))
    print('\n'.join(passwords))

if __name__ == '__main__':
    main()
