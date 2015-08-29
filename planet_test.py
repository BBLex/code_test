import os
import rest 
import unittest
import json
from unittest.mock import MagicMock

class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.app = rest.app.test_client()

    def tearDown(self): pass

    def test_get_user(self):
        
        mock_db = MagicMock()
        rv = self.app.get('users/10')
        assert 'user has id 10' in rv.data

    def test_post_user(self):
        user = {"userid":"billy"}
        rv = self.app.post('/users', user) 

    def test_post_group(self):
        rv = self.app.post('/groups', 'group')

if __name__ == '__main__':
    unittest.main()
