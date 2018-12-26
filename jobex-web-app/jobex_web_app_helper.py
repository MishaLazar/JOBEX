from requests import post, RequestException
from config_helper import ConfigHelper
from flask import jsonify

config = ConfigHelper('jobex-web-app/Configurations.ini')
rest_host = config.readRestParams('REST_HOST')


class JobexWebHelper:
    def __init__(self, host):
        self.host = host

    def create_user(self, user_obj):
        url = "http://{}/user".format(rest_host)
        user_json = user_obj.to_json_str()
        try:
            response = post(url, json=user_json)
            response_json = jsonify(response)
            return response_json.content
        except (RequestException, OSError) as err:
            message = "Failed to create user. Error '{}'".format(err)
            raise IOError(message)
