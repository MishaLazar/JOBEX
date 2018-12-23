from DAL import web_db_handler
import configparser

class WebController:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if WebController.__instance == None:
            WebController()
        return WebController.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if WebController.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            WebController.__instance = self

    def status(self):
        db = web_db_handler.WebDbHandler.getInstance()
        return db.status()


    def get_engagements(self, company_id):
        db = web_db_handler.WebDbHandler.getInstance()
        result = db.get_engagements(company_id)
        return result

    def add_job(self, position, company_id):
        db = web_db_handler.WebDbHandler.getInstance()
        result = db.add_position(position, company_id)
        return result