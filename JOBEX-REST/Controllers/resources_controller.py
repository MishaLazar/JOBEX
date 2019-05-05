from DAL import mongo_db_handler
from DAL.db_collections import DbCollections


class ResourcesController:

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """

        if ResourcesController.__instance == None:

            ResourcesController()
        return ResourcesController.__instance

    def __init__(self):
        """ Virtually private constructor. """

        if ResourcesController.__instance != None:

            self.__instance
        else:
            ResourcesController.__instance = self

    @staticmethod
    def get_all_skills():
        db_client = mongo_db_handler.Client()
        return db_client.find_by_collection(DbCollections.get_collection(key="skills"))

    @staticmethod
    def search_skills(skill_to_find):
        db_client = mongo_db_handler.Client()
        return db_client.get_many_docs_from_collection(DbCollections.get_collection(key="skills"),
                                                       json_query={"skill_name": "{}".format(skill_to_find)})

    @staticmethod
    def add_skill(skill_obj):
        db_client = mongo_db_handler.Client()
        return db_client.insert_doc_to_collection(DbCollections.get_collection(key="skills"), doc=skill_obj)

    @staticmethod
    def get_all_cities():
        db_client = mongo_db_handler.Client()
        return db_client.find_by_collection(DbCollections.get_collection(key="cities"))
