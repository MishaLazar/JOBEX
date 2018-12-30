import jwt
from Utils.config_helper import ConfigHelper
import datetime
import json
from DAL import mobile_db_handler


class AuthController:

    config = ConfigHelper.get_instance()
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
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=360),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                config_helper.ConfigHelper.get_instance().read_auth("SECRET_KEY"),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, config_helper.ConfigHelper.get_instance().read_auth("SECRET_KEY"))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def login(self, username,password):
        db = mobile_db_handler.MobileDbHandler().getInstance()
        user_id = db.login(username=username, password=password)
        result = {"token": self.encode_auth_token(user_id).decode('utf8').replace("'", '"')}
        json_result = json.dumps(result)
        return json_result
