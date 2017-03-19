# cypy - User data management.
# ===================================

# Built-in modules
import os
import json


class Data(object):
    """Manages credentials file."""
    def __init__(self, path=None):
        if not path:
            self.path = os.getcwd() + "/.credentials.json"
        else:
            # Avoid name errors.
            self.path = (path + "/.credentials.json" if path[-1] != "/" else
                         path + ".credentials.json")
        if not os.path.isfile(self.path):
            self.credentials = {}
            with open(self.path, "w") as f:
                f.write(json.dumps(self.credentials))
        else:
            with open(self.path, "r") as f:
                self.credentials = json.loads(f.read())

    def add_credential(self, username, password):
        """Credentials entered here should be encrypted."""
        with open(self.path, "w") as f:
            self.credentials[username] = password
            f.write(json.dumps(self.credentials))

    def get_credential(self, username):
        """Returns password associated to a given username."""
        return self.credentials[username]

    def delete_credential(self, username):
        """Removes a credential given one of its parts."""
        del self.credentials[username]
        with open(self.path, "w") as f:
            f.write(json.dumps(self.credentials))
