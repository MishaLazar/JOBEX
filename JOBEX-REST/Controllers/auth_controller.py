from DAL.mongo_db_handler import Client
from db_collections import DbCollections
import json
class AuthController:

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AuthController.__instance == None:
            AuthController()
        return AuthController.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if AuthController.__instance != None:
            self.__instance
        else:
            AuthController.__instance = self

    @staticmethod
    def add_token_to_blacklist(jti):
        db_client = Client()
        try:
            db_client.insert_doc_to_collection(DbCollections.get_collection(Key="token_blacklist_collection"),jti)
            return {'message': 'tokens has been revoked'}, 200
        except:
            return {'message': 'Something went wrong'}, 500

    @staticmethod
    def check_token_in_blacklist(jti):
        db_client = Client()
        return bool(db_client.count_docs_in_collection(DbCollections.get_collection(Key="token_blacklist_collection"),jti))

    @staticmethod
    def login(username, password):
        db_client = Client()
        query = {
            "UserName": username,
            "password": password
        }
        print("Getting user doc")
        user_doc = db_client.get_single_doc_from_collection(DbCollections.get_collection("users_collection"), query)
        print("Got user doc, printing:")
        print(user_doc)
        if user_doc:
            user_id = json.loads(user_doc)['_id']
            print(user_id)
            return user_id
        return None
