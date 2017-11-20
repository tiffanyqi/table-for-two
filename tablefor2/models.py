from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
from django.utils import timezone


class Profile(AbstractBaseUser):
    first_name = models.CharField(null=True, max_length=50)
    last_name = models.CharField(null=True, max_length=50)
    preferred_first_name = models.CharField(null=True, max_length=50)
    email = models.CharField(null=True, max_length=50)
    distinct_id = models.CharField(null=True, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    username = models.CharField(null=True, max_length=50)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    extra_saved_information = models.BooleanField(default=False)
    department = models.CharField(null=True, max_length=50)
    location = models.CharField(null=True, max_length=50)
    timezone = models.CharField(null=True, max_length=50)
    google_hangout = models.CharField(null=True, max_length=50)
    frequency = models.CharField(null=True, max_length=50)
    number_of_matches = models.IntegerField(default=0)
    date_entered_mixpanel = models.DateField(null=True)

    picture_url = models.CharField(null=True, max_length=255)
    what_is_your_favorite_animal = models.CharField(null=True, max_length=50)
    name_a_fun_fact_about_yourself = models.CharField(null=True, max_length=50)
    accept_matches = models.CharField(null=True, max_length=50)

    objects = UserManager()

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name


class RecurringAvailability(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    day = models.CharField(null=True, max_length=50)
    time = models.CharField(null=True, max_length=50)


class Availability(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    matched_name = models.CharField(null=True, max_length=50)
    matched_email = models.CharField(null=True, max_length=50)
    time_available = models.DateTimeField(default=timezone.now)
    time_available_utc = models.DateTimeField(default=timezone.now)
    picture_url = models.CharField(null=True, max_length=255)
    what_is_your_favorite_animal = models.CharField(null=True, max_length=50)
    name_a_fun_fact_about_yourself = models.CharField(null=True, max_length=50)
    department = models.CharField(null=True, max_length=50)
    timezone = models.CharField(null=True, max_length=50)
    google_hangout = models.CharField(null=True, max_length=50)
