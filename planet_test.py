import unittest
import json
import rest
from rest import db


class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.app = rest.app.test_client()
        self.sample_user_json = ('{"userid": "jim",'
                                 '"firstname": "Bob",'
                                 '"lastname": "Brown",'
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

    def test_add_get_delete_group(self):
        rv = self.app.post('/groups', data='{"name": "test-group"}')
        assert rv.status_code == 200
        rv = self.app.post('/groups', data='{"name": "test-group"}')
        assert rv.status_code == 409
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
        assert ret_array.index('jim') >= 0
        assert ret_array.index('another_user') >= 0

    def test_delete_group(self):
        self.populate_db()
        self.app.delete('/groups/test-group')
        rv = self.app.get('/groups/test-group')
        assert rv.status_code == 404

        rv = self.app.get('/users/jim')
        assert rv.status_code == 200
        with self.assertRaises(Exception):
            json.loads(rv.data)['groups'].index('test-group')

        rv = self.app.get('/users/another_user')
        assert rv.status_code == 200
        with self.assertRaises(Exception):
            json.loads(rv.data)['groups'].index('test-group')

    def populate_db(self):
        self.app.post('/groups', data='{"name": "test-group"}')
        self.sample_user_dict['groups'] = ['test-group']
        self.app.post('/users', data=json.dumps(self.sample_user_dict))
        self.sample_user_dict['userid'] = 'another_user'
        self.app.post('/users', data=json.dumps(self.sample_user_dict))


if __name__ == '__main__':
    unittest.main()
