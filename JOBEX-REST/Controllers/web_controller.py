from DAL.mongo_db_handler import Client
from DAL.db_collections import DbCollections
from datetime import datetime

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

    def add_engagement(self, engagement_obj):
        db_client = Client()
        return db_client.insert_doc_to_collection(DbCollections.get_collection("engagements"), engagement_obj)

    def get_engagements(self, engagement_id=None):
        db_client = Client()
        if engagement_id:
            return db_client.get_single_doc_from_collection(DbCollections.get_collection("engagements"),
                                                            object_id=engagement_id)
        else:
            return db_client.get_many_docs_from_collection(DbCollections.get_collection("engagements"))

    def add_position(self, position_obj):
        db_client = Client()
        position_id = db_client.insert_doc_to_collection(DbCollections.get_collection("positions"), position_obj)
        now = datetime.now()
        job_obj = {
            "job_type_id": "2",
            "source_objectid": str(position_id),
            "creation_date": str(now),
            "status": "0"
        }
        db_client.insert_doc_to_collection(DbCollections.get_collection("jobs"), job_obj)
        return position_id

    def get_positions(self, position_id=None):
        db_client = Client()
        if position_id:
            return db_client.get_single_doc_from_collection(DbCollections.get_collection("positions"),
                                                            object_id=position_id)
        else:
            return db_client.get_many_docs_from_collection(DbCollections.get_collection("positions"))

    def get_user(self, user_id):
        db_client = Client()
        return db_client.get_single_doc_from_collection(DbCollections.get_collection("users"), object_id=user_id)

    def add_user(self, user_obj):
        db_client = Client()

        return db_client.insert_doc_to_collection(DbCollections.get_collection("users"), user_obj)

    def get_matches(self, position_id=None, student_id=None):
        db_client = Client()
        if position_id:
            return db_client.get_many_docs_from_collection(DbCollections.get_collection("matches"),
                                                           json_query={"position_id": "{}".format(position_id)})
        if student_id:
            return db_client.get_many_docs_from_collection(DbCollections.get_collection("matches"),
                                                           json_query={"student_id": "{}".format(student_id)})
        else:
            return db_client.get_many_docs_from_collection(DbCollections.get_collection("matches"))

    def get_companies_list(self):
        db_client = Client()
        companies_list = []
        companies_dict = db_client.get_many_docs_from_collection(DbCollections.get_collection("companies"))
        for company in companies_dict:
            company_name = company["name"]
            companies_list.append(company_name)
        return companies_list

    def add_company(self, company_name):
        db_client = Client()
        company_obj = {"name": company_name}
        return db_client.insert_doc_to_collection(DbCollections.get_collection("companies"), company_obj)
