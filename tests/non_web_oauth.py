import requests
import unittest
import json
from requests.auth import HTTPBasicAuth

class TestOauthNonWeb(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(TestOauthNonWeb, self).__init__(*a, **kw)
        self.client_id = 'b0b93b4a6a2dae43ff23'
        self.client_secret  = 'd3f895625ad17c732a921cadedbd8add6facaddc'
        self.oauth_url = "https://api.github.com/authorizations"
        self.success = 200

    def test_oauth(self):
        status_code = self._add_comment()
        self.assertEqual(status_code, self.success)

    def _add_comment(self):
       # _header = {'Accept': DEFAULT_HEADER, 'Content-Type': DEFAULT_HEADER,'Authorization': AUTH_TOKEN}
        _payload = json.dumps({"note": "admin script", "scopes": "public_repo", "client_id": self.client_id, "client_secret": self.client_secret})
        _response = requests.get(self.oauth_url, auth=('n0mac', 'pzhfg2910'), data=_payload)
        print(_response.json())
        return _response.status_code

