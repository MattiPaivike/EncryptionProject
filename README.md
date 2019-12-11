# EncryptionProject
Verify that your strings have been encrypted correctly through django restframework.

# Features
-The requested strings are stored inside a sqlite database.
-Only authenticated users can request new strings.
-Everytime a user requests a new string, the existing string is deleted from the database(if it exists).
-The user can verify that the string has been encrypted correctly.
-The user can only verify their own string.
-The original string in the database expires after 15 minutes.

# Requirements
Python 3

# How to setup
-Clone the repository to a local folder
-Make a python virtual environment in to the same folder: ("python -m venv .")
-Activate the python virtual environment: (on windows scripts\activate.bat)
-Install all requirements with pip: (pip install -r requirements.txt)
-Run Django Dev server: (navigate to \encryption and run "python manage.py runserver")

# Testing with "client" files
- Once everything is up and running you can run "client.py". The client requests a new string from the server, encrypts it with bcrypt and verifies that the string has been encrypted correctly
-testcase1.py tries to verify a string that does not exist in the database
-testcase2.py tries to verify a string that exists in the database, but "belongs" to another user.

# Manual testing notes
-The application has 3 users. testuser1, testuser2 and superuser. The password for all users is: testing321

-Getting the string from the API (python requests example):

import requests

url = 'http://127.0.0.1:8000/string/'
username = "testuser1"
password = "testing321"
r = requests.get(url, auth=(username, password))
print(r.text)

"{Random String: hfhasfjhfahfaha}"

-Encrypting and posting the same string (python requests example):

import requests
import bcrypt

string = hfhasfjhfahfaha}

hashed = bcrypt.hashpw(string.encode('utf8'), bcrypt.gensalt())

headers = {'string': hashed}
r = requests.post(url, data=headers, auth=(username, password)).json()
if r["Response"] == "OK":
    print("The string was verified as properly encrypted!")
