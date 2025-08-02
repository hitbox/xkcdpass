from abc import ABC
from abc import abstractmethod

class Mutator(ABC):

    @abstractmethod
    def __call__(self, strings):
        pass


class AddDigit(Mutator):

    def __init__(self, whitespace, avoid_first=True):
        self.whitespace = whitespace
        self.avoid_first = avoid_first

    def __call__(self, strings):
        assert isinstance(string, list)
        assert all(isinstance(item, str) for item in strings)
        result = strings.copy()
        # TODO

        indexes = list(range(len(strings)))
        index = random.choice(indexes)
        # Want to make a new list and modify it and return it.
        # A list of string is great because string are immutable. Just copy the list.

        part = random.choice(strings)
        insert_start = random.choice([True, False])
        if insert_start and self.avoid_first and strings.index(part) == 0:
            insert_start = False
        if insert_start:
            pass


class SubstituteDigit(Mutator):

    def __init__(self, replaceable):
        """
        :param replaceable:
            Iterable of characters it is permitted to replace with digits. If a
            mapping, then the values are an iterable of replacement characters.
        """
        self.replaceable = replaceable

    def __call__(self, string):
        pass
