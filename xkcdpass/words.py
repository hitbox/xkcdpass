import os

from .external import nltk
from .external import wordfreq
from .external import zxcvbn

def resolve_words(path):
    if os.path.exists(path):
        with open(path) as file:
            return [line.strip() for line in file]

    if wordfreq:
        return wordfreq.iter_wordlist('en')

    if nltk:
        from nltk.corpus import nltk_words
        try:
            return nltk_words.words()
        except LookupError as e:
            raise RuntimeError(
                'nltk installed but words not found. Use nltk.downloader'
                ' to download words.')

    raise RuntimeError('No word source found.')
