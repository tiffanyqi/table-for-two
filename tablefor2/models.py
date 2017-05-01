# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django_unixdatetimefield import UnixDateTimeField
from django.db import models
from django.utils import timezone


class Profile(AbstractBaseUser):
    # user = models.OneToOneField(User)
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

    division = models.CharField(null=True, max_length=50)
    location = models.CharField(null=True, max_length=50)
    ghangout = models.BooleanField(default=False)

    objects = UserManager()

    def is_authenticated(self):
        return self.is_authenticated


class Availability(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    matched_name = models.CharField(null=True, max_length=50)
    matched_email = models.CharField(null=True, max_length=50)
    time_available = UnixDateTimeField()
