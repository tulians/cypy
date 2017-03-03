# cypy - Creadentials definition.
# ===================================
import cypher

"""Credentials only exist in RAM."""

class Credentials(object):
    """User information of assumed competence."""
    def __init__(self, username, password, keyword_length=10, period=1):
        self.keyword = cypher.generate_random_phrase(keyword_length)
        self.th = cypher.IntervalThread(period, cypher.encode, self.keyword, 
                                        username, password)
        self.th.start()

    @property
    def credentials(self):
        """Returns credentials with their current encryption."""
        username = self.th.username
        password = self.th.password
        return username, password

    def stop(self):
        """Stop credentials encryption."""
        return self.th.join()
