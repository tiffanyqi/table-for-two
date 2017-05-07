from django.core.management.base import BaseCommand

from tablefor2.models import *

import pytz
import datetime


class Command(BaseCommand):
    help = 'Matches users'
    '''
    Matching Process:
    - [ ] Runs this command at 3pm on all Availabilities that do not have
    a matched_name from tomorrow until a week from tomorrow.
    - [x] Prioritizes new Mixpanel hires.
    - [ ] Check if they haven't been matched before
    - [x] Compares only users who have a different profile.department
    - [x] Checks same location first, else if both open to a google_hangout
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
        for timestamp, availability_list in future_availabilities.iteritems():
            rest_count = 0
            for av1 in availability_list:
                rest_count += 1
                for av2 in availability_list[rest_count:]:
                    profile1 = Profile.objects.get(email=av1.profile)
                    profile2 = Profile.objects.get(email=av2.profile)
                    if self.check_match(profile1, profile2):
                        self.match(av1, av2, profile1, profile2)

        # print Availability.objects.all().values()

    # actually match the two [TESt]
    def match(self, av1, av2, profile1, profile2):
        print av1.matched_name
        print av2.matched_name
        av1.matched_name = profile2.preferred_name + ' ' + profile2.last_name
        av1.matched_email = profile2.email
        av2.matched_name = profile1.preferred_name + ' ' + profile1.last_name
        av2.matched_email = profile1.email
        av1.save()
        av2.save()
        print '--'

    # check to see that the two profiles should match [TEST]
    def check_match(self, profile1, profile2):
        if self.check_previous_matches(profile1, profile2):
            if self.check_departments(profile1, profile2):
                return self.check_locations(profile1, profile2) or self.google_hangout(profile1, profile2)
            else:
                return False
        else:
            return False

    # check to see that the google hangouts aren't the same
    def check_google_hangout(self, profile1, profile2):
        return profile1.google_hangout == 'Yes' and profile2.google_hangout == 'Yes'

    # check to see that they're in the same place
    def check_locations(self, profile1, profile2):
        return profile1.location == profile2.location and profile1.location is not 'Other'

    # check to see that the departments aren't the same
    def check_departments(self, profile1, profile2):
        return profile1.department != profile2.department

    # get all previous matches in list form from a profile and check they weren't there before [TEST]
    def check_previous_matches(self, profile1, profile2):
        avs = Availability.objects.filter(profile=profile1).exclude(matched_name=None)
        previous_matches = avs.values('matched_email')
        return profile2.email not in previous_matches

    # sets up dictionary of timestamps to a list of availabilities [TEST]
    def setup(self, avs):
        future_availabilities = {}
        for availability in avs:
            timestamp = (availability.time_available-datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
            if timestamp in future_availabilities:
                future_availabilities[timestamp].append(availability)
            else:
                future_availabilities[timestamp] = [availability]
        return future_availabilities
