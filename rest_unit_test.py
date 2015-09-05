import unittest
import rest
import json
from rest import db
from user_group_db import DuplicateGroupException
from user_group_db import DuplicateUserException
from user_group_db import NoSuchGroupException
from user_group_db import NoSuchUserException


class RestUnitTest(unittest.TestCase):

    def setUp(self):
        self.app = rest.app.test_client()
        self.test_user = {'userid': 'bob',
                          'firstname': 'Bob',
                          'lastname': 'Brown',
                          'groups': []}

    def tearDown(self):
        pass

    def test_get_user(self):
        def mock_get(userid):
            return self.test_user
        db.get_user = mock_get

        rv = self.app.get('/users/bob')
        assert rv.status_code == 200

        def mock_get_fail(userid):
            raise NoSuchUserException('')

        db.get_user = mock_get_fail
        rv = self.app.get('/users/bob')
        assert rv.status_code == 404

    def test_post_user(self):
        test_user = {'userid': 'bob',
                     'firstname': 'Bob',
                     'lastname': 'Brown',
                     'groups': []}

        def mock_add(mock_user):
            pass

        db.add_user = mock_add
        rv = self.app.post('/users', data=json.dumps(test_user))
        assert rv.status_code == 200

        def mock_add_duplicate_user(mock_user):
            raise DuplicateUserException('')

        db.add_user = mock_add_duplicate_user
        rv = self.app.post('/users', data=json.dumps(test_user))
        assert rv.status_code == 409

        def mock_add_bad_group(mock_user):
            raise NoSuchGroupException('')

        db.add_user = mock_add_bad_group
        rv = self.app.post('/users', data=json.dumps(test_user))
        assert rv.status_code == 400

    def test_delete_user(self):
        def delete_bad_user(userid):
            raise NoSuchUserException('')

        db.delete_user = delete_bad_user
        rv = self.app.delete('/users/bob')
        assert rv.status_code == 404

        db.delete_user = lambda x: 'success'
        rv = self.app.delete('/users/bob')
        assert rv.status_code == 200

    def test_put_user(self):
        db.update_user = lambda userid, user: 'success'
        rv = self.app.put('/users/bob', data=json.dumps(self.test_user))
        assert rv.status_code == 200

        def delete_bad_user(userid, user):
            raise NoSuchUserException('')

        db.update_user = delete_bad_user
        rv = self.app.put('/users/bob', data=json.dumps(self.test_user))
        assert rv.status_code == 404

        def delete_bad_group(userid, user):
            raise NoSuchGroupException('')

        db.update_user = delete_bad_group
        rv = self.app.put('/users/bob', data=json.dumps(self.test_user))
        assert rv.status_code == 400