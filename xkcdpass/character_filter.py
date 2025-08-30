class CharacterFilter:
    """
    Filter a string for valid characters and has none of the invalid_if_all characters.
    """

    def __init__(self, valid, invalid_if_all):
        self.valid = set(valid)
        self.invalid_if_all = set(invalid_if_all)

    def __call__(self, word):
        has_non_invalid_if_all = False

        for char in word:
            if char not in self.valid:
                return False
            if char not in self.invalid_if_all:
                has_non_invalid_if_all = True

        return has_non_invalid_if_all
