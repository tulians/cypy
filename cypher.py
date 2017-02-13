# cypy - Vigenere cypher scheme.
# ===================================
import base64


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
