from core.api_wrapper import ApiWrapper

class Config:
    def __init__(self, _wrapper: ApiWrapper=None):
        self.ENDPOINT = "/api/config"
        self.ENDPOINT_ID = "/api/config/{0}"
        self.wrapper = _wrapper if not _wrapper is None else ApiWrapper()

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
