import copy


class UserGroupData:
    def __init__(self):
        self.groups = []
        self.users = {}

    def reset(self):
        self.groups = []
        self.users = {}

    def add_user(self, new_user):
        if not new_user['userid'] in self.users:
            for group in new_user['groups']:
                if not group in self.groups:
                    raise NoSuchGroupException('group "{0}" does not exist'.format(group))

            self.users[new_user['userid']] = copy.deepcopy(new_user)

        else:
            raise DuplicateUserException(new_user['userid'])

    def get_user(self, userid):
        if userid in self.users:
            return self.users[userid]
        else:
            raise NoSuchUserException('user "{0}" does not exist'.format(userid))

    def delete_user(self, userid): 
        try:
            self.users.pop(userid)
        except:
            raise NoSuchUserException('user "{0}" does not exist'.format(userid))

    def update_user(self, userid, user):
        if userid != user['userid']:
            raise Exception('bad request')

        if user['userid'] not in self.users:
            raise NoSuchUserException('user "{0}" does not exist'.format(userid))

        for group in user['groups']:
            if not group in self.groups:
                raise NoSuchGroupException('group "{0}" does not exist'.format(group))

        self.users[user['userid']] = user

    def add_group(self, group_name):
        if group_name in self.groups:
            raise DuplicateGroupException('group "{0}" already exists'.format(group_name))
        else:
            self.groups.append(group_name)

    def get_group(self, group_name):
        users = []
        if not group_name in self.groups:
            raise NoSuchGroupException('group {0} does not exist'.format(group_name))
        else:
            for user_key in self.users:
                if group_name in self.users[user_key]['groups']:
                    users.append(self.users[user_key]['userid'])

        return users

    def delete_group(self, group_name):
        if group_name in self.groups:
            self.groups.remove(group_name)
            for username in self.users:
                if group_name in self.users[username]['groups']:
                    self.users[username]['groups'].remove(group_name)
        else:
            raise NoSuchGroupException('group "{0}" does not exist'.format(group_name))

    def update_group(self, group_name, group_members):
        if not group_name in self.groups:
            raise NoSuchGroupException('group "{0}" does not exist'.format(group_name))
        for member in group_members:
            if not member in self.users:
                raise NoSuchUserException('user "{0}" does not exist'.format(member))
        for username in self.users:
            if group_name in self.users[username]['groups']:
                self.users[username]['groups'].remove(group_name)
        for member in group_members:
            self.users[member]['groups'].append(group_name)


class NoSuchGroupException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NoSuchUserException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DuplicateUserException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DuplicateGroupException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)