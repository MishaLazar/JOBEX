from requests import post, put, get, delete, RequestException
from config_helper import ConfigHelper
import json

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
        return self.api_call(api_path="register", obj=user_obj, method='POST')

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

    def get_all_positions(self, company_name, access_token):
        return self.api_call(api_path="positions/{}".format(company_name), method='GET', access_token=access_token)

    def get_position(self, company_name, position_id):
        return self.api_call(api_path="positions/{}/{}".format(company_name, position_id), method='GET')

    def get_engagement(self, company_name, engagement_id):
        return self.api_call(api_path="engagements/{}/{}".format(company_name, engagement_id), method='GET')

    def get_all_engagements(self, company_name):
        return self.api_call(api_path="engagements/{}".format(company_name), method='GET')

    def get_user(self, user_id):
        return self.api_call(api_path="users/{}".format(user_id), method='GET')

    @staticmethod
    def api_call(api_path=None, obj=None, method='GET', access_token=None, refresh_token=None):
        url = "http://{}/{}".format(rest_host, api_path)
        headers = None
        if access_token:
            headers = {'content-type': 'application/json', 'Access-Control-Allow-Origin': '*',
                       'Authorization': "Bearer " + access_token}
        try:
            if method == 'POST':
                if headers:
                    response = post(url, json=obj, headers=headers)
                else:
                    response = post(url, json=obj)
            elif method == 'PUT':
                response = put(url, json=obj)
            elif method == 'GET':
                response = get(url)
            elif method == 'DELETE':
                response = delete(url)
            else:
                response = get(url)
            status_code = response.status_code
            if status_code == 200:
                return response
            elif status_code == 500 or 401 or 404:
                reason = response.reason
                message = "API call failed for {}. Reason '{}'".format(url, reason)
                raise IOError(message)
        except RequestException as err:
            message = "API call failed for {}. Error '{}'".format(url, err)
            raise IOError(message)
