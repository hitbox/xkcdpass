import random
import string

from abc import ABC
from abc import abstractmethod

from .constant import ALL_SPECIALS
from .constant import EASYWRAPCHARS
from .constant import LEET_MAP
from .constant import RIGHT_HAND_SEPARATORS
from .constant import RIGHT_HAND_SPECIALS
from .constant import SPECIALS
from .constant import WRAPCHARS

class Mutator(ABC):

    @abstractmethod
    def __call__(self, strings):
        pass


class InsertCharacter(Mutator):
    """
    Randomly insert a random character into a list.
    """

    def __init__(self, population, start=0):
        self.population = population
        self.start = start

    def __call__(self, string_list):
        assert isinstance(string_list, list)
        assert all(isinstance(item, str) for item in string_list)
        index = random.randrange(self.start, len(string_list))
        string_list.insert(index, random.choice(self.population))


class InsertWrapping(Mutator):

    def __init__(self, wrappers, start=0):
        assert all(len(wrapper) == 2 for wrapper in wrappers)
        self.wrappers = wrappers
        self.start = start

    def __call__(self, string_list):
        assert isinstance(string_list, list)
        assert all(isinstance(item, str) for item in string_list)
        index = random.randrange(self.start, len(string_list))

        left, right = random.choice(self.wrappers)

        string_list.insert(index + 1, right)
        string_list.insert(index, left)


class ModifyWord(Mutator):

    def __init__(self, modifier, start=0):
        self.modifier = modifier
        self.start = start

    def __call__(self, string_list):
        assert isinstance(string_list, list)
        assert all(isinstance(item, str) for item in string_list)
        index = random.randrange(self.start, len(string_list))
        word = string_list[index]
        string_list[index] = self.modifier(word)


insert_digit = InsertCharacter(string.digits)

insert_digit_after_first = InsertCharacter(string.digits, start=1)

insert_special_after_first = InsertCharacter(SPECIALS, start=1)

insert_wrapping = InsertWrapping(WRAPCHARS)

insert_easy_wrapping = InsertWrapping(EASYWRAPCHARS)

insert_easier_wrapping_after_first = InsertWrapping(('[]',"''"), start=1)

capitalize_word = ModifyWord(lambda word: word.capitalize())

def _wrap(word):
    left, right = random.choice(['[]', "''", '{}'])
    return f'{left}{word}{right}'

wrap_word_after_first = ModifyWord(_wrap, start=1)
