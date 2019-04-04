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
    def get_full_skillSet():
        db_client = mongo_db_handler.Client()

        return db_client.get_many_docs_from_collection(DbCollections.get_collection(key="skills"))
