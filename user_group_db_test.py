import unittest
import user_group_db
from duplicate_user_exception import DuplicateUserException
from duplicate_group_exception import DuplicateGroupException
from no_such_user_exception import NoSuchUserException
from no_such_group_exception import NoSuchGroupException

class UserGroupTest(unittest.TestCase):

    def setUp(self):
        self.userGroup = user_group_db.UserGroup()

        self.sample_user = {'userid': 'bob',
                            'firstname': 'Bob',
                            'lastname': 'Brown',
                            'groups': []}

        self.sample_user_2 = {'userid': 'billy',
                              'firstname': 'Billy',
                              'lastname': 'Braun',
                              'groups': []}

    def tearDown(self): pass

    def test_add_user(self):

        self.userGroup.add_user(self.sample_user)
        assert len(self.userGroup.users) is 1
        assert self.userGroup.users['bob']
        assert cmp(self.userGroup.users['bob'], self.sample_user) is 0

    def test_add_duplicate_user(self):
        
        self.userGroup.add_user(self.sample_user)

        with self.assertRaises(DuplicateUserException):
            self.userGroup.add_user(self.sample_user)

    def test_add_user_bad_group(self):

        self.sample_user['groups'] = ['bad_group']

        with self.assertRaises(NoSuchGroupException):
            self.userGroup.add_user(self.sample_user)

    def test_get_user(self):

        self.userGroup.users = {}
        self.userGroup.users[self.sample_user['userid']] = self.sample_user
        user = self.userGroup.get_user('bob')

        assert cmp(self.sample_user, user) is 0

    def test_get_nonexistent_user(self):

        with self.assertRaises(NoSuchUserException):
            self.userGroup.get_user('bob')

    def test_delete_user(self):
        self.userGroup.users = {self.sample_user['userid']: self.sample_user}
        self.userGroup.delete_user('bob')

        assert len(self.userGroup.users) is 0

    def test_delete_nonexistent_user(self):
        with self.assertRaises(NoSuchUserException):
            self.userGroup.delete_user('bob')

    def test_update_user(self):
        self.userGroup.users[self.sample_user['userid']] = self.sample_user
        updated_user = self.sample_user
        updated_user['firstname'] = 'Ralph'
        updated_user['lastname'] = 'Gordon'
        self.userGroup.update_user(updated_user['userid'], updated_user)
        saved_user = self.userGroup.users['bob']
        assert cmp(saved_user, updated_user) is 0

    def test_update_user_mismatched_userid(self):
        self.userGroup.users[self.sample_user['userid']] = self.sample_user
        updated_user = self.sample_user
        updated_user['firstname'] = 'Ralph'
        updated_user['lastname'] = 'Gordon'

        with self.assertRaises(Exception):
            self.userGroup.update_user('bad_user_id', updated_user)

    def test_update_nonexistent_user(self):
        with self.assertRaises(NoSuchUserException):
            self.userGroup.update_user(self.sample_user['userid'], self.sample_user)

    def test_add_group(self):
        self.userGroup.add_group('test_group')
        assert len(self.userGroup.groups) is 1
        assert self.userGroup.groups[0] is 'test_group'

    def test_add_duplicate_group(self):
        self.userGroup.add_group('test_group')
        with self.assertRaises(DuplicateGroupException):
            self.userGroup.add_group('test_group')

    def test_add_user_with_good_group(self):
        self.userGroup.groups.append('test_group')
        self.sample_user['groups'] = ['test_group']
        self.userGroup.add_user(self.sample_user)
   
        assert len(self.userGroup.users) is 1

    def test_delete_group(self):
        self.userGroup.groups.append('test_group')
        self.userGroup.delete_group('test_group')
        assert(len(self.userGroup.groups)) is 0

    def test_delete_nonexistent_group(self):
        with self.assertRaises(NoSuchGroupException):
            self.userGroup.delete_group('test_group')

    def test_delete_group_with_user(self):

        self.userGroup.groups.append('test_group')
        self.sample_user['groups'] = ['test_group']
        self.userGroup.users[self.sample_user['userid']] = self.sample_user
        self.userGroup.delete_group('test_group')

        assert len(self.userGroup.groups) is 0

        user = self.userGroup.get_user('bob')
        assert len(user['groups']) is 0 

    def test_get_group_users(self):

        self.userGroup.groups = ['test_group']
        self.sample_user['groups'] = ['test_group']
        self.sample_user_2['groups'] = ['test_group_2']

        self.userGroup.users = {}
        self.userGroup.users[self.sample_user['userid']] = self.sample_user
        self.userGroup.users[self.sample_user_2['userid']] = self.sample_user_2

        users = self.userGroup.get_group('test_group')
        assert len(users) is 1
        assert users.index('bob') >= 0

        self.userGroup.users[self.sample_user_2['userid']]['groups'].append('test_group')
        users = self.userGroup.get_group('test_group')
        assert len(users) is 2
        assert users.index('bob') >= 0
        assert users.index('billy') >= 0

    def test_update_group_add_all_users(self):
        self.userGroup.groups = ['test_group']
        self.userGroup.users = {}
        self.userGroup.users[self.sample_user['userid']] = self.sample_user
        self.userGroup.users[self.sample_user_2['userid']] = self.sample_user_2

        self.userGroup.update_group('test_group', ['bob', 'billy'])

        assert self.userGroup.users['bob']['groups'].index('test_group') >= 0
        assert self.userGroup.users['billy']['groups'].index('test_group') >= 0

    def test_update_group_add_one_user(self):
        self.userGroup.groups = ['test_group']
        self.userGroup.users = {}
        self.userGroup.users[self.sample_user['userid']] = self.sample_user
        self.userGroup.users[self.sample_user_2['userid']] = self.sample_user_2

        self.userGroup.update_group('test_group', ['bob'])

        assert self.userGroup.users['bob']['groups'].index('test_group') >= 0
        with self.assertRaises(Exception):
            assert self.userGroup.users['billy']['groups'].index('test_group') >= 0

    def test_update_group_with_nonexistent_group(self):
        self.userGroup.users = {}
        self.userGroup.users[self.sample_user['userid']] = self.sample_user
        self.userGroup.users[self.sample_user_2['userid']] = self.sample_user_2

        with self.assertRaises(Exception):
            self.userGroup.update_group('test_group', ['bob', 'billy'])

    def test_update_group_with_nonexistent_member(self):
        self.userGroup.groups = ['test_group']
        self.userGroup.users = {}
        self.userGroup.users[self.sample_user['userid']] = self.sample_user
        self.userGroup.users[self.sample_user_2['userid']] = self.sample_user_2

        with self.assertRaises(Exception):
            self.userGroup.update_group('test_group', ['bob', 'billy', 'joe'])

if __name__ == '__main__':
    unittest.main()
