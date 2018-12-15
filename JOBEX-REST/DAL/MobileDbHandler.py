from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient, errors
import configparser

class MobileDbHandler:
    # Here will be the instance stored.
    __instance = None
    config = configparser.ConfigParser()
    config.read('../JOBEX-REST/Configurations.ini')
    MONGO_HOST = config['DBPARAMS']['MONGO_HOST']
    MONGO_DB = config['DBPARAMS']['MONGO_DB']
    MONGO_USER = config['DBPARAMS']['MONGO_USER']
    SSH_PKEY_PATH = config['DBPARAMS']['SSH_PKEY_PATH']
    SSH_PKEY_PASS = config['DBPARAMS']['SSH_PKEY_PASS']


    @staticmethod
    def getInstance():
        """ Static access method. """
        if MobileDbHandler.__instance == None:
            MobileDbHandler()
        return MobileDbHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MobileDbHandler.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MobileDbHandler.__instance = self



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
            return 'DB timeout error'
        server.stop()