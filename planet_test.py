import unittest
import json
import rest
import copy
from rest import db


class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.app = rest.app.test_client()
        self.sample_user_json = ('{"userid": "jim",'
                                 '"first_name": "Bob",'
                                 '"last_name": "Brown",'
                                 '"groups": []}')
        self.sample_user_dict = json.loads(self.sample_user_json)

    def tearDown(self):
        db.reset()

    def test_get_on_empty_db(self):
        rv = self.app.get('/users/no-user')
        assert rv.status_code == 404

        rv = self.app.get('/group/no-group')
        assert rv.status_code == 404

    def test_post_and_get_user(self):
        rv = self.app.post('/users', data=self.sample_user_json)
        assert rv.status_code == 200
        rv = self.app.get('/users/jim')
        assert rv.status_code == 200
        ret_data = json.loads(rv.data)
        assert 0 == cmp(ret_data, self.sample_user_dict)

    def test_post_user_with_bad_group(self):
        self.sample_user_dict['groups'] = ['bad-group']
        bad_json = json.dumps(self.sample_user_dict)
        rv = self.app.post('/users', data=bad_json)
        assert rv.status_code == 400

    def test_add_duplicate_user(self):
        self.app.post('/users', data=self.sample_user_json)
        rv = self.app.post('/users', data=self.sample_user_json)
        assert rv.status_code == 409

    def test_post_duplicate_group(self):
        rv = self.app.post('/groups', data='{"name": "test-group"}')
        assert rv.status_code == 200
        rv = self.app.post('/groups', data='{"name": "test-group"}')
        assert rv.status_code == 409

    def test_add_get_delete_group(self):
        self.app.post('/groups', data='{"name": "test-group"}')
        rv = self.app.get('/groups/test-group')
        assert rv.status_code == 200
        assert 0 == len(json.loads(rv.data))
        rv = self.app.delete('/groups/test-group')
        assert rv.status_code == 200
        rv = self.app.delete('/groups/test-group')
        assert rv.status_code == 404
        rv = self.app.get('/groups/test-group')
        assert rv.status_code == 404

    def test_add_users_to_group(self):
        self.app.post('/groups', data='{"name": "test-group"}')
        self.sample_user_dict['groups'] = ['test-group']
        rv = self.app.post('/users', data=json.dumps(self.sample_user_dict))
        assert rv.status_code == 200
        rv = self.app.get('/groups/test-group')
        assert rv.status_code == 200
        ret_array = json.loads(rv.data)
        assert 1 == len(ret_array)
        assert ret_array[0] == self.sample_user_dict['userid']
        self.sample_user_dict['userid'] = 'another_user'
        rv = self.app.post('/users', data=json.dumps(self.sample_user_dict))
        assert rv.status_code == 200
        rv = self.app.get('/groups/test-group')
        assert rv.status_code == 200
        ret_array = json.loads(rv.data)
        assert 2 == len(ret_array)
        assert 'jim' in ret_array
        assert 'another_user' in ret_array

    def test_delete_group(self):
        self.populate_db()
        self.app.delete('/groups/test-group')
        rv = self.app.get('/groups/test-group')
        assert rv.status_code == 404

        rv = self.app.get('/users/jim')
        assert rv.status_code == 200
        assert 'test-group' not in json.loads(rv.data)['groups']

        rv = self.app.get('/users/another_user')
        assert rv.status_code == 200
        assert 'test-group' not in json.loads(rv.data)['groups']

    def test_update_user(self):
        self.populate_db()
        self.sample_user_dict['groups'] = ['test-group', 'test-group2']
        self.sample_user_dict['first_name'] = "Carl"
        self.sample_user_dict['last_name'] = "Reiner"
        rv = self.app.put('/users/jim', data=json.dumps(self.sample_user_dict))
        assert rv.status_code == 200

    def test_delete_group_updates_users(self):
        self.populate_db()
        rv = self.app.get('/users/jim')
        ret_user = json.loads(rv.data)
        assert 'test-group' in ret_user['groups']
        self.app.delete('/groups/test-group')
        rv = self.app.get('/users/jim')
        ret_user = json.loads(rv.data)
        assert 'test-group' not in ret_user['groups']

    def populate_db(self):
        local_user = copy.deepcopy(self.sample_user_dict)
        self.app.post('/groups', data='{"name": "test-group"}')
        self.app.post('/groups', data='{"name": "test-group2"}')
        local_user['groups'] = ['test-group']
        self.app.post('/users', data=json.dumps(local_user))
        local_user['userid'] = 'another_user'
        self.app.post('/users', data=json.dumps(local_user))


if __name__ == '__main__':
    unittest.main()
