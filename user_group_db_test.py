import unittest
import user_group_db

class UserGroupTest(unittest.TestCase):

    def setUp(self):
        self.userGroup = user_group_db.UserGroup()

        self.sample_user = {'userid': 'bob',
                           'firstname': 'Bob',
                           'lastname': 'Brown',
                           'groups': []}


    def tearDown(self): pass


    def test_add_user(self):

        self.userGroup.add_user(self.sample_user)
        assert len(self.userGroup.users) is 1


    def test_add_duplicate_user(self):
        
        self.userGroup.add_user(self.sample_user)

        with self.assertRaises(Exception):
            self.userGroup.add_user(self.sample_user)


    def test_add_user_bad_group(self):
        
       self.sample_user['groups'] = ['bad_group']

       with self.assertRaises(Exception):
            self.userGroup.add_user(sample_user)


    def test_get_user(self):
 
        self.userGroup.add_user(self.sample_user)

        user1 = self.sample_user
        user2 = self.userGroup.get_user('bob')
        assert user1['userid'] == user2['userid']
        assert user1['firstname'] == user2['firstname']
        assert user1['lastname'] == user2['lastname']
        assert len(user2['groups']) is 0


    def test_get_nonexistent_user(self):

        with self.assertRaises(Exception):
            self.userGroup.get_user('bob')


    def test_delete_user(self):
        
        self.userGroup.add_user(self.sample_user)

        self.userGroup.delete_user('bob')

        assert len(self.userGroup.users) is 0


    def test_delete_nonexistent_user(self):

        with self.assertRaises(Exception):
            self.userGroup.delete_user('bob')


    def test_add_group(self):
        self.userGroup.add_group('test_group')

        assert len(self.userGroup.groups) is 1


    def test_add_user_with_good_group(self):
        self.userGroup.add_group('test_group')

        self.sample_user['groups'] = ['test_group']
        self.userGroup.add_user(self.sample_user)
   
        assert len(self.userGroup.users) is 1


    def test_delete_group(self):
        self.userGroup.add_group('test_group') 
        self.userGroup.delete_group('test_group')
        assert(len(self.userGroup.groups)) is 0


    def test_delete_nonexistent_group(self):
        with self.assertRaises(Exception):
            self.userGroup.delete_group('test_group')



    def test_delete_group_with_user(self):
        self.userGroup.add_group('test_group')

        self.sample_user['groups'] = ['test_group']
        self.userGroup.add_user(self.sample_user)

        self.userGroup.delete_group('test_group')

        assert len(self.userGroup.groups) is 0

        user = self.userGroup.get_user('bob')

        assert len(user['groups']) is 0 


    def test_get_group_users(self):
        self.userGroup.add_group('test_group')

        self.sample_user['groups'] = ['test_group']
        self.userGroup.add_user(self.sample_user)
        users = self.userGroup.get_group('test_group')
        
        assert len(users) is 1
        assert users[0] is 'bob'
            
        self.sample_user['userid'] = 'billy'
        self.userGroup.add_user(self.sample_user)

        users = self.userGroup.get_group('test_group')
    
        assert len(users) is 2
        assert users.index('bob')
        assert users.index('billy')
        
if __name__ == '__main__':
    unittest.main()
