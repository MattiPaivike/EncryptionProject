from encrypt.models import randomstring
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
#import datetime for datetime comparisons
from datetime import datetime, timedelta, timezone

class Command(BaseCommand):
    def handle(self, *args, **options):
        #get all random strings
        randomstrings = randomstring.objects.all()

        #parse all random strings and see if they have expired
        for string in randomstrings:
            datecreated = string.date_created + timedelta(minutes=15)
            datenow = datetime.now(timezone.utc)
            #compare strings and delete
            if datenow > datecreated:
                string.delete()
