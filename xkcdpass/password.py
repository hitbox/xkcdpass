import random

from string import digits

def capitalize_random(words):
    index = random.choice(range(len(words)))
    words[index] = words[index].capitalize()

def random_append_digit(words):
    index = random.choice(range(len(words)))
    digit = random.choice(digits)
    words[index] = words[index] + digit

def create_password(words, nwords, separators, minimum_length):
    while True:
        word_list = random.sample(words, nwords)
        capitalize_random(word_list)
        random_append_digit(word_list)
        separator = random.choice(separators)
        password = separator.join(word_list)
        if len(password) >= minimum_length:
            return password
