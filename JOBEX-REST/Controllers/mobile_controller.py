from DAL import mongo_db_handler
from db_collections import DbCollections
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
    def get_student_engagements(student_id):
        db_client = mongo_db_handler.Client()
        result = db_client.get_single_doc_from_collection(collection_name=DbCollections.get_collection("users"),
                                                          object_id=student_id)
        return result

    @staticmethod
    def register_user(new_user):
        db_client = mongo_db_handler.Client()
        new_user_id = db_client.insert_doc_to_collection(DbCollections["users"], doc=new_user)
        if new_user_id:
            return json.dumps({"new_user_id": new_user_id})
        return None


