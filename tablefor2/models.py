from django.contrib.auth.models import User
from django_unixdatetimefield import UnixDateTimeField
from django.db import models


class Profile(models.Model):
    first_name = models.CharField(null=True, max_length=50)
    last_name = models.CharField(null=True, max_length=50)
    email = models.CharField(null=True, max_length=50)
    division = models.CharField(null=True, max_length=50)
    location = models.CharField(null=True, max_length=50)
    ghangout = models.BooleanField(default=False)


class Availability(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    matched_name = models.CharField(null=True, max_length=50)
    matched_email = models.CharField(null=True, max_length=50)
    time_available = UnixDateTimeField()
