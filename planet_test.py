import unittest
import json
import rest
from user_group_db import UserGroup


class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.app = rest.app.test_client()
        self.sample_user_json = ('{"userid": "jim",'
                                 '"firstname": "Bob",'
                                 '"lastname": "Brown",'
                                 '"groups": []}')
        self.sample_user_dict = json.loads(self.sample_user_json)

    def tearDown(self):
        pass

    def test_get_on_empty_db(self):
        rv=self.app.get('/users/no-user')
        assert rv.status_code == 404

        rv=self.app.get('/group/no-group')
        assert rv.status_code == 404

    def test_post_and_get_user(self):
        rv=self.app.post('/users', data=self.sample_user_json)
        assert rv.status_code == 200
        rv = self.app.get('/users/jim')
        assert rv.status_code == 200
        ret_data = json.loads(rv.data)
        assert 0 == cmp(ret_data, self.sample_user_dict)

    def test_post_user_with_bad_group(self):
        self.sample_user_dict['groups'] = ['bad-group']
        bad_json = json.dumps(self.sample_user_dict)
        print bad_json
        rv=self.app.post('/users', data=bad_json)
        print 'the status code'
        print rv.status_code
        assert rv.status_code == 400

    def test_add_group(self):
        rv=self.app.post('/groups', data='{"name": "test-group"}')
        assert rv.status_code == 200
        rv=self.app.post('/groups', data='{"name": "test-group"}')
        assert rv.status_code == 409

    def test_post_user(self):
        user = {"userid": "billy"}
        rv = self.app.post('/users', user) 

    def test_post_group(self):
        rv = self.app.post('/groups', 'group')

if __name__ == '__main__':
    unittest.main()
