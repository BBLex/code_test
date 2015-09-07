RUNNING THE SERVER
==================

Requirements:
- Python 2.7.6
- virtualenv:
  >sudo pip install virtualenv


Steps to run REST service:

1. Get the code:  
   >git clone https://github.com/BBLex/code_test.git

2. cd into 'code_test':  
   >cd code_test

3. Create a virtual environment:  
   >virtualenv venv

4. Activate the virtual environment:  
   >. venv/bin/activate

5. Install Flask in the virtual environment:  
   >pip install Flask

6. Start the server:  
   >python rest.py

At this point, you should have a server running at http://127.0.0.1:5000/

To make the server publicly available, use the --external argument:  
>python rest.py --external


RUNNING THE TESTS
=================
To run unit tests for the database (includes business logic):  
>python user_group_db_test.py

To run unit tests for the REST API:  
>python rest_unit_test.py

To run integration tests:
>python planet_test.py


API DESCRIPTION
================

Data types
----------
```
User:
{
    "first_name": "<first_name>",
    "last_name": "<last_name>",
    "userid": "<userid>",
    "groups": ["<group_name_1>", "<group_name_2>", ...]
}
```
```
Group_User_Array:
["<userid1>", "<userid2>", ...]
```
```
Group:
{
    "name": "<group_name>"
}
```

REST endpoints
--------------
```
GET /users/<userid>
returns User

Return codes:
200 OK
404 Not Found
```
```
POST /users
Payload: User

Return codes:
200 OK
409 Conflict (user already exists)
400 Bad Request (unknown group)
```
```
PUT /users/<userid>
Payload: User

Return codes:
200 OK
404 Not Found (user not found)
400 Bad Request (unknown group)
```
```
DELETE /users/<userid>

Return codes:
200 OK
404 Not Found (user not found)
```
```
GET /groups/<groupname>
returns Group_User_Array

Return codes:
200 OK
404 Not Found (group doesn't exist>
```
```
POST /groups
Payload: Group

Return codes:
200 OK
409 Conflict (group already exists)
```
```
PUT /groups/<groupname>
Payload: Group_User_Array

Return codes:
200 OK
404 Not Found (no such group)
400 Bad Request (unknown user)
```
```
DELETE /groups/<groupname>

Return codes:
200 OK
404 Not Found (no such group)
```
