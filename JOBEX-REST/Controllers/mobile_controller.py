from bson import ObjectId
from datetime import datetime
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
        new_user_id = db_client.insert_doc_to_collection(collection_name=DbCollections.get_student_collection(), doc=new_user)
        if new_user_id:
            return new_user_id
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
        doc = {
            "$set": { "student_skill_list" : skills }
        }
        return db_client.update_single_doc_in_collection(DbCollections.get_student_skills_collection(),query,doc,True)

    @staticmethod
    def get_student_profile(student_id):
        db_client = Client()
        return db_client.get_single_doc_from_collection(DbCollections.get_student_collection(), object_id=student_id)

    @staticmethod
    def set_active_status_on_profile(student_id,active_status):
        db_client = Client()
        doc_filter = {
            "_id": ObjectId(student_id),

        }
        doc = {
         "$set": {"active": active_status}
        }
        return db_client.update_single_doc_in_collection(DbCollections.get_student_collection(), filter_json=doc_filter,
                                                         doc_update_json=doc)

    @staticmethod
    def set_student_for_rematch(student_id):
        db_client = Client()
        doc = {
            "job_type_id": 1,
            "source_objectid": student_id,
            "creation_date": datetime.now(),
            "status": 0
        }
        return db_client.insert_doc_to_collection(DbCollections.get_job_collection(),doc)

