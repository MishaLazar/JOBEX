from DAL.mongo_db_handler import Client
from DAL.db_collections import DbCollections
import json


class MobileController:

    # __instance = None

    # @staticmethod
    # def get_instance():
    #     """ Static access method. """
    #     if MobileController.__instance == None:
    #         MobileController()
    #     return MobileController.__instance

    def __init__(self):
        """ Virtually private constructor. """
        # if MobileController.__instance != None:
        #     raise Exception("This class is a singleton!")
        # else:
        #     MobileController.__instance = self



    @staticmethod
    def register_user(new_user):
        db_client = Client()
        new_user_id = db_client.insert_doc_to_collection(collection_name=DbCollections["users"], doc=new_user)
        if new_user_id:
            return json.dumps({"new_user_id": new_user_id})
        return None

    @staticmethod
    def get_student_engagements(student_id):
        db_client = Client()
        result = db_client.get_single_doc_from_collection(collection_name=DbCollections.get_collection("users"),
                                                          object_id=student_id)
        return result

    @staticmethod
    def get_student_skills(student_id):
        db_client = Client()
        query = {
            "student_id": student_id
        }
        return db_client.get_single_doc_from_collection(DbCollections.get_collection("student_skills"), json_query=query)

    @staticmethod
    def set_student_skills(student_id,skills):
        db_client = Client()
        query = {
            "student_id": student_id
        }
        return db_client.update_single_doc_in_collection(DbCollections.get_student_skills_collection(),query,skills,True)

    @staticmethod
    def get_student_profile(student_id):
        db_client = Client()
        return db_client.get_single_doc_from_collection(DbCollections.get_student_collection(), object_id=student_id)

