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
                     raise Exception('group does not exist')
            self.users[new_user['userid']] = new_user

        else:
            raise Exception('user already exists')

    def get_user(self, userid): 
        try:
            user = self.users[userid]
            return user
        except:
            raise Exception('user does not exist') 

    def delete_user(self, userid): 
        try:
            self.users.pop(userid)
        except:
            raise Exception('user does not exist')

    def update_user(self, user):
        user_to_update = self.get_user(user['userid'])
        if user_to_update is None:
            raise Exception('user does not exist')

        for group in user['groups']:
            if not self.group_exists(group):
                raise Exception('group does not exist')

        self.users[user['userid']] = user


    def group_exists(self, group_name):
        try:
            self.groups.index(group_name)
            return True

        except: 
            return False

    def add_group(self, group_name):
        if self.group_exists(group_name):
            return False
        else:
            self.groups.append(group_name)
            return True

    def get_group(self, group_name):
        users = []
        if not self.group_exists(group_name):
            raise Exception('group does not exist')
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
                    print e    
                
        else:
            raise Exception('group does not exist')            
