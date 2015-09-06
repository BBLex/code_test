Requirements:
- Python 2.7.6
- virtualenv:
  sudo pip install virtualenv


Steps to run REST service:

1. Get the code:
   git clone https://github.com/BBLex/code_test.git

2. cd into 'code_test':
   cd code_test

3. Run virtualenv:
   virtualenv venv

4. Activate the virtual environment:
   . venv/bin/activate

5. Install Flask in the virtual environment:
   sudo pip install Flask

6. Start the server:
   python rest.py

At this point, you should have a server running at http://127.0.0.1:5000/
To make the server publicly available, use the --external argument:
   python rest.py --external



API DESCRIPTION

Data types
----------

User_JSON:
{
    "first_name": "<first_name>",
    "last_name": "<last_name>",
    "userid": "<userid>",
    "groups": ["<group_name_1>", "<group_name_2>", ...]
}

Group_User_Array:
["<userid1>", "<userid2", ...]

Group:
{
    "name": "<group_name>"
}


REST endpoints
--------------

GET /users/<userid>
returns User_JSON

Return codes:
200 OK
404 Not Found


POST /users
Payload: User_JSON

Return codes:
200 OK
409 Conflict (user already exists)
400 Bad Request (unknown group)


PUT /users/<userid>
Payload: User_JSON

Return codes:
200 OK
404 Not Found (user not found)
400 Bad Request (unknown group)


DELETE /users/<userid>

Return codes:
200 OK
404 Not Found (user not found)


GET /groups/<groupname>
returns Group_User_Array

Return codes:
200 OK
404 Not Found (group doesn't exist>


POST /groups
Payload: Group

Return codes:
200 OK
409 Conflict (group already exists)


PUT /groups/<groupname>
Payload: Group_User_Array

Return codes:
200 OK
404 Not Found (no such group)
400 Bad Request (unknown user)


DELETE /groups/<groupname>
200 OK
404 Not Found (no such group)