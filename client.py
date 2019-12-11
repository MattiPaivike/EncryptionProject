#import request so we can communicate with the API
import requests
#import bcrypt for encryption
import bcrypt

url = 'http://127.0.0.1:8000/string/'
#Add username and password here. Other users: testuser1 and testuser2, passwords: testing321
username = "testuser1"
password = "testing321"
#make the request
r = requests.get(url, auth=(username, password)).json()
print("Succesfully requested new random string:" + r["Random String:"])
#get string from json
string = r["Random String:"]
#encrypt the string with bcrypt
print("Encrypting the string with bcrypt...")
hashed = bcrypt.hashpw(string.encode('utf8'), bcrypt.gensalt())
#prepare the payload
headers = {'string': hashed}
r = requests.post(url, data=headers, auth=(username, password)).json()
if r["Response"] == "OK":
    print("The string was verified as properly encrypted!")
else:
    print("The string was NOT properly encrypted, or the string has expired or it has been deleted")
