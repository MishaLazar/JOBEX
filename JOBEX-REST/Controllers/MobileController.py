from DAL import MobileDbHandler
import configparser

class MobileController:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MobileController.__instance == None:
            MobileController()
        return MobileController.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MobileController.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MobileController.__instance = self

    def status(self):
        db = MobileDbHandler.MobileDbHandler.getInstance()
        return db.status()

    def get_StudentEngagements(self,studentId):
        db = MobileDbHandler.MobileDbHandler.getInstance()
        return db.get_studentengagements(studentId)
