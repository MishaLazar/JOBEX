from requests import post, put, get, delete, RequestException
# from Utils.config_helper import ConfigHelper

# config = ConfigHelper(r'C:\JOBEX\JOBEX-REST\Configurations.ini')
rest_host = '127.0.0.1:5050'


class JobexWebHelper:
    """this class is used to handle API calls to the REST server"""

    def __init__(self, host):
        self.host = host

    def get_login(self, login_obj):
        return self.api_call(api_path="get_login", obj=login_obj, method='POST')

    def create_user(self, user_obj):
        return self.api_call(api_path="register", obj=user_obj, method='POST')

    # protected API calls ----------------------------------------------------------------------------------------------
    def logout(self, logout_obj, access_token):
        return self.api_call(api_path="logout", obj=logout_obj, method='POST', access_token=access_token)

    def edit_user(self, user_obj, user_id, access_token):
        return self.api_call(api_path="users/{}".format(user_id), obj=user_obj, method='PUT', access_token=access_token)

    def delete_user(self, user_obj, user_id, access_token):
        return self.api_call(api_path="users/{}".format(user_id), obj=user_obj, method='DELETE',
                             access_token=access_token)

    def create_position(self, position_obj, access_token):
        return self.api_call(api_path="positions", obj=position_obj, method='POST', access_token=access_token)

    def edit_position(self, user_obj, position_id, access_token):
        return self.api_call(api_path="positions/{}".format(position_id), obj=user_obj, method='PUT',
                             access_token=access_token)

    def delete_position(self, user_obj, position_id, access_token):
        return self.api_call(api_path="positions/{}".format(position_id), obj=user_obj, method='DELETE',
                             access_token=access_token)

    def create_engagement(self, engagement_obj, access_token):
        return self.api_call(api_path="engagements", obj=engagement_obj, method='POST', access_token=access_token)

    def edit_engagement(self, engagement_obj, engagement_id, access_token):
        return self.api_call(api_path="engagements/{}".format(engagement_id), obj=engagement_obj, method='PUT',
                             access_token=access_token)

    def delete_engagement(self, engagement_id, access_token):
        return self.api_call(api_path="engagements/{}".format(engagement_id), method='DELETE',
                             access_token=access_token)

    def get_all_positions(self, access_token):
        return self.api_call(api_path="positions", method='GET', access_token=access_token)

    def get_position(self, position_id, access_token):
        return self.api_call(api_path="positions/{}".format(position_id), method='GET', access_token=access_token)

    def get_engagement(self, engagement_id, access_token):
        return self.api_call(api_path="engagements/{}".format(engagement_id), method='GET', access_token=access_token)

    def get_all_engagements(self, access_token):
        return self.api_call(api_path="engagements", method='GET', access_token=access_token)

    def get_user(self, user_id, access_token):
        return self.api_call(api_path="users/{}".format(user_id), method='GET', access_token=access_token)
    # protected API calls ----------------------------------------------------------------------------------------------

    @staticmethod
    def api_call(api_path=None, obj=None, method='GET', access_token=None, refresh_token=None):
        url = "http://{}/{}".format(rest_host, api_path)
        headers = None
        if access_token:
            if access_token.startswith("Bearer "):
                headers = {'content-type': 'application/json', 'Access-Control-Allow-Origin': '*',
                           'Authorization': access_token}
            else:
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
