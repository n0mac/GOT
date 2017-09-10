import requests
import unittest
import json

DEFAULT_HEADER = 'application/json'

SUCCESS = 200
INCORRECT_HEADER = 400
ADDED = 201
NOT_AUTHORIZED = 404
REMOVED = 204

GET_USER = "/users/{user}"
GET_FOLLOWERS = "/followers"
GET_USER_FOLLOWERS = "/users/{user}/followers"
GET_USER_COMMITS = "/repos/{user}/{repo}/commits"
GET_USER_COMMIT_BY_SHA2 = "/repos/{user}/{repo}/commits/{sha}"
GET_USER_COMMIT_BY_SHA = "https://api.github.com/repos/{user}/{repo}/commits/{sha}"
GET_USER_COMMIT_COMMENTS_URL = "https://api.github.com/repos/n0mac/trek/commits/e9bd1f80c0bb60bc4d248d36b2a1804ac07ae314/comments"
GITHUB_AUTHORIZATIONS_URL = "https://api.github.com/authorizations"
GITHUB_COMMENT_ID_URL = "https://api.github.com/repos/{user}/{repo}/comments/{id}"
AUTH_TOKEN = "token 95334a5a5dc2ce71e79d05b026895eb5eab4c50b"

USER = "n0mac"
REPO = "trek"
SHA = "4ace7325787475b1a8e72b0e96da271187f19a99"


class TestCommitsFunctionality(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(TestCommitsFunctionality, self).__init__(*a, **kw)
        self.host = 'api.github.com'
        self.command = 'repos'
        self.url = 'http://{}/{}'.format(self.host, self.command)
        self.user = 'n0mac'
        self.repo = 'trek'
        self.sha = '522b0fa809b8af60edf44e0fb06aad12963b8fe1'
        self.comments = 'comments'
        self.get_user_commit_by_sha = "https://api.github.com/repos/{}/{}/commits/{}".format(self.user, self.repo, self.sha)
        self.get_user_commit_by_sha2 = "https://api.github.com/repos/{}/{}/commits/{}/{}".format(self.user, self.repo, self.sha,self.comments)
        self.comment_id_url = "https://api.github.com/repos/{}/{}/comments/".format(self.user, self.repo)

    def test_commit_author(self):
        status_code, body = self._get_commits()
        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(body['commit']['author']['name'], 'n0mac')
        self.assertEqual(body['commit']['author']['email'], 'smiling.n0mac@gmail.com')

    def test_commit_committer(self):
        status_code, body = self._get_commits()
        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(body['commit']['committer']['name'], 'n0mac')
        self.assertEqual(body['commit']['committer']['email'], 'smiling.n0mac@gmail.com')

    def test_commits_comments_count(self):

        # GET comments count
        status_code, body = self._get_commits()
        self.assertEqual(status_code, SUCCESS)
        self.assertTrue(body['commit']['comment_count'], int)
        self.comment_count = body['commit']['comment_count']

        # Add new comment
        status_code, body = self._add_comment()
        self.assertEqual(status_code, ADDED)
        self.assertEqual(body['body'], 'test1')

        # Check if comments count changed to +1
        status_code, body = self._get_commits()
        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(body['commit']['comment_count'], self.comment_count+1)

    def test_adding_comments_not_logged_in_user(self):
        status_code, body = self._add_comment_not_logged_in()
        self.assertEqual(status_code, NOT_AUTHORIZED)
        #self.assertEqual(body['body'], 'test')

    def test_removing_of_added_comment(self):
        status_code, body = self._get_commits_comments()
        self.assertEqual(status_code, ADDED)
        self.comment_id = body["id"]
        #self.assertEqual(body['id'], self.id)

        status_code = self._remove_commits_comment()
        self.assertEqual(status_code, REMOVED)

    def test_updating_of_added_comment(self):
        status_code, body = self._get_commits_comments()
        self.assertEqual(status_code, ADDED)
        self.comment_id = body["id"]

        status_code, body = self._update_commit_comment()
        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(body["body"], 'updated')


    def _get_commits(self, identificator=None):
        _url = self.get_user_commit_by_sha
        if identificator:
            _url = "{}/{}".format(self.url, identificator)
        _response1 = requests.get(_url)
        json_o = json.loads(_response1.content)
        return _response1.status_code, json_o

    def _update_commit_comment(self, identificator=None):
        _header = {'Accept': DEFAULT_HEADER, 'Content-Type': DEFAULT_HEADER, 'Authorization': AUTH_TOKEN}
        _payload = json.dumps({'body': 'updated'})
        _response1 = requests.patch(self.comment_id_url+str(self.comment_id), headers=_header, data=_payload)
        json_o = json.loads(_response1.content)
        print(_response1.json())
        return _response1.status_code, json_o

    def _get_commits_comments(self, identificator=None):
        _header = {'Accept': DEFAULT_HEADER, 'Content-Type': DEFAULT_HEADER, 'Authorization': AUTH_TOKEN}
        _payload = json.dumps({'body': 'test2', 'path': '', 'position': 4, 'line': None})
        _response1 = requests.post(self.get_user_commit_by_sha2, headers=_header, data=_payload)
        json_o = json.loads(_response1.content)
        print(_response1.json())
        return _response1.status_code, json_o

    def _remove_commits_comment(self, identificator=None):
        _header = {'Accept': DEFAULT_HEADER, 'Content-Type': DEFAULT_HEADER, 'Authorization': AUTH_TOKEN}
        _response1 = requests.delete(self.comment_id_url+str(self.comment_id), headers=_header)
        return _response1.status_code

    def _add_comment(self):
        _header = {'Accept': DEFAULT_HEADER, 'Content-Type': DEFAULT_HEADER,'Authorization': AUTH_TOKEN}
        _payload = json.dumps({'body': 'test1', 'path': '', 'position': 4, 'line': None})
        _response = requests.post(self.get_user_commit_by_sha2, headers=_header, data=_payload)
        #print(_response.json())
        return _response.status_code, _response.json()

    def _add_comment_not_logged_in(self):
        _payload = json.dumps({'body': 'test1', 'path': '', 'position': 4, 'line': None})
        _response = requests.post(self.get_user_commit_by_sha2, data=_payload)
        #print(_response.json())
        return _response.status_code, _response.json()





