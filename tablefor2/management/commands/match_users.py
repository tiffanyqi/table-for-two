from __future__ import print_function
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from apiclient import discovery
from datetime import timedelta
from oauth2client import client, tools
from oauth2client.file import Storage

from mixpanel import Mixpanel

from tablefor2.helpers import calculate_utc, determine_ampm, get_next_weekday
from tablefor2.models import *
from tablefor2.settings import MATCHING_KEY, MATCHING_SECRET, MP_TOKEN

import datetime
import httplib2
import os

try:
    import argparse
    flags = tools.argparser.parse_args([])
    # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/X.json
APPLICATION_NAME = 'Table for 2'
mp = Mixpanel(MP_TOKEN)


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
    - [x] Ensure that the 1x/mo frequency has not yet been satisifed
    - [ ] (v2) Ensure that their chosen frequency has not yet been satisfied
    - [x] If two users finally fits all of these criteria, we'll take the two
    Availability models and set the matched_name and matched_email
    - [x] Send a calendar invite to both parties
    '''

    def handle(self, *args, **options):
        today = datetime.datetime.utcnow().date()
        self.delete_availabilities(today)
        self.create_availabilities(today)
        return self.runs_matches()

    # creates availabilities from recurring availabilities
    def create_availabilities(self, today):
        availabilities = []
        recurrings = RecurringAvailability.objects.all()
        for rec_av in recurrings:
            if rec_av.profile.accept_matches == "Yes":
                day = rec_av.day  # num of week
                time = determine_ampm(rec_av.time)  # HH:MM, miltary
                time_available = get_next_weekday(today, day, time)
                utc = calculate_utc(rec_av.profile, time_available)
                try:
                    av = Availability.objects.get(profile=rec_av.profile, time_available=time_available, time_available_utc=utc)
                except:
                    av = Availability(profile=rec_av.profile, time_available=time_available, time_available_utc=utc)
                    av.save()
                availabilities.append(av)
        return availabilities

    # delete availabilities that were there before but not in recurrings anymore
    def delete_availabilities(self, today):
        availabilities = Availability.objects.filter(time_available_utc__gte=today)
        for av in availabilities:
            profile = av.profile
            day = av.time_available.weekday()
            time = av.time_available.strftime("%-I:%M%p")

            try:
                RecurringAvailability.objects.get(profile=profile, day=day, time=time)
            except:
                print('deleted %s' % profile)
                av.delete()

    # actually runs the cron job, goes through new profiles and old profiles and sees
    # if the availabilities match at all
    def runs_matches(self):
        matches = []
        today = datetime.datetime.utcnow().date()

        # iterate through all profiles regardless of availability
        for new_profile in Profile.objects.filter(accept_matches='Yes').order_by('-date_entered_mixpanel'):
            new_profile_availabilities = Availability.objects.filter(profile=new_profile, time_available_utc__gte=today)
            for old_profile in Profile.objects.filter(accept_matches='Yes', date_entered_mixpanel__lt=new_profile.date_entered_mixpanel).order_by('date_entered_mixpanel'):
                old_profile_availabilities = Availability.objects.filter(profile=old_profile, time_available_utc__gte=today)

                # check each av in the profile
                for new_availability in new_profile_availabilities:
                    for old_availability in old_profile_availabilities:
                        if new_availability.time_available_utc == old_availability.time_available_utc:

                            # actually do the checking from here
                            if self.check_match(new_availability, old_availability, new_profile, old_profile):
                                self.match(new_availability, old_availability, new_profile, old_profile)
                                self.match(old_availability, new_availability, old_profile, new_profile)
                                matches.append([new_availability, new_profile, old_profile])

        # sends hangouts to each group of matches
        for match in matches:
            self.send_google_calendar_invite(match[0], match[1], match[2])

        return matches

    # check to see that the two profiles should match
    def check_match(self, av1, av2, profile1, profile2):
        if self.check_accept_matches(profile1, profile2) and self.check_frequency(av1, profile1) and self.check_frequency(av2, profile2) and self.check_not_currently_matched(av1) and self.check_not_currently_matched(av2) and self.check_previous_matches(profile1, profile2) and self.check_departments(profile1, profile2):
            return self.check_locations(profile1, profile2) or self.check_google_hangout(profile1, profile2)
        return False

    # actually match the two
    def match(self, orig_av, matched_av, original_profile, matched_profile):
        orig_av.matched_name = matched_profile.preferred_first_name + ' ' + matched_profile.last_name
        orig_av.matched_email = matched_profile.email
        orig_av.picture_url = matched_profile.picture_url
        orig_av.what_is_your_favorite_animal = matched_profile.what_is_your_favorite_animal
        orig_av.name_a_fun_fact_about_yourself = matched_profile.name_a_fun_fact_about_yourself
        orig_av.department = matched_profile.department
        orig_av.timezone = matched_profile.timezone
        original_profile.number_of_matches += 1

        if original_profile.location == matched_profile.location:
            orig_av.google_hangout = matched_av.google_hangout = "in person"
        else:
            orig_av.google_hangout = matched_av.google_hangout = "Google Hangout"

        orig_av.save()
        original_profile.save()
        self.execute_mixpanel_matches(orig_av, original_profile, matched_profile)

    def send_google_calendar_invite(self, availability, profile1, profile2):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        start_time = availability.time_available_utc
        end_time = start_time + datetime.timedelta(minutes=30)
        description = "You are now matched for a Table for Two session! The session lasts how ever long you'd like, and you can meet "
        description += "wherever you want. If you're on Google Hangout, please use the hangout link located in this event. If something "
        description += "comes up and you are unable to make the session, you are welcome to reschedule to a different time--don't be afraid "
        description += "to reach out to them over Slack! If you have any questions, don't hesitate to Slack Tiffany Qi or Kate Ryan. Have fun!"

        event = {
            'summary': '%s // %s Table for Two via %s' % (profile1.preferred_first_name, profile2.preferred_first_name, availability.google_hangout),
            'description': description,
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
            "guestsCanModify": True
        }

        print('Event created between %s and %s at %s' % (profile1.preferred_first_name, profile2.preferred_first_name, start_time))
        # event = service.events().insert(calendarId='primary', body=event).execute()
        event = service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()
        self.execute_mixpanel_calendar_invite(profile1, start_time)
        self.execute_mixpanel_calendar_invite(profile2, start_time)

    ### Helpers ###

    # check to see that the profiles can accept matches
    def check_accept_matches(self, profile1, profile2):
        return profile1.accept_matches == 'Yes' and profile1.accept_matches == profile2.accept_matches

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
        return profile2.email not in previous_matches and profile1.email != profile2.email

    # check to see that this availability is not matched yet
    def check_not_currently_matched(self, av):
        return av.matched_name is None

    # check to see that the frequency has not been matched yet, for now based on 1x/mo
    def check_frequency(self, av, profile):
        av_time = av.time_available_utc
        try:
            last_matched_av = Availability.objects.filter(profile=profile).exclude(matched_name=None).latest('time_available_utc')
            # compare the time between the last accepted av and this av
            days_between = abs((av_time - last_matched_av.time_available_utc).days)
            return days_between >= 28

        except ObjectDoesNotExist:  # if no latest_matched_av, it'll be true for sure
            return True

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
            flow = client.OAuth2WebServerFlow(client_id=MATCHING_KEY,
                                              client_secret=MATCHING_SECRET,
                                              scope='https://www.googleapis.com/auth/calendar',
                                              redirect_uris='http://localhost, https://tablefortwo.herokuapp, http://tablefortwo.herokuapp')

            flow.user_agent = APPLICATION_NAME
            if flags:
                flags.noauth_local_webserver = True
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    # execute mixpanel things related to matches
    def execute_mixpanel_matches(self, orig_av, original_profile, matched_profile):
        mp.track(original_profile.distinct_id, 'Match Created', {
            'Current User Department': original_profile.department,
            'Current User Location': original_profile.location,
            'Other User Department': matched_profile.department,
            'Other User Location': matched_profile.location,
            'Google Hangout or In Person': orig_av.google_hangout,
        })
        mp.people_set(original_profile.distinct_id, {
            'Number of Matches': original_profile.number_of_matches,
            'Last Match Created': datetime.datetime.utcnow()
        })

    # execute mixpanel things related to calendar invite
    def execute_mixpanel_calendar_invite(self, profile, start_time):
        mp.track(profile.distinct_id, 'Calendar Invite Sent', {
            'Meeting Time': start_time.isoformat(),
            'Timezone': profile.timezone
        })
