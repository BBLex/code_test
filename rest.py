from flask import Flask, request
from flask import abort
from user_group_db import UserGroup
from user_group_db import DuplicateUserException
from user_group_db import DuplicateGroupException
from user_group_db import NoSuchUserException
from user_group_db import NoSuchGroupException
import json

app = Flask(__name__)
db = UserGroup()


@app.route('/users/<userid>')
def get_user(userid):
    try:
        return json.dumps(db.get_user(userid))
    except NoSuchUserException:
        abort(404)


@app.route('/users', methods=['POST'])
def post_user():
    incoming = json.loads(request.data)

    try:
        db.add_user(incoming)
        return 'success'

    except DuplicateUserException:
        abort(409)

    except NoSuchGroupException:
        abort(400)


@app.route('/users/<userid>', methods=['PUT'])
def modify_user(userid):

    try:
        incoming = json.loads(request.data)
        db.update_user(userid, incoming)
        return 'success'

    except NoSuchUserException:
        abort(404)

    except NoSuchGroupException:
        abort(400)


@app.route('/users/<userid>', methods=['DELETE'])
def delete_user(userid):

    try:
        db.delete_user(userid)
        return 'success'

    except NoSuchUserException:
        abort(404)


@app.route('/groups/<groupname>')
def get_group(groupname):
    try:
        result = db.get_group(groupname)
        return json.dumps(result)

    except NoSuchGroupException:
        abort(404)


@app.route('/groups', methods=['POST'])
def post_group():
    try:
        incoming = json.loads(request.data)
        db.add_group(incoming['name'])
        return 'success'

    except DuplicateGroupException:
        abort(409)


@app.route('/groups/<group_name>', methods=['PUT'])
def modify_group(group_name):
    try:
        group_members = json.loads(request.data)
        db.update_group(group_name, group_members)
        return 'success'

    except NoSuchGroupException:
        abort(404)

    except NoSuchUserException:
        abort(409)


@app.route('/groups/<group_name>', methods=['DELETE'])
def delete_group(group_name):
    try:
        db.delete_group(group_name)
        return 'success'

    except NoSuchGroupException:
        abort(404)

if __name__ == '__main__':
    db = UserGroup()
    app.run()

