#this testcase tries to verify a string that does exist, but "belongs" to another user

#import request so we can communicate with the API
import requests
#import bcrypt for encryption
import bcrypt

url = 'http://127.0.0.1:8000/string/'
#Add username and password here. Other users: testuser1 and testuser2, passwords: testing321
username = "testuser2"
password = "testing321"

string = "xvjndgjdgjdjg"

hashed = bcrypt.hashpw(string.encode('utf8'), bcrypt.gensalt())
#prepare the payload
headers = {'string': hashed}
r = requests.post(url, data=headers, auth=(username, password))
print(r.text)
