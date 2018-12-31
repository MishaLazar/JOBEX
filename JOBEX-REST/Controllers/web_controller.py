from DAL import mongo_db_handler
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
        db = mongo_db_handler.WebDbHandler.getInstance()
        return db.status()

    def add_engagement(self, engagement_obj):
        db = mongo_db_handler.WebDbHandler.getInstance()
        result = db.add_engagement(engagement_obj)
        return result

    def get_engagements(self, company_name=None, engagement_id=None):
        db = mongo_db_handler.WebDbHandler.getInstance()
        if company_name:
            return db.get_all_engagements(company_name)
        elif company_name and engagement_id:
            return db.get_engagement(company_name, engagement_id)
        else:
            return None

    def add_position(self, position_obj):
        db = mongo_db_handler.WebDbHandler.getInstance()
        result = db.add_position(position_obj)
        return result

    def get_positions(self, company_name=None, position_id=None):
        db = mongo_db_handler.WebDbHandler.getInstance()
        if company_name:
            return db.get_all_positions(company_name)
        elif company_name and position_id:
            return db.get_position(company_name, position_id)
        else:
            return None
