from requests import post, put, get, delete, RequestException
from config_helper import ConfigHelper
from flask import jsonify

config = ConfigHelper(r'C:\JOBEX\jobex-web-app\Configurations.ini')
rest_host = config.readRestParams('REST_HOST')


class JobexWebHelper:
    """this class is used to handle API calls to the REST server"""
    def __init__(self, host):
        self.host = host

    def login(self, login_obj):
        return self.api_call(api_path="login", obj=login_obj, method='POST')

    def logout(self, logout_obj):
        return self.api_call(api_path="logout", obj=logout_obj, method='POST')

    def create_user(self, user_obj):
        return self.api_call(api_path="users", obj=user_obj, method='POST')

    def edit_user(self, user_obj, user_id):
        return self.api_call(api_path="users/{}".format(user_id), obj=user_obj, method='PUT')

    def delete_user(self, user_obj, user_id):
        return self.api_call(api_path="users/{}".format(user_id), obj=user_obj, method='DELETE')

    def create_position(self, position_obj):
        return self.api_call(api_path="positions", obj=position_obj, method='POST')

    def edit_position(self, user_obj, position_id):
        return self.api_call(api_path="positions/{}".format(position_id), obj=user_obj, method='PUT')

    def delete_position(self, user_obj, position_id):
        return self.api_call(api_path="positions/{}".format(position_id), obj=user_obj, method='DELETE')

    def create_engagement(self, engagement_obj):
        return self.api_call(api_path="engagements", obj=engagement_obj, method='POST')

    def edit_engagement(self, engagement_obj, engagement_id):
        return self.api_call(api_path="engagements/{}".format(engagement_id), obj=engagement_obj, method='PUT')

    def delete_engagement(self, position_obj, engagement_id):
        return self.api_call(api_path="engagements/{}".format(engagement_id), obj=position_obj, method='DELETE')

    def get_all_positions(self):
        return self.api_call(api_path="positions", method='GET')

    def get_engagements(self):
        return self.api_call(api_path="engagements", method='GET')

    def api_call(self, api_path=None, obj=None, method='GET'):
        url = "http://{}/{}".format(rest_host, api_path)
        json_str = obj.to_json_str()
        try:
            if method == 'POST':
                response = post(url, json=json_str)
            elif method == 'PUT':
                response = put(url, json=json_str)
            elif method == 'GET':
                response = get(url)
            elif method == 'DELETE':
                response = delete(url)
            else:
                response = get(url)
            response_json = jsonify(response)
            return response_json
        except RequestException as err:
            message = "API call failed for {}. Error '{}'".format(url, err)
            raise IOError(message)
