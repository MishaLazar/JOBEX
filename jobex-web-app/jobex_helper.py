import requests


class JobexHelper:
    def __init__(self, host):
        self.host = host


def create_user(self, username, email, password):
    url = "http://{}/user".format(host)

    try:
        response_string = self.get_uri(url, expected_status_codes=200).response.content
    except requests.RequestException as e:
        message = "Failed to create user. Error '{}'".format(e)
        raise IOError(message)
    return response_string