# cypy - Creadentials definition.
# ===================================

# Project specific modules
import cypher

NUMERIC = [int, float]


class Credential(object):
    """User information of assumed competence."""
    def __init__(self, username, password, keyword=None,
                 cyclic=False, period=1, keyword_length=10):
        if ((type(username) and type(password) is str) and
           (type(keyword_length) is int) and (type(period) in NUMERIC)):
            self.cyclic = cyclic
            if self.cyclic and not keyword:
                self.keyword = cypher.generate_random_phrase(keyword_length)
                self.th = cypher.IntervalThread(period, cypher.encode,
                                                self.keyword, username,
                                                password)
                self._start_cyclic_encryption()
            elif keyword:
                self.keyword = keyword
                self.username = cypher.encode(self.keyword, username)
                self.password = cypher.encode(self.keyword, password)
            else:
                raise ValueError("Incorrect set of parameters given.")
        else:
            raise ValueError("Check the types of the given parameters.")

    @property
    def credentials(self):
        """Returns credentials with their current encryption."""
        if self.cyclic:
            return self.th.username, self.th.password
        return self.username, self.password

    @property
    def decoded_credentials(self):
        """Returns decoded credentials."""
        return (cypher.decode(self.keyword, self.username),
                cypher.decode(self.keyword, self.password))

    def _start_cyclic_encryption(self):
        """Start cyclic credentials encryption."""
        self.th.start()

    def _stop_cyclic_encryption(self):
        """Stop credentials encryption."""
        return self.th.join()
