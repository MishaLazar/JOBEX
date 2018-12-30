from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient, errors
from Utils.config_helper import ConfigHelper
from Classes import engagement


class WebDbHandler:
    # Here will be the instance stored.
    config = ConfigHelper('../JOBEX-REST/Configurations.ini')
    #    config.read('../JOBEX-REST/Configurations.ini')
    MONGO_HOST = config.read_db_params('MONGO_HOST')
    # config['DBPARAMS']['MONGO_HOST']
    MONGO_DB = config.read_db_params('MONGO_DB')
    # config['DBPARAMS']['MONGO_DB']
    MONGO_USER = config.read_db_params('MONGO_USER')
    # config['DBPARAMS']['MONGO_USER']
    SSH_PKEY_PATH = config.read_db_params('SSH_PKEY_PATH')
    # config['DBPARAMS']['SSH_PKEY_PATH']
    SSH_PKEY_PASS = config.read_db_params('SSH_PKEY_PASS')
    # config['DBPARAMS']['SSH_PKEY_PASS']

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if WebDbHandler.__instance == None:
            WebDbHandler()
        return WebDbHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if WebDbHandler.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            WebDbHandler.__instance = self

    def status(self):
        server = SSHTunnelForwarder(
            self.MONGO_HOST,
            ssh_username=self.MONGO_USER,
            ssh_pkey=self.SSH_PKEY_PATH,
            ssh_private_key_password=self.SSH_PKEY_PASS,
            remote_bind_address=('127.0.0.1', 27017))
        server.start()
        try:
            client = MongoClient('127.0.0.1', server.local_bind_port)  # server.local_bind_port is assigned local port
            db = client[self.MONGO_DB]
            return db.collection_names()[0]
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error, {}'.format(err)
        finally:
            server.stop()

    def add_position(self, position_obj):
        # todo this db handle
        pass

    def get_position(self, company_name, position_id):
        # todo this db handle
        pass

    def get_all_positions(self, company_name):
        # todo this db handle
        pass

    def add_engagement(self, engagement_obj):
        # todo this db handle
        pass

    def get_engagement(self, company_name, engagement_id):
        # todo this db handle
        pass

    def get_all_engagements(self, company_name):
        # todo this section as def - from here
        server = SSHTunnelForwarder(
            self.MONGO_HOST,
            ssh_username=self.MONGO_USER,
            ssh_pkey=self.SSH_PKEY_PATH,
            ssh_private_key_password=self.SSH_PKEY_PASS,
            remote_bind_address=('127.0.0.1', 27017))
        server.start()
        try:
            client = MongoClient('127.0.0.1', server.local_bind_port)  # server.local_bind_port is assigned local port
            db = client[self.MONGO_DB]
            # todo until here
            collection = db["Engagements"]

            pieline = [{
                        "$match": {
                            "$expr": "ObjectId(company_name)"
                        }
                    },{
                        "$sort": {
                            "_id": -1
                        }
                    },{
                        "$limit": 100
                    }]

            cursor = collection.aggregate(pieline)
            try:
                for doc in cursor:
                    curr_engagement = engagement.Engagement()
                    # curr_engagement.setFirstName(doc['FirstName'])
                    # curr_engagement.setEngagementId(str(doc['_id']))

                    return curr_engagement.to_json_str()
            finally:
                cursor.close()
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error'
        server.stop()
