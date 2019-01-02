from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient, errors
from Utils.config_helper import ConfigHelper


class Client:

    def __init__(self):
        config = ConfigHelper('../JOBEX-REST/Configurations.ini')
        self.mongo_host = config.read_db_params('MONGO_HOST')
        self.mongo_db = config.read_db_params('MONGO_DB')
        self.mongo_user = config.read_db_params('MONGO_USER')
        self.ssh_key_path = config.read_db_params('SSH_PKEY_PATH')
        self.ssh_pkey_pass = config.read_db_params('SSH_PKEY_PASS')
        self.server = SSHTunnelForwarder( # used for remote testing, will be removed when deployed on server
            ssh_address_or_host=self.mongo_host,
            ssh_username=self.mongo_user,
            ssh_pkey=self.ssh_key_path,
            ssh_private_key_password=self.ssh_pkey_pass,
            remote_bind_address=('127.0.0.1', 27017))
        self.client = MongoClient('127.0.0.1', self.server.local_bind_port)  # server.local_bind_port is assigned local port
        self.db = self.client[self.mongo_db]

    def find_by_collection(self, collection_name, limit=100):
        """Insert doc to collection

            :param collection_name: The name of the collection to insert in
            :type collection_name: str
            :param limit: (optional) how many docs will be returned
            :type limit: int
            :returns cursor docs
            :rtype JSON objects
        """
        try:
            collection = self.db[collection_name]
            sort = [("_id", -1)]
            cursor = collection.find(sort=sort, limit=limit)
            try:
                for doc in cursor:
                    return doc
            finally:
                cursor.close()
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            self.server.stop()

    def insert_doc_to_collection(self, collection_name, doc):
        """Insert doc to collection

                :param collection_name: The name of the collection to insert in
                :type collection_name: str
                :param doc: the JSON object to insert in the collection
                :type doc: json str
                :returns inserted_id of the inserted doc
                :rtype str
        """
        try:
            collection = self.db[collection_name]
            return collection.insert_one(doc).inserted_id
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            self.server.stop()

    def get_single_doc_from_collection(self, collection_name, json_query=None, object_id=None):
        """Getting a single doc from collection by JSON query / objectID
             default is first doc in the collection

                :param collection_name: The name of the collection to insert in
                :type collection_name: str
                :param json_query: (optional) the JSON object query, can be used to find specific docs
                :type json_query: json str
                :param object_id: (optional) getting doc by objectID
                :type object_id: str
                :returns single doc
                :rtype JSON object of the doc
        """
        try:
            collection = self.db[collection_name]
            if json_query:
                return collection.find_one(json_query)
            elif object_id:
                return collection.find_one({"_id": object_id})
            return collection.find_one()
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            self.server.stop()

    def insert_many_docs_to_collection(self, collection_name, docs_list):
        """Insert many docs to collection

                :param collection_name: The name of the collection to insert in
                :type collection_name: str
                :param docs_list: the JSON objects to insert in the collection
                :type docs_list: list of JSONs
                :returns inserted_ids of the docs inserted
                :rtype list of objectID objects
        """
        try:
            collection = self.db[collection_name]
            return collection.insert_many(docs_list).inserted_ids
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            self.server.stop()

    def get_many_docs_from_collection(self, collection_name, json_query=None):
        """ Getting many docs from collection by collection name

                :param collection_name: The name of the collection to insert in
                :type collection_name: str
                :param json_query: the json query to search with
                :type JSON str
                :returns many docs
                :rtype JSON objects of the docs found in the collection
        """
        try:
            collection = self.db[collection_name]
            if json_query:
                for doc in collection.find(json_query):
                    return doc
            else:
                for doc in collection.find():
                    return doc
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            self.server.stop()

    def count_docs_in_collection(self, collection_name, json_query=None):
        """ Getting many docs from collection by collection name

                :param collection_name: The name of the collection to count in
                :type collection_name: str
                :param json_query: the json query to search with
                :type JSON str
                :returns number of docs in the collection
                :rtype int
        """
        try:
            collection = self.db[collection_name]
            if json_query:
                return collection.count_documents(json_query)
            return collection.count_documents({})
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            self.server.stop()

    def update_single_doc_in_collection(self, collection_name, filter_json, doc_update_json):
        """ Update doc in collection

                :param collection_name: The name of the collection to update in
                :type collection_name: str
                :param filter_json: filter of which doc to update, best to use _id
                :type filter_json: json str
                :param doc_update_json: the values to update in the doc
                :type doc_update_json: json str
                :returns modified_count, should be 1 as single doc should be updated
                :rtype int
        """
        try:
            collection = self.db[collection_name]
            return collection.update_one(filter=filter_json, update=doc_update_json).modified_count
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            self.server.stop()
