# cypy - Vigenere cypher scheme.
# ===================================

# Built-in modules
import string
from itertools import count, cycle

char_to_int = string.printable[:95]
int_to_char = dict(zip(char_to_int, count()))


def vigenere(key, text, decrypt=False):
    if not (key and text):
        raise ValueError("No valid key and/or text values.")
    sign = -1 if decrypt else 1
    num_key = [int_to_char[char] for char in key]
    out = (char_to_int[(int_to_char[char] + sign * key_index) %
                       len(char_to_int)]
           for key_index, char in zip(cycle(num_key), text))
    return "".join(out)


def encode(key, text):
    return vigenere(key, text)


def decode(key, text):
    return vigenere(key, text, True)
