from django.contrib.auth.models import AbstractBaseUser, UserManager

from django.db import models
from django.utils import timezone


class Profile(AbstractBaseUser):
    first_name = models.CharField(null=True, max_length=50)
    last_name = models.CharField(null=True, max_length=50)
    email = models.CharField(null=True, max_length=50)

    USERNAME_FIELD = 'email'
    username = models.CharField(null=True, max_length=50)
    is_authenticated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    extra_saved_information = models.BooleanField(default=False)
    preferred_name = models.CharField(null=True, max_length=50)
    department = models.CharField(null=True, max_length=50)
    location = models.CharField(null=True, max_length=50)
    google_hangout = models.CharField(null=True, max_length=50)
    frequency = models.CharField(null=True, max_length=50)
    date_entered_mixpanel = models.DateField(default=timezone.now)

    objects = UserManager()

    def is_authenticated(self):
        return self.is_authenticated


class Availability(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    matched_name = models.CharField(null=True, max_length=50)
    matched_email = models.CharField(null=True, max_length=50)
    time_available = models.DateTimeField(default=timezone.now)
