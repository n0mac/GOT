import requests
import unittest
import json

class TestOauthNonWeb(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(TestOauthNonWeb, self).__init__(*a, **kw)
        self.first_half = 'b0b93b4a6a'
        self.second_half = '2dae43ff23'
        self.client_id = self.first_half + self.second_half
        self.secret_one = 'd3f895625ad17c732a'
        self.secret_two = '921cadedbd8add6facaddc'
        self.client_secret  = self.secret_one + self.secret_two
        self.oauth_url = "https://api.github.com/authorizations"
        self.success = 200
        self.ok = 201

    def test_oauth_get(self):
        status_code = self._get_method()
        self.assertEqual(status_code, self.success)

    def test_oauth_post(self):
        status_code = self._post_method()
        self.assertEqual(status_code, self.ok)

    def _get_method(self):
        _payload = json.dumps({"note": "admin script", "scopes": "public_repo", "client_id": self.client_id, "client_secret": self.client_secret})
        _response = requests.get(self.oauth_url, auth=('tastytoste', 'qaztgb1029'), data=_payload)
        return _response.status_code

    def _post_method(self):
        _payload = json.dumps({"note": "admin script", "scopes": "public_repo", "client_id": self.client_id, "client_secret": self.client_secret})
        _response = requests.post(self.oauth_url, auth=('tastytoste', 'qaztgb1029'), data=_payload)
        return _response.status_code

if __name__ == '__main__':
    unittest.main()

