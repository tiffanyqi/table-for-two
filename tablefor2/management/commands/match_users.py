from __future__ import print_function
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from apiclient import discovery
import datetime
import httplib2
import json
from mixpanel import Mixpanel
from oauth2client import client, tools
from oauth2client.file import Storage
import os
from slackclient import SlackClient

from tablefor2.app_helpers import calculate_utc
from tablefor2.helpers import determine_ampm, get_next_weekday
from tablefor2.models import (
    Availability,
    GroupAvailability,
    Profile,
    RecurringAvailability
)
from tablefor2.settings import (
    MATCHING_KEY,
    MATCHING_SECRET,
    MP_TOKEN,
    SLACK_TOKEN
)


try:
    import argparse
    flags = tools.argparser.parse_args([])
    # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/X.json
APPLICATION_NAME = 'Table for 2'
# ensure in sync with forms.py
locations = ['San Francisco', 'New York', 'Seattle', 'Austin', 'London', 'Paris', 'Barcelona', 'Singapore', 'Other']
mp = Mixpanel(MP_TOKEN)


class Command(BaseCommand):
    help = 'Matches users'
    """
    Matching Process:
    - [ ] Runs this command at 3pm on all Availabilities that do not have
    a matched_name from tomorrow until a week from tomorrow.
    - [x] Prioritizes new Mixpanel hires.
    - [x] Checks to see if they're a valid Mixpanel user
    - [x] Check if they haven't been matched before
    - [x] Compares only users who have a different profile.department
    - [x] Checks same location first, else if both open to a google_hangout
    - [x] Ensure that the 1x/mo frequency has not yet been satisifed
    - [x] (v2) Ensure that their chosen frequency has not yet been satisfied
    - [x] If two users finally fits all of these criteria, we'll take the two
    Availability models and set the matched_name and matched_email
    - [x] Send a calendar invite to both parties
    """

    def handle(self, *args, **options):
        employees = self.get_employees()	
        self.check_profiles(employees)
        today = datetime.datetime.utcnow().date()
        self.delete_availabilities(today)
        self.create_availabilities(today)
        return self.runs_matches()

    def get_employees(self):	
        """	
        Get a list of all employees from Slack	
        """	
        sc = SlackClient(SLACK_TOKEN)
        slack_users = sc.api_call('users.list')['members']
        current_directory = {}	
        for employee in slack_users:
            if not employee['deleted'] and not employee['is_bot'] and not employee['id'] == 'USLACKBOT' and not employee['is_restricted']:
                profile = employee.get('profile')
                if 'email' in profile.keys():
                    current_directory[profile['email']] = {	
                        'slack_id': employee['id']
                    }
        return current_directory		

    def check_profiles(self, employees):	
        """	
        Checks to see if the matching profiles are valid employees, otherwise	
        set to not accepting matches	
        """	
        for profile in Profile.objects.filter(frequency__gt=0):	
            try:	
                employees[profile.email]	
            except KeyError:	
                profile.frequency = 0	
                profile.save()
                mp.people_set(original_profile.distinct_id, {'Accepting Matches': 'No', 'Frequency': 0})
                print('Deactivated ' + profile.email)

    def create_availabilities(self, today):
        """
        Creates availabilities from recurring availabilities
        Returns all created availabilities
        """
        availabilities = []
        recurrings = RecurringAvailability.objects.all()
        for rec_av in recurrings:
            if rec_av.profile.frequency > 0:
                day = rec_av.day  # num of week
                time = determine_ampm(rec_av.time)  # HH:MM, miltary
                time_available = get_next_weekday(today, day, time)
                utc = calculate_utc(rec_av.profile, time_available)
                if rec_av.profile.match_type == 'one-on-one':
                    try:
                        av = Availability.objects.get(profile=rec_av.profile, time_available=time_available, time_available_utc=utc)
                    except:
                        av = Availability(profile=rec_av.profile, time_available=time_available, time_available_utc=utc)
                        av.save()
                else:
                    if rec_av.time == '12PM':
                        try:
                            av = GroupAvailability.objects.get(profile=rec_av.profile, time_available=time_available, time_available_utc=utc)
                        except:
                            av = GroupAvailability(profile=rec_av.profile, time_available=time_available, time_available_utc=utc)
                            av.save()
                availabilities.append(av)
        print(Availability.objects.filter(time_available__gte=today).count(), ' created')
        return availabilities

    def delete_availabilities(self, today):
        """
        Deletes:
            - excess availabilities that were there but not in recurrings anymore
            - delete those who should be OOO via time off or holidays
            - past availabilities with no matches
        Returns future availabilities
        """
        future_availabilities = Availability.objects.filter(time_available_utc__gte=today)
        for av in future_availabilities:
            profile = av.profile
            self.delete_av_from_recurring(profile, av)

        # prevent excess rows from being generated for heroku
        old_availabilities = Availability.objects.filter(time_available_utc__lt=today, matched_name=None)
        old_group_availabilities = GroupAvailability.objects.filter(time_available_utc__lt=today, matched_group_users=None)
        print('deleted ', old_availabilities.count() + old_group_availabilities.count())
        old_availabilities.delete()
        old_group_availabilities.dekete()
        return future_availabilities

    def runs_matches(self):
        """
        Actually runs the cron job, 
        """
        self.run_one_on_one_matches()
        self.run_group_matches()

    def run_one_on_one_matches(self):
        """
        goes through new profiles and old profiles and sees if the availabilities match at all
        Returns all matches
        """
        today = datetime.datetime.utcnow().date()
        matches = []
        # iterate through all profiles regardless of availability
        for new_profile in Profile.objects.filter(match_type='one-on-one', frequency__gt=0).order_by('-date_entered_mixpanel'):
            new_profile_availabilities = Availability.objects.filter(profile=new_profile, time_available_utc__gte=today)
            for old_profile in Profile.objects.filter(frequency__gt=0, date_entered_mixpanel__lt=new_profile.date_entered_mixpanel).order_by('date_entered_mixpanel'):
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
        # match the users
        for match in matches:
            self.send_google_calendar_invite(match[0], [match[1], match[2]], 'one-on-one')

        return matches

    def run_group_matches(self):
        """
        groups users by location and availability first and outputs the group matches
        """
        today = datetime.datetime.utcnow().date()
        group_matches = {}
        for location in locations:
            # assuming these are all lunchtime avs from av creation
            in_progress_matched_profiles = []
            for av in GroupAvailability.objects.filter(profile__location=location, time_available_utc__gte=today, profile__frequency__gt=0):
                if (self.check_fuzzy_match(av.profile, av, in_progress_matched_profiles)):
                    in_progress_matched_profiles.append(av.profile)
                if len(in_progress_matched_profiles) == 4:
                    group_matches[av.time_available_utc] = in_progress_matched_profiles  
                    self.match_group(av.time_available_utc, in_progress_matched_profiles)
                    in_progress_matched_profiles = []

        # send the invites
        for time, matches in group_matches.items():
            self.send_google_calendar_invite(time, matches, 'group')

        return group_matches

    # check to see that the two profiles should match
    def check_match(self, av1, av2, profile1, profile2):
        """
        Checks to see that the two profiles actually match
        Returns a boolean of whether the two profiles are matched
        """
        if self.check_frequency(av1, profile1) and self.check_frequency(av2, profile2) and self.check_not_currently_matched(av1) and self.check_not_currently_matched(av2) and self.check_previous_matches(profile1, profile2) and self.check_departments(profile1, profile2):
            return self.check_locations(profile1, profile2) or self.check_google_hangout(profile1, profile2)
        return False

    # check to see if user is different enough from the others of the group
    def check_fuzzy_match(self, profile, av, group):
        """
        Returns a boolean of whether the user can join the group
        """
        # TODO: implement checking seniority, for now hope it just works out
        if self.check_frequency(av, profile) and self.check_not_currently_matched(av):
            return len(group) == 0 or (self.check_fuzzy_previous_matches(profile, group) and self.check_fuzzy_departments(profile, group))
        return False

    def match(self, orig_av, matched_av, original_profile, matched_profile):
        """
        Matches the two
        """
        orig_av.matched_name = matched_profile.preferred_first_name + ' ' + matched_profile.last_name
        orig_av.matched_email = matched_profile.email
        orig_av.picture_url = matched_profile.picture_url
        orig_av.what_is_your_favorite_movie = matched_profile.what_is_your_favorite_movie
        orig_av.name_a_fun_fact_about_yourself = matched_profile.name_a_fun_fact_about_yourself
        orig_av.department = matched_profile.department
        orig_av.timezone = matched_profile.timezone
        original_profile.number_of_matches += 1

        if original_profile.location == matched_profile.location:
            orig_av.google_hangout = matched_av.google_hangout = 'in person'
        else:
            orig_av.google_hangout = matched_av.google_hangout = 'video call'

        orig_av.save()
        original_profile.save()
        self.execute_mixpanel_one_on_one_matches(orig_av, original_profile, matched_profile)

    def match_group(self, time, matches):
        """
        Creates a group and matches each av profile with the group
        """
        emails = [prof.email for prof in matches]
        for prof in matches:
            av = GroupAvailability.objects.get(time_available_utc=time, profile=prof)
            av.matched_group_users = json.dumps(emails)
            av.save()
            prof.number_of_matches += 1
            prof.save()
            self.execute_mixpanel_group_matches(prof)

    def send_google_calendar_invite(self, time, profiles, match_type):
        """
        Sends the calendar invite to the newly matched profiles
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        start_time = time if match_type == 'group' else time.time_available_utc
        end_time = start_time + datetime.timedelta(minutes=30)
        description = "You are now matched for a Table for Two session! The session lasts how ever long you'd like, and you can meet "
        description += "wherever you want. If you're on Google Hangout, please use the hangout link located in this event. If something "
        description += "comes up and you are unable to make the session, you are welcome to reschedule to a different time--don't be afraid "
        description += "to reach out to them over Slack! If you have any questions, don't hesitate to Slack Tiffany Qi or Kate Ryan. Have fun! "
        description += "You can opt out of table for 2 by going to tablefortwo.herokuapp.com."

        event = {
            'summary': 'Table for Two ({})'.format(match_type),
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'attendees': [{'email': profile.email} for profile in profiles],
            "guestsCanModify": True
        }

        print('{} event created with {} at {}'.format(match_type, [p.email for p in profiles], start_time))
        # event = service.events().insert(calendarId='primary', body=event).execute()
        event = service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()
        self.execute_mixpanel_calendar_invite(profiles, start_time)

    ### Helpers ###

    def check_google_hangout(self, profile1, profile2):
        """
        Check to see that the google hangout (video call) prefs are both "yes"
        Returns a boolean
        """
        return profile1.google_hangout == 'Yes' and profile2.google_hangout == 'Yes'

    def check_locations(self, profile1, profile2):
        """
        Check to see that the profiles are in the same location
        Returns a boolean
        """
        return profile1.location == profile2.location and profile1.location is not 'Other'
    
    def check_departments(self, profile1, profile2):
        """
        Check to see that the profiles aren't the same department
        Returns a boolean
        """
        return profile1.department != profile2.department

    def check_fuzzy_departments(self, profile, group):
        """
        Check to see that the group has one or fewer of the same department as the profile
        Returns a boolean
        """
        departments = {}
        for prof in group:
            if prof.department in departments:
                departments[prof.department] += 1
            else:
                departments[prof.department] = 1
        return profile.department not in departments or departments[profile.department] < 2

    def check_previous_matches(self, profile1, profile2):
        """
        Get all previous matches in list form from a profile and check
        they weren't there before
        Returns a boolean
        """
        avs = Availability.objects.filter(profile=profile1).exclude(matched_name=None)
        previous_matches = avs.values_list('matched_email', flat=True)
        return profile2.email not in previous_matches and profile1.email != profile2.email

    def check_fuzzy_previous_matches(self, profile, group):
        """
        Check to see that the profile has not met more than one person of the group before
        Returns a boolean
        """
        emails = [prof.email for prof in group]
        avs = GroupAvailability.objects.filter(profile=profile).exclude(matched_group_users=None)
        previous_matches = list(avs.values_list('matched_group_users', flat=True))
        flat_matches = [item for sublist in previous_matches for item in json.loads(sublist)]
        intersection = [value for value in emails if value in flat_matches]
        return len(intersection) < 2

    def check_not_currently_matched(self, av):
        """
        Check to see that the availability is not matched yet
        Returns a boolean
        """
        return ((av.profile.match_type == 'one-on-one' and av.matched_name is None)
            or (av.profile.match_type == 'group' and av.matched_group_users is None))

    def check_frequency(self, av, profile):
        """
        Check to see that the frequency has not been matched yet
        This one is once a month, but will change later
        Returns a boolean
        """
        av_time = av.time_available_utc
        try:
            if profile.match_type == 'one-on-one':
                last_matched_av = Availability.objects.filter(profile=profile).exclude(matched_name=None).latest('time_available_utc')
            else:
                last_matched_av = GroupAvailability.objects.filter(profile=profile).exclude(matched_group_users=None).latest('time_available_utc')
            # compare the time between the last accepted av and this av
            days_between = abs((av_time - last_matched_av.time_available_utc).days)
            day_limit = 35 - 7 * int(profile.frequency)  # max is 28 days, which is once per month
            return days_between >= day_limit

        except ObjectDoesNotExist:  # if no latest_matched_av, it'll be true for sure
            return True

    def delete_av_from_recurring(self, profile, av):
        """
        Delete the availability if recurring isn't there
        Returns a boolean, True is deleted
        """
        day = av.time_available.weekday()
        time = av.time_available.strftime("%-I:%M%p")
        result = False
        try:
            RecurringAvailability.objects.get(profile=profile, day=day, time=time)
        except ObjectDoesNotExist:
            print('deleted avs from %s' % profile)
            av.delete()
            result = True
        return result

    def check_av_deleted(self, av, date, key, name, time_off):
        """
        Checks whether the availability is in the specified time period
        Returns a boolean
        """
        start = datetime.datetime.strptime(time_off[key][name]['start'], '%Y-%m-%d')
        end = datetime.datetime.strptime(time_off[key][name]['end'], '%Y-%m-%d')
        return start <= date <= end

    def get_credentials(self):
        """
        Taken from: taken from https://developers.google.com/google-apps/calendar/quickstart/python
        Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns credentials, the obtained credential.
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

    def execute_mixpanel_one_on_one_matches(self, orig_av, original_profile, matched_profile):
        """
        Execute Mixpanel code from matches
        """
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
    
    def execute_mixpanel_group_matches(self, profile):
        """
        Execute Mixpanel code from group matches
        """
        mp.track(profile.distinct_id, 'Match Created', {
            'Current User Department': profile.department,
            'Current User Location': profile.location,
            'Type': 'Group',
        })
        mp.people_set(profile.distinct_id, {
            'Number of Matches': profile.number_of_matches,
            'Last Match Created': datetime.datetime.utcnow()
        })

    def execute_mixpanel_calendar_invite(self, profiles, start_time):
        """
        Execute Mixpanel code from calendar invites
        """
        for prof in profiles:
            mp.track(profile.distinct_id, 'Calendar Invite Sent', {
                'Meeting Time': start_time.isoformat(),
                'Timezone': profile.timezone
            })
