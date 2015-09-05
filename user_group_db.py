import copy
from duplicate_user_exception import DuplicateUserException
from duplicate_group_exception import DuplicateGroupException
from no_such_user_exception import NoSuchUserException
from no_such_group_exception import NoSuchGroupException

class UserGroup:
    def __init__(self):
        self.groups = []
        self.users = {}

    def user_exists(self, userid):
        try:
            self.users[userid]
            return True
        except:
            return False

    def add_user(self, new_user):
        if not self.user_exists(new_user['userid']):
            for group in new_user['groups']:
                if not self.group_exists(group):
                     raise NoSuchGroupException('group "{0}" does not exist'.format(group))

            self.users[new_user['userid']] = copy.deepcopy(new_user)

        else:
            raise DuplicateUserException(new_user['userid'])

    def get_user(self, userid): 
        try:
            user = self.users[userid]
            return user
        except:
            raise NoSuchUserException(userid)

    def delete_user(self, userid): 
        try:
            self.users.pop(userid)
        except:
            raise NoSuchUserException('user "{0}" does not exist'.format(userid))

    def update_user(self, userid, user):
        if userid != user['userid']:
            raise Exception('bad request')

        user_to_update = self.get_user(user['userid'])
        if user_to_update is None:
            raise NoSuchUserException('user "{0}" does not exist'.format(userid))

        for group in user['groups']:
            if not self.group_exists(group):
                raise NoSuchGroupException('group "{0}" does not exist'.format(group))

        self.users[user['userid']] = user


    def group_exists(self, group_name):
        try:
            self.groups.index(group_name)
            return True

        except: 
            return False

    def add_group(self, group_name):
        if self.group_exists(group_name):
            raise DuplicateGroupException('group "{0}" already exists'.format(group_name))
        else:
            self.groups.append(group_name)

    def get_group(self, group_name):
        users = []
        if not self.group_exists(group_name):
            raise NoSuchGroupException('group {0} does not exist'.format(group_name))
        else:
            for user_key in self.users:
                try:
                     self.users[user_key]['groups'].index(group_name)
                     users.append(self.users[user_key]['userid'])
                except:
                     continue

        return users

    def delete_group(self, group_name):
        if self.group_exists(group_name):
            self.groups.remove(group_name)
            for username in self.users:
                try:
                    self.users[username]['groups'].remove(group_name)
                except Exception, e:
                    continue
        else:
            raise NoSuchGroupException('group "{0}" does not exist'.format(group_name))

    def update_group(self, group_name, group_members):
        if not self.group_exists(group_name):
            raise NoSuchGroupException('group "{0}" does not exist'.format(group_name))
        for member in group_members:
            if not self.user_exists(member):
                raise NoSuchUserException('user "{0}" does not exist'.format(member))
        for user in self.users:
            try:
                user['groups'].remove(group_name)
            except:
                continue
        for member in group_members:
            self.users[member]['groups'].append(group_name)