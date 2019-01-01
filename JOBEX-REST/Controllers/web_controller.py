from DAL.mongo_db_handler import Client

COLLECTION_NAMES = {
    "engagements_collection": "engagements",
    "positions_collection": "positions",
    "users_collection": "users"
}

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
        return db_client.insert_doc_to_collection(COLLECTION_NAMES["engagements_collection"], engagement_obj)

    def get_engagements(self, company_name=None, engagement_id=None):
        db_client = Client()
        if company_name:
            return db_client.get_many_docs_from_collection(COLLECTION_NAMES["engagements_collection"], {"company_name": company_name})
        elif company_name and engagement_id:
            return db_client.get_single_doc_from_collection(COLLECTION_NAMES["engagements_collection"],
                                                            {"_id": engagement_id, "company_name": company_name})
        else:
            return None

    def add_position(self, position_obj):
        db_client = Client()
        return db_client.insert_doc_to_collection(COLLECTION_NAMES["positions_collection"], position_obj)

    def get_positions(self, company_name=None, position_id=None):
        db_client = Client()
        if company_name:
            return db_client.get_many_docs_from_collection(COLLECTION_NAMES["positions_collection"], {"company_name": company_name})
        elif company_name and position_id:
            return db_client.get_single_doc_from_collection(COLLECTION_NAMES["positions_collection"],
                                                            {"company_name": company_name, "_id": position_id})
        else:
            return None

    def get_user(self, user_id):
        db_client = Client()
        return db_client.get_single_doc_from_collection(COLLECTION_NAMES["users_collection"], {"_id": user_id})

    def add_user(self, user_obj):
        db_client = Client()
        return db_client.insert_doc_to_collection(COLLECTION_NAMES["users_collection"], user_obj)

