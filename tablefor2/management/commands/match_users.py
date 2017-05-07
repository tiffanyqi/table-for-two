from django.core.management.base import BaseCommand

from tablefor2.models import *

import pytz
import time
import datetime


class Command(BaseCommand):
    help = 'Matches users'
    '''
    Matching Process:
    - [ ] Runs this command at 3pm on all Availabilities that do not have
    a matched_name from tomorrow until a week from tomorrow.
    - [x] Prioritizes new Mixpanel hires.
    - [x] Compares only users who have a different profile.department
    - [x] Matches the user if they are in the same location first, else
    will check whether they are both open to a google_hangout
    - [x] Check if they haven't been matched before
    - [ ] (V2) Ensure that the frequency has not yet been satisifed
    - [ ] If two users finally fits all all of these criteria, we'll take
    the two Availability models and set the matched_name and matched_email
    - [ ] Send a calendar invite to both parties
    '''

    def handle(self, *args, **options):
        today = datetime.date.today()
        avs = Availability.objects.filter(time_available__gte=today, matched_name=None).order_by('time_available', '-profile__date_entered_mixpanel')

        # dictionary of availability objects with datetime key
        future_availabilities = self.setup(avs)

        # actually do the matching from here
        for timestamp, availability_object in future_availabilities.iteritems():
            for availability in availability_object:
                print availability.profile

        print future_availabilities

    def match(self):
        print 'hi'

    # check to see that the departments aren't the same [TEST]
    def check_departments(self, profile1, profile2):
        return profile1.department != profile2.department

    # check to see that the google hangouts aren't the same [TEST]
    def check_google_hangout(self, profile1, profile2):
        return profile1.google_hangout == 'Yes' and profile2.google_hangout == 'Yes'

    # get all previous matches in list form from a profile and check they weren't there before [TEST]
    def check_previous_matches(self, profile1, profile2):
        today = datetime.date.today()
        avs = Availability.objects.filter(time_available__lte=today, profile=profile1).exclude(matched_name=None)
        previous_matches = avs.values('matched_email')
        return profile2.email not in previous_matches

    # sets up dictionary of timestamps to a list of availabilities
    def setup(self, avs):
        future_availabilities = {}
        for availability in avs:
            timestamp = (availability.time_available-datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
            if timestamp in future_availabilities:
                future_availabilities[timestamp].append(availability)
            else:
                future_availabilities[timestamp] = [availability]
        return future_availabilities
