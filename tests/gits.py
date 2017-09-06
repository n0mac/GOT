import requests
import unittest
import json


DEFAULT_HEADER = 'application/json'

SUCCESS = 200
INCORRECT_HEADER = 400
ADDED = 201

GET_USER = "/users/{user}"
GET_FOLLOWERS = "/followers"
GET_USER_FOLLOWERS = "/users/{user}/followers"
GET_USER_COMMITS = "/repos/{user}/{repo}/commits"
GET_USER_COMMIT_BY_SHA2 = "/repos/{user}/{repo}/commits/{sha}"
GET_USER_COMMIT_BY_SHA = "https://api.github.com/repos/{user}/{repo}/commits/{sha}"
GET_USER_COMMIT_COMMENTS_URL = "https://api.github.com/repos/n0mac/trek/commits/e9bd1f80c0bb60bc4d248d36b2a1804ac07ae314/comments"
GITHUB_AUTHORIZATIONS_URL = "https://api.github.com/authorizations"
GITHUB_COMMENT_ID_URL = "https://api.github.com/repos/{user}/{repo}/comments/{id}"

USER = "n0mac"
REPO = "trek"
SHA = "522b0fa809b8af60edf44e0fb06aad12963b8fe1"


class TestCommitsFunctionality(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(TestCommitsFunctionality, self).__init__(*a, **kw)
        self.host = 'api.github.com'
        self.command = 'repos'
        self.url = 'http://{}/{}'.format(self.host, self.command)
        self.user = 'n0mac'
        self.repo = 'trek'
        self.sha = '522b0fa809b8af60edf44e0fb06aad12963b8fe1'
        self.get_user_commit_by_sha = "https://api.github.com/repos/{}/{}/commits/{}".format(self.user, self.repo, self.sha)

    def test_commit_author(self):
        status_code, body = self._get_commits()
        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(body['commit']['author']['name'], 'n0mac')
        self.assertEqual(body['commit']['author']['email'], 'smiling.n0mac@gmail.com')

    def _get_commits(self, identificator=None):
        _url = self.get_user_commit_by_sha
        if identificator:
            _url = "{}/{}".format(self.url, identificator)
        _response1 = requests.get(_url)
        json_o = json.loads(_response1.content)
        return _response1.status_code, json_o

