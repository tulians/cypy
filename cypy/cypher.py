# cypy - Vigenere cypher scheme.
# ===================================
import time
import string
import random
from itertools import count, cycle

char_to_int = string.printable[:95]
int_to_char = dict(zip(char_to_int, count()))


def vigenere(key, text, decrypt=False):
    sign = -1 if decrypt else 1
    num_key = [int_to_char[char] for char in key]
    out = (char_to_int[(int_to_char[char] + sign * key_index) %
                       len(char_to_int)]
           for key_index, char in zip(cycle(num_key), text))
    return ''.join(out)


def encode(key, text):
    return vigenere(key, text)


def decode(key, text):
    return vigenere(key, text, True)


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
            time.sleep(next(iterator))
            try:
                task(*arguments)
            except TypeError as exception_detail:
                print("ERROR: There is a mismatch between the number"
                      " of  arguments provided in `arguments` and the ones"
                      " needed by the task function. Detail: " +
                      str(exception_detail))
                break
    else:
        print("ERROR: Make sure to provide a callable task to perform. Param"
              " `task` is not a callable method/function.")


def generate_random_phrase(length, char_set=(string.ascii_letters +
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
