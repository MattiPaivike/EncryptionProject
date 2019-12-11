#this testcase tries to verify a string that does not exist

#import request so we can communicate with the API
import requests

url = 'http://127.0.0.1:8000/string/'
#Add username and password here. Other users: testuser1 and testuser2, passwords: testing321
username = "testuser1"
password = "testing321"

headers = {'string': "asdadsasdasdasdasdasddas"}
r = requests.post(url, data=headers, auth=(username, password))
print(r.text)
