from DAL import mobile_db_handler
import json


class MobileController:

    __instance = None

    @staticmethod
    def get_instance():
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

    @staticmethod
    def status():
        db = mobile_db_handler.MobileDbHandler.getInstance()
        return db.status()

    @staticmethod
    def get_student_engagements(student_id):
        db = mobile_db_handler.MobileDbHandler.getInstance()
        result = db.get_student_engagements(student_id)
        return result

    @staticmethod
    def register_user(new_user):
        db = mobile_db_handler.MobileDbHandler.getInstance()
        new_user_id = db.register_student(new_user)
        if new_user_id:
            return json.dumps({"new_user_id": new_user_id})
        return None

    @staticmethod
    def create_obj_with_authentication(object):
        db = mobile_db_handler.MobileDbHandler.getInstance()
        result = db.create_with_authentication(object)
        return result
