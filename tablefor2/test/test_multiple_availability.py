from django.test import TestCase

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command

import datetime
import pytz


class MatchMultipleAvailabilityTestCase(TestCase):
    mon = datetime.datetime(2030, 10, 21, 12, 0, tzinfo=pytz.UTC)
    tue = datetime.datetime(2030, 10, 22, 12, 0, tzinfo=pytz.UTC)
    wed = datetime.datetime(2030, 10, 23, 12, 0, tzinfo=pytz.UTC)

    profiles = {
        'christine': [datetime.datetime(2017, 7, 1), 'Engineering', 'MTW'],
        'jameson': [datetime.datetime(2017, 6, 1), 'Marketing', 'W'],
        'james': [datetime.datetime(2017, 5, 1), 'General & Administrative', 'T'],
        'shimin': [datetime.datetime(2017, 4, 1), 'Sales', 'MT'],
    }

    # setup
    def init_profiles(self):
        for name, profile_values in self.profiles.iteritems():
            Profile.objects.create(
                distinct_id=name,
                first_name=name,
                preferred_first_name=name,
                department=profile_values[1],
                email='%s@TEST-mixpanel.com' % (name),
                date_entered_mixpanel=profile_values[0],
                last_name='test',
                location='San Francisco',
                timezone='PST',
                google_hangout='Yes',
                match_type='one-on-one',
                frequency='Once a month',
                accept_matches='Yes'
            )

    def fresh_setup(self):
        self.init_profiles()
        for name, profile_values in self.profiles.iteritems():
            days = list(profile_values[2])
            for day in days:
                saved_day = ''
                if day == 'M':
                    saved_day = self.mon
                if day == 'T':
                    saved_day = self.tue
                if day == 'W':
                    saved_day = self.wed

                Availability.objects.create(
                    profile=Profile.objects.get(first_name=name),
                    time_available=saved_day,
                    time_available_utc=saved_day
                )

    def add_new(self):
        self.fresh_setup()

        Profile.objects.create(
            distinct_id='zara',
            first_name='zara',
            preferred_first_name='zara',
            department='Support',
            email='%s@TEST-mixpanel.com' % ('zara'),
            date_entered_mixpanel=datetime.datetime(2017, 7, 1),
            last_name='test',
            location='San Francisco',
            timezone='PST',
            google_hangout='Yes',
            match_type='one-on-one',
            frequency='Once a month',
            accept_matches='Yes'
        )

        Availability.objects.create(
            profile=Profile.objects.get(first_name='zara'),
            time_available=self.tue,
            time_available_utc=self.tue
        )

        christine = Profile.objects.get(first_name='christine')
        christine_mon = Availability.objects.get(profile=christine, time_available_utc=self.mon)
        christine_mon.matched_name = 'shimin test'
        christine_mon.save()

        shimin = Profile.objects.get(first_name='shimin')
        shimin_mon = Availability.objects.get(profile=shimin, time_available_utc=self.mon)
        shimin_mon.matched_name = 'christine test'
        shimin_mon.save()

    def test_new_multiple_availabilities(self):
        '''
        Christine & Shimin - M
        '''
        self.fresh_setup()
        christine = Profile.objects.get(first_name='christine')
        shimin = Profile.objects.get(first_name='shimin')

        christine_mon = Availability.objects.get(profile=christine, time_available_utc=self.mon)

        matches = [
            [christine_mon, christine, shimin]
        ]

        self.assertEqual(Command.run_one_on_one_matches(Command()), matches)

    def test_add_new(self):
        '''
        Zara & James - T
        '''
        self.add_new()
        zara = Profile.objects.get(first_name='zara')
        james = Profile.objects.get(first_name='james')

        zara_tue = Availability.objects.get(profile=zara, time_available_utc=self.tue)

        matches = [
            [zara_tue, zara, james]
        ]

        self.assertEqual(Command.run_one_on_one_matches(Command()), matches)
