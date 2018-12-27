import json


class Login:

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def to_json_str(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
