from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient, errors
from Utils.config_helper import ConfigHelper
from Classes import Student
from bson import ObjectId

class MobileDbHandler:
    # Here will be the instance stored.

    config = ConfigHelper('../JOBEX-REST/Configurations.ini')
    MONGO_HOST = config.readDbParams('MONGO_HOST')
    MONGO_DB = config.readDbParams('MONGO_DB')
    MONGO_USER = config.readDbParams('MONGO_USER')
    SSH_PKEY_PATH = config.readDbParams('SSH_PKEY_PATH')
    SSH_PKEY_PASS = config.readDbParams('SSH_PKEY_PASS')

    __instance = None

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

    def register_student(self, student):
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
            collection = db["Users"]

            _id = collection.insert_one(student)

            return _id.inserted_id

        except errors as err:
            return err
        server.stop()

    def get_student_engagements(self, student_id):
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
            collection = db["Student"]

            pieline = [{
                        "$match": {
                            "$expr": "ObjectId(studentId)"
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
                    student = Student.Student()
                    student.setFirstName(doc['FirstName'])
                    student.setLastName(doc['LastName'])
                    student.setEmail(doc['Email'])
                    student.setStudentId(str(doc['_id']))

                    return student.toJSON()
            finally:
                cursor.close()
        except errors.ServerSelectionTimeoutError as err:
            return 'DB timeout error'
        server.stop()