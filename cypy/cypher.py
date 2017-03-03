# cypy - Vigenere cypher scheme.
# ===================================
import time
import string
import random
from threading import Thread, Event
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


class TaskThread(Thread):
    def __init__(self, task, key, username, password):
        Thread.__init__(self)
        self.task = encode if task == "encode" else decode
        self.key = key
        self.username = username
        self.password = password
        self.stopped = Event()
        self.return_value = None

    def run(self):
        self.return_value = (self.task(self.key, self.username),
                             self.task(self.key, self.password))
        return self.return_value

    def join(self):
        if self.is_alive():
            self.stopped.set()
            Thread.join(self)
        return self.username, self.password


class IntervalThread(TaskThread):
    def __init__(self, period, task, key, username, password):
        super().__init__(task, key, username, password)
        self.period = period

    def run(self):
        self.username, self.password = super().run()
        while not self.stopped.is_set():
            time.sleep(self.period)
            self.username, self.password = super().run()


def generate_random_phrase(length, char_set=(string.ascii_letters +
                                             string.digits +
                                             string.punctuation)):
    if type(char_set) is str:
        try:
            return "".join(random.choice(char_set) for _ in xrange(length))
        except NameError:
            return "".join(random.choice(char_set) for _ in range(length))
    else:
        raise NameError("Make sure to provide a character set consisting of"
                        " a string of chars. type(char_set) != str.")
