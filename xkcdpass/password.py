from .mutator import capitalize_word
from .mutator import insert_digit_after_first
from .mutator import insert_easier_wrapping_after_first
from .mutator import insert_easy_wrapping
from .mutator import insert_special_after_first
from .mutator import insert_wrapping
from .mutator import wrap_word_after_first

class PasswordBuilder:

    def __init__(self, mutators):
        """
        """
        self.mutators = mutators

    def __call__(self, word_list):
        for mutator in self.mutators:
            mutator(word_list)


class XKCDPassword(PasswordBuilder):
    """
    """

    def __init__(self, mutators=None):
        """
        """
        if mutators is None:
            mutators = (
            )
        self.mutators = tuple(mutators)

    def __call__(self, word_list):
        """
        """

xkcd_password_builder = PasswordBuilder(
    mutators = (
        capitalize_word,
        wrap_word_after_first,
        #insert_digit_after_first,
        #insert_special_after_first,
        #insert_easier_wrapping_after_first,
    ),
)
