# cypy - Creadentials definition.
# ===================================

# Project specific modules
import cypher

NUMERIC = [int, float]


class Credential(object):
    """User information of assumed competence."""
    def __init__(self, username, password, keyword):
        if (type(username) and type(password) and type(keyword)) is str:
                self.keyword = keyword
                self.username = cypher.encode(self.keyword, username)
                self.password = cypher.encode(self.keyword, password)
        else:
            raise ValueError("Check the types of the given parameters.")

    @property
    def credentials(self):
        """Returns credentials with their current encryption."""
        return self.username, self.password

    @property
    def decoded_credentials(self):
        """Returns decoded credentials."""
        return (cypher.decode(self.keyword, self.username),
                cypher.decode(self.keyword, self.password))
