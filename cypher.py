# cypy - Vigenere cypher scheme.
# ===================================
import sys
import time
import string
import base64
import random
import inspect


def encode(keyword, string, iterations=1):
    encoded_string = _encode(keyword, string)
    for _ in range(iterations - 1):
        encoded_string = _encode(keyword, encoded_string)
    return encoded_string


def decode(keyword, string, iterations=1):
    decoded_string = _decode(keyword, string)
    for _ in range(iterations - 1):
        decoded_string = _decode(keyword, decoded_string)
    return decoded_string


def _encode(keyword, string):
    encoded_characters = []
    for i in range(len(string)):
        key_character = keyword[i % len(keyword)]
        encoded_character = chr(ord(string[i]) + ord(key_character) % 256)
        encoded_characters.append(encoded_character)
    encoded_string = "".join(encoded_characters)
    return base64.urlsafe_b64encode(encoded_string)


def _decode(keyword, string):
    decoded_characters = []
    string = base64.urlsafe_b64decode(string)
    for i in range(len(string)):
        key_character = keyword[i % len(keyword)]
        decoded_character = chr(abs(ord(string[i]) - ord(key_character) % 256))
        decoded_characters.append(decoded_character)
    decoded_string = "".join(decoded_characters)
    return decoded_string


def repeat_task_periodically(period, task, *arguments):
    if callable(task):
        def _tick():
            time_base = time.time()
            # As the time_base variable will hold still a moment in time,
            # the offset will be used to generate multiples of the period,
            # which can then be compared with the current time in the yield
            # statement.
            offset = 0
            while True:
                offset += 1
                yield max(time_base + offset * period - time.time(), 0)
        iterator = _tick()
        while True:
            # Python 3 compatibility.
            try:
                time.sleep(iterator.next())
                if len(arguments) >= len(inspect.getargspec(task).args):
                    task(*arguments)
            except AttributeError:
                time.sleep(next(iterator))
                if len(arguments) >= len(inspect.getfullargspec(task).args):
                    task(*arguments)
    else:
        print("ERROR: Make sure to provide a callable task to perform. Param"
              " `task` is not a callable method/function.")


def generate_random_string(length, char_set=(string.ascii_letters +
                                             string.digits +
                                             string.punctuation)):
    if type(char_set) is str:
        # Python 3 compatibility.
        try:
            return "".join(random.choice(char_set) for _ in xrange(length))
        except NameError:
            return "".join(random.choice(char_set) for _ in range(length))
    else:
        print("ERROR: Make sure to provide a character set consisting on a"
              " string of chars. Param `char_set` is not of type str.")
