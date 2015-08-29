from flask import Flask
from flask import abort
from user_group_db import UserGroup

app = Flask(__name__)
db = UserGroup()

@app.route('/users/<userid>')
def get_user(userid):
    user = db.get_user(userid)
    if user is None:
        abort(404) 
    return user

@app.route('/users', methods=['POST'])
def post_user():
    return request.get_json()

@app.route('/users/<userid>', methods=['DELETE', 'PUT'])
def modify_user(userid):
    return 'deleting ' + userid

@app.route('/groups/<groupname>')
def get_group(groupname):
    return groupname

@app.route('/groups', methods=['POST'])
def post_group():
    db.add_group('group')
    return 'abc' 

@app.route('/groups/<group_name>', methods=['DELETE', 'PUT'])
def modify_group():
    return true

if __name__ == '__main__':
    
    
    app.run()

