import json


class User:

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def to_json_str(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
