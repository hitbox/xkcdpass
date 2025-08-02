from abc import ABC
from abc import abstractmethod

class Validate(ABC):

    @abstractmethod
    def __call__(self, string):
        pass


class Contains(Validate):

    def __init__(self, substrings):
        self.substrings = substrings

    def __call__(self, string):
        for substring in self.substrings:
            if substring in string:
                break
        else:
            raise ValidateError(f'{string} does not contain any of {self.substrings}')


class Excludes(Validate):

    def __init__(self, substrings):
        self.substrings = substrings

    def __call__(self, string):
        for substring in self.substrings:
            if substring in string:
                raise ValidateError(f'{string} contains excluded {substring}')


class StartsWith(Validate):

    def __init__(self, substring):
        self.substring = substring

    def __call__(self, string):
        for substring in self.substrings:
            if string.startswith(substring):
                break
        else:
            raise ValidateError(f'{string} does not start with any of {self.substrings}')


class MinimumLength(Validate):

    def __init__(self, length):
        self.length = length

    def __call__(self, string):
        if len(string) < self.length:
            raise ValidateError(f'{string} is less than {self.length}')
