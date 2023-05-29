import os
import requests

# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1

class ApiWrapper:
    def __init__(self, _client_id=None, _client_secret=None):
        self.BASE_URI = os.environ["HOSTNAME"] or "http://localhost"
        self.AUTHORIZATION_CLIENT_PATH = "/oauth/token"
        self.AUTHORIZATION_END_USER_PATH = "/oauth/authorize"

        self.session = requests.Session()
        self.client_id = _client_id if _client_id else os.environ["CLIENT_ID"]
        self.client_secret = _client_secret if _client_secret else os.environ["CLIENT_SECRET"]
        self.verbose = False
        self.verify = True
        self.auth_token = None

        self.REDIRECT_URI = os.environ["REDIRECT_URI"] or "http://localhost"

    def authorize_client(self):
        """
            @response:
              {
                  "access_token": "GHSjze1H5ivL2Q2uMGyf",
                  "token_type": "Bearer",
                  "expires_in": 26947575,
                  "scope": "basic_info building_list building_details feedback",
                  "created_at": 1565983436
              }
        """
        if self.verbose:
            print("authorize_client", self.AUTHORIZATION_CLIENT_PATH)

        auth_client = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        url = self.BASE_URI + self.AUTHORIZATION_CLIENT_PATH
        return self.session.post(url, data=auth_client, verify=self.verify)

    def get(self, _path: str, _options=None):
        headers = _options["headers"] if _options and "headers" in _options else {}

        query = _options["query"] if _options and "query" in _options else {}
        _path += "?" + self.__mount_query_string__(query)

        access_token = self.__get_authorization_token()
        headers["Authorization"] = access_token

        url = self.BASE_URI + _path
        return self.session.get(url, headers=headers, verify=self.verify)

    def post(self, _path: str, _options=None):
        headers = _options["headers"] if _options and "headers" in _options else {}
        data = _options["data"] if _options and "data" in _options else {}

        access_token = self.__get_authorization_token()
        headers["Authorization"] = access_token

        url = self.BASE_URI + _path
        return self.session.post(url, data=data, headers=headers, verify=self.verify)

    def __get_authorization_token(self):
        if self.auth_token:
            return self.auth_token
        response = self.authorize_client()
        j_response = response.json()
        self.auth_token = "{0} {1}".format(j_response["token_type"], j_response["access_token"])

        return self.auth_token

    def __mount_query_string__(self, _filters):
        """
            Mounts a query string from a dictionary
        """
        query = ""
        # loops over all filters
        for _key in _filters:
            # checks if a filter is array to mount a formated string as 
            # key[]=value1&key[]=value2&key[]=value3
            if isinstance(_filters[_key], list):
                for f in _filters[_key]:
                    if query != "":
                        query += "&"
                    query += str(_key) + "[]=" + str(f)
            else:
                # else, simply mounts a string as key=value
                if query != "":
                    query += "&"
                query += str(_key) + "=" + str(_filters[_key])
        return query

class Config:
    def __init__(self, _wrapper: ApiWrapper):
        self.ENDPOINT = "/api/config"
        self.ENDPOINT_ID = "/api/config/{0}"
        self.wrapper = _wrapper

    def list_settings(self, _filters=None):
        _filters = {} if not _filters else _filters
        options = {
            "query": _filters
        }
        response = self.wrapper.get(self.ENDPOINT, options)
        return response.json()

    def get_setting(self, _setting_id: str):
        url = self.ENDPOINT_ID.format(_setting_id)
        response = self.wrapper.get(url)
        return response.json()
