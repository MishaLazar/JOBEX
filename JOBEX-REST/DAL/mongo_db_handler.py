from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient, errors, DESCENDING, ASCENDING
from Utils.config_helper import ConfigHelper
from bson.objectid import ObjectId

class Client:

    def __init__(self):
        config = ConfigHelper('../JOBEX-REST/Configurations.ini')
        self.mongo_host = config.read_db_params('MONGO_HOST')
        self.mongo_db = config.read_db_params('MONGO_DB')
        self.mongo_user = config.read_db_params('MONGO_USER')
        self.ssh_key_path = config.read_db_params('SSH_PKEY_PATH')
        self.ssh_pkey_pass = config.read_db_params('SSH_PKEY_PASS')
        self.server = SSHTunnelForwarder(  # used for remote testing, will be removed when deployed on server
            ssh_address_or_host=self.mongo_host,
            ssh_username=self.mongo_user,
            ssh_pkey=self.ssh_key_path,
            ssh_private_key_password=self.ssh_pkey_pass,
            remote_bind_address=('127.0.0.1', 27017))
        self.server.start()
        self.client = MongoClient('127.0.0.1', self.server.local_bind_port)  # server.local_bind_port is assigned local port
        self.db = self.client[self.mongo_db]

    def find_by_collection(self, collection_name):
        """Insert doc to collection

            :param collection_name: The name of the collection to get from
            :type collection_name: str
            :returns list of docs
            :rtype list of JSON objects
        """
        result = []
        try:
            collection = self.db[collection_name]
            cursor = collection.find()
            try:
                for doc in cursor:
                    doc['_id'] = str(doc['_id'])
                    result.append(doc)
            finally:
                cursor.close()
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            return result

    def insert_doc_to_collection(self, collection_name, doc):
        """Insert doc to collection

                :param collection_name: The name of the collection to insert in
                :type collection_name: str
                :param doc: the JSON object to insert in the collection
                :type doc: json str
                :returns inserted_id of the inserted doc
                :rtype str
        """
        result = None
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(doc).inserted_id
            result['_id'] = str(result['_id'])
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            return result

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
        result = None
        try:
            collection = self.db[collection_name]
            if json_query:
                result = collection.find_one(json_query)
                result['_id'] = str(result['_id'])
            elif object_id:
                result = collection.find_one({"_id": ObjectId(object_id)})
                result['_id'] = str(result['_id'])
            else:
                result = collection.find_one()
                result['_id'] = str(result['_id'])
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            return result

    def insert_many_docs_to_collection(self, collection_name, docs_list):
        """Insert many docs to collection

                :param collection_name: The name of the collection to insert in
                :type collection_name: str
                :param docs_list: the JSON objects to insert in the collection
                :type docs_list: list of JSONs
                :returns inserted_ids of the docs inserted
                :rtype list of objectID objects
        """
        result = None
        try:
            collection = self.db[collection_name]
            result = collection.insert_many(docs_list).inserted_ids
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            return result

    def get_many_docs_from_collection(self, collection_name,
                                      json_query=None,
                                      sort_order_parameter=None,
                                      direction=None,
                                      limit=None):
        """ Getting many docs from collection by collection name

                :param collection_name: The name of the collection to insert in
                :type collection_name: str
                :param sort_order_parameter: field to sort by
                :type sort_order_parameter: str
                :param direction: True = Desc else Asc
                :type direction: boolean
                :param limit: max number of doc to find
                :type limit: int
                :param json_query: the json query to search with
                :type json_query dict
                :returns many docs
                :rtype JSON objects of the docs found in the collection
        """
        result = []
        if direction:
            direction = DESCENDING
        else:
            direction = ASCENDING
        try:
            collection = self.db[collection_name]
            if json_query:
                if sort_order_parameter:
                    for doc in collection.find(json_query).sort(sort_order_parameter, direction).limit(limit):
                        doc['_id'] = str(doc['_id'])
                        result.append(doc)
                else:
                    for doc in collection.find(json_query):
                        doc['_id'] = str(doc['_id'])
                        result.append(doc)
            else:
                for doc in collection.find():
                    doc['_id'] = str(doc['_id'])
                    result.append(doc)
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            return result

    def count_docs_in_collection(self, collection_name, json_query=None):
        """ Getting many docs from collection by collection name

                :param collection_name: The name of the collection to count in
                :type collection_name: str
                :param json_query: the json query to search with
                :type json_query: str
                :returns number of docs in the collection
                :rtype int
        """
        result = None
        try:
            collection = self.db[collection_name]
            if json_query:
                result = collection.count_documents(json_query)
            else:
                result = collection.count_documents({})
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            return result

    def update_single_doc_in_collection(self, collection_name, filter_json, doc_update_json, update_if_exists=False):
        """ Update doc in collection

                :param collection_name: The name of the collection to update in
                :type collection_name: str
                :param filter_json: filter of which doc to update, best to use _id
                :type filter_json: json str
                :param doc_update_json: the values to update in the doc ,
                :type doc_update_json: json str
                :param update_if_exists: if not exists insert else update
                :type update_if_exists: json str
                :returns modified_count, should be 1 as single doc should be updated
                :rtype int
        """
        result = None
        try:
            collection = self.db[collection_name]
            result = collection.update_one(filter=filter_json, update=doc_update_json,
                                           upsert=update_if_exists).modified_count

        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            return result

    def get_aggregate_document(self, collection_name, pipeline):
        """ Update doc in collection

                :param collection_name: The name of the collection to update in
                :type collection_name: str
                :param filter_json: filter of which doc to update, best to use _id
                :type filter_json: json str
                :param doc_update_json: the values to update in the doc ,
                       update_if_exists: if not exists insert else update
                :type doc_update_json: json str
                :returns modified_count, should be 1 as single doc should be updated
                :rtype int
        """
        result = None
        try:
            collection = self.db[collection_name]
            cursor = collection.aggregate(pipeline=pipeline)
            result = list(cursor)
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error: {}'.format(err)
        finally:
            return result