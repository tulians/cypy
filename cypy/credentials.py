# cypy - Creadentials definition.
# ===================================
import cypher as cy


class Credentials(object):
    """User information of assumed competence."""
    def __init__(self, username, password, keyword_length=10):
        self.keyword = cy.generate_random_string(keyword_length)
        self.username = cy.encode(self.keyword, username)
        self.password = cy.encode(self.keyword, password)
