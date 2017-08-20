from django.test import TestCase

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command

import datetime
import pytz


class RecurringAvailabilityTest(TestCase):
    def setup_profiles(self):
        # tiffany, Success, SF, No, once a month
        Profile.objects.create(
            first_name='tiffany',
            last_name='qi',
            preferred_first_name='tiffany',
            email='tiffany@TEST-mixpanel.com',
            department='Success',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            frequency='Once a month',
            accept_matches='Yes',
            date_entered_mixpanel=datetime.datetime(2016, 10, 31),
            distinct_id='tiffany'
        )

    def setup_recurring(self):
        self.setup_profiles()
        RecurringAvailability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            day="0",  # mon
            time="1:00PM"
        )
        RecurringAvailability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            day="2",  # wed
            time="12:00PM"
        )
        RecurringAvailability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            day="4",  # fri
            time="10:00AM"
        )

    def test_create_availabilities(self):
        self.setup_recurring()
        t = Profile.objects.get(first_name='tiffany')
        av1 = Availability.objects.create(
            profile=t,
            time_available=datetime.datetime(2017, 8, 7, 13, 0, tzinfo=pytz.UTC),
            time_available_utc=datetime.datetime(2017, 8, 7, 20, 0, tzinfo=pytz.UTC),
        )
        av2 = Availability.objects.create(
            profile=t,
            time_available=datetime.datetime(2017, 8, 9, 12, 0, tzinfo=pytz.UTC),
            time_available_utc=datetime.datetime(2017, 8, 9, 19, 0, tzinfo=pytz.UTC),
        )
        av3 = Availability.objects.create(
            profile=t,
            time_available=datetime.datetime(2017, 8, 11, 10, 0, tzinfo=pytz.UTC),
            time_available_utc=datetime.datetime(2017, 8, 11, 17, 0, tzinfo=pytz.UTC),
        )
        today = datetime.datetime(2017, 8, 1)
        self.assertEqual([av1, av2, av3], Command.create_availabilities(Command(), today))

    def test_delete_availabilities(self):
        self.setup_recurring()
        t = Profile.objects.get(first_name='tiffany')
        RecurringAvailability.objects.get(profile=t, day="0", time="1:00PM").delete()
        av1 = Availability(
            profile=t,
            time_available=datetime.datetime(2017, 7, 24, 13, 0, tzinfo=pytz.UTC),
            time_available_utc=datetime.datetime(2017, 7, 24, 20, 0, tzinfo=pytz.UTC),
        )
        av2 = Availability(
            profile=t,
            time_available=datetime.datetime(2017, 7, 31, 13, 0, tzinfo=pytz.UTC),
            time_available_utc=datetime.datetime(2017, 7, 31, 20, 0, tzinfo=pytz.UTC),
        )
        today = datetime.datetime(2017, 7, 19)
        # self.assertEqual([av1, av2], Command.delete_availabilities(Command(), today))  # why not equal??
