from Classes import Student
from Classes import Position
import sys
import json
class Engagement:

    def __init__(self, name=None):
        self.name = name

    def set_name(self,firstName):
        self.firstName = firstName

    def to_json_str(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
