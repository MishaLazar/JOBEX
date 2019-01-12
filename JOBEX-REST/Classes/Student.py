from Classes import Skill
import sys
import json


class Student:

    skills = list()

    def __init__(self,first_name=None,last_name=None,student_id=None,email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
        self.email = email

    def add_skill(self,skill:Skill):
        try:
            self.skills.append(skill)
        except:
            return sys.exc_info()[0]

    def get_skills(self):
        return self.skills

    def set_first_name(self,first_name):
        self.first_name = first_name

    def set_last_name(self,last_name):
        self.last_name = last_name

    def set_student_id(self,student_id):
        self.student_id = student_id

    def set_email(self,email):
        self.email = email

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
