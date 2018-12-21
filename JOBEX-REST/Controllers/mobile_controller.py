from DAL import mobile_db_handler


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

    def status(self):
        db = mobile_db_handler.MobileDbHandler.getInstance()
        return db.status()

    def get_student_engagements(self, student_id):
        db = mobile_db_handler.MobileDbHandler.getInstance()
        result = db.get_student_engagements(student_id)
        return result

    def register_student(self, student):
        db = mobile_db_handler.MobileDbHandler.getInstance()
        result = db.register_student(student)
        return result


