# cypy - Creadentials definition.
# ===================================
from cypher import encode, generate_random_phrase


class Credentials(object):
    """User information of assumed competence."""
    def __init__(self, username, password, keyword_length=10):
        self.keyword = generate_random_phrase(keyword_length)
        self.username = encode(self.keyword, username)
        self.password = encode(self.keyword, password)
