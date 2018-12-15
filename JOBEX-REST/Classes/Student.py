from Classes import Skill
import sys
import json
class Student:

    skills = list()

    def __init__(self,FirstName=None,LastName=None,StudentId=None,Email=None):
        self.firstName = FirstName
        self.lastName  = LastName
        self.studentId = StudentId
        self.email = Email

    def addSkill(self,skill:Skill):
        try:
            self.skills.append(Skill)
        except:
            return sys.exc_info()[0]

    def getSkills(self):
        return  self.skills

    def setFirstName(self,firstName):
        self.firstName = firstName
    def setLastName(self,lastName):
        self.lastName = lastName
    def setStudentId(self,studentId):
        self.studentId = studentId
    def setEmail(self,email):
        self.email = email

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
