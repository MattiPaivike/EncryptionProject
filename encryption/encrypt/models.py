from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class randomstring(models.Model):
    string = models.CharField(max_length=32)
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #return the string for our queries
    def __str__(self):
        return self.string
