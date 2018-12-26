from requests import post, RequestException
from config_helper import ConfigHelper
from flask import jsonify

config = ConfigHelper('jobex-web-app/Configurations.ini')
rest_host = config.readRestParams('REST_HOST')


class JobexWebHelper:
    def __init__(self, host):
        self.host = host

    def login(self, login_obj):
        url = "http://{}/login".format(rest_host)
        login_json = login_obj.to_json_str()
        try:
            response = post(url, json=login_json)
            response_json = jsonify(response)
            return response_json
        except (RequestException, OSError) as err:
            message = "Failed to login. Error '{}'".format(err)
            raise IOError(message)

    def logout(self, logout_obj):
        url = "http://{}/logout".format(rest_host)
        logout_json = logout_obj.to_json_str()
        try:
            response = post(url, json=logout_json)
            response_json = jsonify(response)
            return response_json
        except (RequestException, OSError) as err:
            message = "Failed to logout. Error '{}'".format(err)
            raise IOError(message)

    def create_user(self, user_obj):
        url = "http://{}/user".format(rest_host)
        user_json = user_obj.to_json_str()
        try:
            response = post(url, json=user_json)
            response_json = jsonify(response)
            return response_json
        except (RequestException, OSError) as err:
            message = "Failed to create user. Error '{}'".format(err)
            raise IOError(message)
