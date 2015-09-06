import unittest
import user_group_db
from user_group_db import DuplicateUserException
from user_group_db import DuplicateGroupException
from user_group_db import NoSuchUserException
from user_group_db import NoSuchGroupException


class UserGroupTest(unittest.TestCase):

    def setUp(self):
        self.user_group = user_group_db.UserGroup()

        self.sample_user = {'userid': 'bob',
                            'first_name': 'Bob',
                            'last_name': 'Brown',
                            'groups': []}

        self.sample_user_2 = {'userid': 'billy',
                              'first_name': 'Billy',
                              'last_name': 'Braun',
                              'groups': []}

    def tearDown(self):
        pass

    def test_add_user(self):

        self.user_group.add_user(self.sample_user)
        assert len(self.user_group.users) is 1
        assert self.user_group.users['bob']
        assert cmp(self.user_group.users['bob'], self.sample_user) is 0

    def test_add_duplicate_user(self):
        
        self.user_group.add_user(self.sample_user)

        with self.assertRaises(DuplicateUserException):
            self.user_group.add_user(self.sample_user)

    def test_add_user_bad_group(self):

        self.sample_user['groups'] = ['bad_group']

        with self.assertRaises(NoSuchGroupException):
            self.user_group.add_user(self.sample_user)

    def test_get_user(self):

        self.user_group.users = {self.sample_user['userid']: self.sample_user}
        user = self.user_group.get_user('bob')

        assert cmp(self.sample_user, user) is 0

    def test_get_nonexistent_user(self):

        with self.assertRaises(NoSuchUserException):
            self.user_group.get_user('bob')

    def test_delete_user(self):
        self.user_group.users = {self.sample_user['userid']: self.sample_user}
        self.user_group.delete_user('bob')

        assert len(self.user_group.users) is 0

    def test_delete_nonexistent_user(self):
        with self.assertRaises(NoSuchUserException):
            self.user_group.delete_user('bob')

    def test_update_user(self):
        self.user_group.users[self.sample_user['userid']] = self.sample_user
        updated_user = self.sample_user
        updated_user['first_name'] = 'Ralph'
        updated_user['last_name'] = 'Gordon'
        self.user_group.update_user(updated_user['userid'], updated_user)
        saved_user = self.user_group.users['bob']
        assert cmp(saved_user, updated_user) is 0

    def test_update_user_mismatched_userid(self):
        self.user_group.users[self.sample_user['userid']] = self.sample_user
        updated_user = self.sample_user
        updated_user['first_name'] = 'Ralph'
        updated_user['last_name'] = 'Gordon'

        with self.assertRaises(Exception):
            self.user_group.update_user('bad_user_id', updated_user)

    def test_update_nonexistent_user(self):
        with self.assertRaises(NoSuchUserException):
            self.user_group.update_user(self.sample_user['userid'], self.sample_user)

    def test_add_group(self):
        self.user_group.add_group('test_group')
        assert len(self.user_group.groups) is 1
        assert self.user_group.groups[0] is 'test_group'

    def test_add_duplicate_group(self):
        self.user_group.add_group('test_group')
        with self.assertRaises(DuplicateGroupException):
            self.user_group.add_group('test_group')

    def test_add_user_with_good_group(self):
        self.user_group.groups.append('test_group')
        self.sample_user['groups'] = ['test_group']
        self.user_group.add_user(self.sample_user)
   
        assert len(self.user_group.users) is 1

    def test_delete_group(self):
        self.user_group.groups.append('test_group')
        self.user_group.delete_group('test_group')
        assert(len(self.user_group.groups)) is 0

    def test_delete_nonexistent_group(self):
        with self.assertRaises(NoSuchGroupException):
            self.user_group.delete_group('test_group')

    def test_delete_group_with_user(self):

        self.user_group.groups.append('test_group')
        self.sample_user['groups'] = ['test_group']
        self.user_group.users[self.sample_user['userid']] = self.sample_user
        self.user_group.delete_group('test_group')

        assert len(self.user_group.groups) is 0

        user = self.user_group.get_user('bob')
        assert len(user['groups']) is 0 

    def test_get_group_users(self):

        self.user_group.groups = ['test_group']
        self.sample_user['groups'] = ['test_group']
        self.sample_user_2['groups'] = ['test_group_2']

        self.user_group.users = {self.sample_user['userid']: self.sample_user,
                                 self.sample_user_2['userid']: self.sample_user_2}

        users = self.user_group.get_group('test_group')
        assert len(users) is 1
        assert users.index('bob') >= 0

        self.user_group.users[self.sample_user_2['userid']]['groups'].append('test_group')
        users = self.user_group.get_group('test_group')
        assert len(users) is 2
        assert users.index('bob') >= 0
        assert users.index('billy') >= 0

    def test_update_group_add_all_users(self):
        self.user_group.groups = ['test_group']
        self.user_group.users = {self.sample_user['userid']: self.sample_user,
                                 self.sample_user_2['userid']: self.sample_user_2}

        self.user_group.update_group('test_group', ['bob', 'billy'])

        assert self.user_group.users['bob']['groups'].index('test_group') >= 0
        assert self.user_group.users['billy']['groups'].index('test_group') >= 0

    def test_update_group_add_one_user(self):
        self.user_group.groups = ['test_group']
        self.user_group.users = {self.sample_user['userid']: self.sample_user,
                                 self.sample_user_2['userid']: self.sample_user_2}

        self.user_group.update_group('test_group', ['bob'])

        assert self.user_group.users['bob']['groups'].index('test_group') >= 0
        with self.assertRaises(Exception):
            assert self.user_group.users['billy']['groups'].index('test_group') >= 0

    def test_update_group_with_nonexistent_group(self):
        self.user_group.users = {self.sample_user['userid']: self.sample_user,
                                 self.sample_user_2['userid']: self.sample_user_2}

        with self.assertRaises(Exception):
            self.user_group.update_group('test_group', ['bob', 'billy'])

    def test_update_group_with_nonexistent_member(self):
        self.user_group.groups = ['test_group']
        self.user_group.users = {self.sample_user['userid']: self.sample_user,
                                 self.sample_user_2['userid']: self.sample_user_2}

        with self.assertRaises(Exception):
            self.user_group.update_group('test_group', ['bob', 'billy', 'joe'])

if __name__ == '__main__':
    unittest.main()
