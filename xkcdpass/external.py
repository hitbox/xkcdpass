try:
    from zxcvbn import zxcvbn
except ImportError:
    zxcvbn = None

try:
    import nltk
except ImportError:
    nltk = None

try:
    import wordfreq
except ImportError:
    wordfreq = None
