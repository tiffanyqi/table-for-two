from __future__ import print_function
from django.core.management.base import BaseCommand

from apiclient import discovery
from datetime import timedelta
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from tablefor2.models import *

import datetime
import httplib2
import os
import pytz

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'calendar_secret.json'
APPLICATION_NAME = 'Table for 2'


class Command(BaseCommand):
    help = 'Matches users'
    '''
    Matching Process:
    - [ ] Runs this command at 3pm on all Availabilities that do not have
    a matched_name from tomorrow until a week from tomorrow.
    - [x] Prioritizes new Mixpanel hires.
    - [x] Check if they haven't been matched before
    - [x] Compares only users who have a different profile.department
    - [x] Checks same location first, else if both open to a google_hangout
    - [x] Ensure that the 1x/wk frequency has not yet been satisifed
    - [ ] (v2) Ensure that their chosen frequency has not yet been satisfied
    - [x] If two users finally fits all all of these criteria, we'll take
    the two Availability models and set the matched_name and matched_email
    - [x] Send a calendar invite to both parties
    '''

    def handle(self, *args, **options):
        today = datetime.datetime.utcnow().date()
        avs = Availability.objects.filter(time_available_utc__gte=today).order_by('time_available_utc', '-profile__date_entered_mixpanel')

        # dictionary of availability objects with datetime key
        future_availabilities = self.setup(avs)
        return self.runs_matches(future_availabilities)

    # actually runs the cron job, here for testing purposes
    def runs_matches(self, future_availabilities):
        matches = []
        # actually do the matching from here
        for timestamp, availability_list in future_availabilities.iteritems():
            rest_count = 0
            for av1 in availability_list:
                rest_count += 1
                for av2 in availability_list[rest_count:]:
                    profile1 = Profile.objects.get(email=av1.profile)
                    profile2 = Profile.objects.get(email=av2.profile)
                    if self.check_match(av1, av2, profile1, profile2):
                        self.match(av1, av2, profile1, profile2)
                        matches.append([timestamp, profile1, profile2])
        # sends hangouts to each group of matches
        for match in matches:
            self.send_google_calendar_invite(match[0], match[1], match[2])

        return matches

    # check to see that the two profiles should match
    def check_match(self, av1, av2, profile1, profile2):
        if self.check_frequency(av1, profile1) and self.check_frequency(av2, profile2):
            if self.check_not_currently_matched(av1) and self.check_not_currently_matched(av2):
                if self.check_previous_matches(profile1, profile2):
                    if self.check_departments(profile1, profile2):
                        return self.check_locations(profile1, profile2) or self.check_google_hangout(profile1, profile2)
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    # actually match the two
    def match(self, av1, av2, profile1, profile2):
        av1.matched_name = profile2.preferred_name + ' ' + profile2.last_name
        av1.matched_email = profile2.email
        av2.matched_name = profile1.preferred_name + ' ' + profile1.last_name
        av2.matched_email = profile1.email
        av1.save()
        av2.save()

    def send_google_calendar_invite(self, timestamp, profile1, profile2):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        start_time = datetime.datetime.fromtimestamp(timestamp)
        end_time = start_time + datetime.timedelta(minutes=30)

        event = {
            'summary': '%s // %s Table for 2' % (profile1.preferred_name, profile2.preferred_name),
            'description': 'Tablefor2!',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'attendees': [
                {'email': profile1.email},
                {'email': profile2.email},
                {'email': 'tiffany.qi+tf2test@mixpanel.com'}  # confirm it worked
            ],
        }

        print('Event created between %s and %s at %s' % (profile1.preferred_name, profile2.preferred_name, start_time))
        event = service.events().insert(calendarId='primary', body=event).execute()
        # event = service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()
        return event.get('id')

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
        previous_matches = avs.values_list('matched_email', flat=True)
        return profile2.email not in previous_matches

    # check to see that this availability is not matched yet
    def check_not_currently_matched(self, av):
        return av.matched_name is None

    # check to see that the frequency has not been matched yet, for now bsased on 1x/wk
    def check_frequency(self, av, profile):
        av_time = av.time_available_utc
        start_week = av_time - timedelta(days=av_time.weekday())
        end_week = start_week + timedelta(days=6)
        avs = Availability.objects.filter(profile=profile, time_available_utc__gte=start_week, time_available_utc__lte=end_week).exclude(matched_name=None)
        return not avs

    # sets up dictionary of timestamps to a list of availabilities
    def setup(self, avs):
        future_availabilities = {}
        for availability in avs:
            timestamp = (availability.time_available_utc-datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
            if timestamp in future_availabilities:
                future_availabilities[timestamp].append(availability)
            else:
                future_availabilities[timestamp] = [availability]
        return future_availabilities

    # taken from https://developers.google.com/google-apps/calendar/quickstart/python
    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'table-for-2.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
