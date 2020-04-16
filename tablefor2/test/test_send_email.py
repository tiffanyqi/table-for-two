import datetime

from django.test import TestCase

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command


class EmailTestCase(TestCase):
    now = datetime.datetime.now()

    def init_profiles(self):
        cherise = Profile.objects.create(
            first_name='Cherise',
            last_name='test',
            preferred_first_name='Cherise',
            email='cherise@TEST-mixpanel.com',
            department='Support',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            frequency=1,
            match_type='group',
            date_entered_mixpanel=datetime.datetime(2017, 8, 28),
            distinct_id='cherise'
        )
        Profile.objects.create(
            first_name='Rishi',
            last_name='test',
            preferred_first_name='Rishi',
            email='rishi@TEST-mixpanel.com',
            department='Support',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            frequency=1,
            match_type='group',
            date_entered_mixpanel=datetime.datetime(2019, 6, 3),
            distinct_id='rishi'
        )
        Availability.objects.create(
            profile=cherise,
            time_available=self.now,
            time_available_utc=self.now,
            matched_name='Rishi',
            matched_email='rishi@TEST-mixpanel.com',
        )

    def test_send_email(self):
        self.init_profiles()
        cherise = Profile.objects.get(first_name='Cherise')
        rishi = Profile.objects.get(first_name='Rishi')
        time = Availability.objects.get(time_available=self.now)
        profiles = [cherise, rishi]
        match_type = 'one-on-one'
        print("Email test sent, check your email and calendar to see if it worked!")
        Command.send_google_calendar_invite(Command(), time, profiles, match_type)
