from __future__ import print_function
from django.core.management.base import BaseCommand

from tablefor2.models import Profile
from tablefor2.settings import MP_TOKEN


mp = Mixpanel(MP_TOKEN)

class Command(BaseCommand):
    """
    Effort to change frequency to conditional frequency per month
    0 = not accepting matches
    1 = once per month, which was the default in the old way of doing things
    """
    def handle(self, *args, **options):
        profiles = Profile.objects.all()
        for profile in profiles:
            if profile.accept_matches == 'Yes':
                profile.frequency = 1
            else:
                profile.frequency = 0
            profile.save()
            mp.people_set(profile.distinct_id, {'Frequency': profile.frequency})
