from django.shortcuts import render
from django.http import HttpResponse
#built in django method to get a random STRING
from django.utils.crypto import get_random_string
#import main user model
from django.contrib.auth.models import User
#import randomstring model
from .models import randomstring
#import random module for random number
import random
#import bcrypt to check the submitted string
import bcrypt
#import datetime for datetime comparisons
from datetime import datetime, timedelta, timezone
#import restframework viewsets
from rest_framework import viewsets
#import restframework authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

#view for the rest framework
class string(APIView):
    #set this so only authenticated users can access
    permission_classes = (IsAuthenticated,)
    #define get request
    def get(self, request):
        #first we need to check if the user has already requested a string
        CurrentUser = User.objects.get(username=str(request.user.username))
        if not CurrentUser.randomstring_set.all():
            #user does not have a string, so lets create one
            randomnumber = random.randrange(8,32)
            random_string = get_random_string(randomnumber, 'abcdefghijklmnopqrstuvwxyz')
            randstr = randomstring(string=str(random_string), user=CurrentUser)
            randstr.save()
        #user has a string so we delete it an create a new one
        else:
            delete_string = CurrentUser.randomstring_set.get(string__iexact=str(CurrentUser.randomstring_set.all().first()))
            delete_string.delete()
            randomnumber = random.randrange(8,32)
            random_string = get_random_string(randomnumber, 'abcdefghijklmnopqrstuvwxyz')
            randstr = randomstring(string=str(random_string), user=CurrentUser)
            randstr.save()
        #save the encrypted string in finalstring variable witch gets passed on to the api
        finalstring = str(CurrentUser.randomstring_set.all().first())
        #finally return the content
        content = {'Random String:': finalstring}
        return Response(content)
    #define post request
    def post(self, request, format=None):
        #get the current string from users database
        CurrentUser = User.objects.get(username=str(request.user.username))
        #make sure that the user has actually requested a string or that the string is not expired
        if CurrentUser.randomstring_set.all():
            originalstring = CurrentUser.randomstring_set.all().first()
            #get created date for comparison and add 15 minutes for comparison purposes
            datecreated = originalstring.date_created + timedelta(minutes=15)
            #get todays time
            datenow = datetime.now(timezone.utc)
            #determine if string is expired by comparing the two datetimes
            if datenow < datecreated:
                #get the string from the submitted form and make sure it is properly encrypted
                originalstring = str(originalstring)
                #encode the string to bytes so bcrypt can work with it
                originalstring = originalstring.encode()
                #get hashed string from the post request
                hashedstring = request.data
                #get the string from json
                hashedstring = hashedstring["string"]
                #encode the string to bytes so bcrypt can work with it
                hashedstring = hashedstring.encode()
                #try and except to prevent django from displaying bcrypt error message
                try:
                    verifycrypt = bcrypt.checkpw(originalstring, hashedstring)
                except Exception:
                    verifycrypt = False
                    pass
                #verify the encryption
                if verifycrypt:
                    #after succesful verification, delete the string from the database
                    delete_string = CurrentUser.randomstring_set.get(string__iexact=str(CurrentUser.randomstring_set.all().first()))
                    delete_string.delete()
                    content = {"Response": "OK"}
                else:
                    #string not encrypted properly
                    content = {"Response": "NOK"}
            else:
                #string is expired return NOK
                content = {"Response": "NOK"}
        else:
            #user has not requested a string
            content = {"Response": "NOK"}
        return Response(content)
