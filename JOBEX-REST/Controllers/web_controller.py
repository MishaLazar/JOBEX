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

    def add_engagement(self, engagement_obj):
        db = web_db_handler.WebDbHandler.getInstance()
        result = db.add_engagement(engagement_obj)
        return result

    def get_engagements(self, company_name=None, engagement_id=None, **kwargs):
        db = web_db_handler.WebDbHandler.getInstance()
        if kwargs == 'all':
            result = db.get_all_engagements(company_name)
        else:
            result = db.get_engagement(company_name, engagement_id)
        return result

    def add_position(self, position_obj):
        db = web_db_handler.WebDbHandler.getInstance()
        result = db.add_position(position_obj)
        return result

    def get_positions(self, company_name=None, position_id=None, **kwargs):
        db = web_db_handler.WebDbHandler.getInstance()
        if kwargs == 'all':
            result = db.get_all_positions(company_name)
        else:
            result = db.get_position(company_name, position_id)
        return result
