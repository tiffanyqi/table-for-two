from django.test import TestCase

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command

import datetime
import pytz


class MatchTestCase(TestCase):
    time_off = {
        'timeOff': {
            'tiffany test': {
                'start': "2017-09-28",
                'end': "2017-10-08",
            }
        },
        'holiday': {
            'Thanksgiving': {
                'start': "2017-11-23",
                'end': "2017-11-24",
            }
        }
    }
    time_off_no_holiday = {
        'timeOff': {
            'tiffany test': {
                'start': "2017-09-28",
                'end': "2017-10-08",
            }
        }
    }
    today = datetime.datetime(2017, 9, 20)

    def init_profiles(self):
        # tiffany, Success, SF, No, once a month
        Profile.objects.create(
            first_name='tiffany',
            last_name='test',
            preferred_first_name='tiffany',
            email='tiffany@TEST-mixpanel.com',
            department='Success',
            location='San Francisco',
            timezone='PST',
            google_hangout='Yes',
            frequency='Once a month',
            accept_matches='Yes',
            date_entered_mixpanel=datetime.datetime(2016, 10, 31),
            distinct_id='tiffany'
        )

    # all is well
    def test_regular(self):
        self.init_profiles()
        date = datetime.datetime(2017, 9, 27, 12, 0)
        RecurringAvailability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            day='2',
            time='12:00PM'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=date,
            time_available_utc=date
        )
        t = Profile.objects.get(first_name='tiffany')
        t_av = Availability.objects.get(profile=t, time_available_utc=date)
        self.assertEqual(Command.delete_av_from_recurring(Command(), t, t_av), False)

    # test delete availabilitity if recurring is not there
    def test_no_recurring(self):
        self.init_profiles()
        date = datetime.datetime(2017, 9, 27, 12, 0)
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=date,
            time_available_utc=date
        )
        t = Profile.objects.get(first_name='tiffany')
        t_av = Availability.objects.get(profile=t, time_available_utc=date)
        self.assertEqual(Command.delete_av_from_recurring(Command(), t, t_av), True)

    # tiffany is OOO on 9/28
    def test_one_ooo(self):
        self.init_profiles()
        date = datetime.datetime(2017, 9, 28, 12, 0)
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=date,
            time_available_utc=date
        )
        t = Profile.objects.get(first_name='tiffany')
        t_av = Availability.objects.get(profile=t, time_available_utc=date)
        self.assertEqual(Command.delete_av_from_time_off(Command(), t, t_av, self.time_off), True)

    # tiffany is OOO on 9/29
    def test_two_ooo(self):
        self.init_profiles()
        date = datetime.datetime(2017, 9, 29, 12, 0)
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=date,
            time_available_utc=date
        )
        t = Profile.objects.get(first_name='tiffany')
        t_av = Availability.objects.get(profile=t, time_available_utc=date)
        self.assertEqual(Command.delete_av_from_time_off(Command(), t, t_av, self.time_off), True)

    # tiffany is OOO on 10/08
    def test_three_ooo(self):
        self.init_profiles()
        date = datetime.datetime(2017, 10, 8, 12, 0)
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=date,
            time_available_utc=date
        )
        t = Profile.objects.get(first_name='tiffany')
        t_av = Availability.objects.get(profile=t, time_available_utc=date)
        self.assertEqual(Command.delete_av_from_time_off(Command(), t, t_av, self.time_off), True)

    # tiffany is not OOO on 10/09
    def test_four_ooo(self):
        self.init_profiles()
        date = datetime.datetime(2017, 10, 9, 12, 0)
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=date,
            time_available_utc=date
        )
        t = Profile.objects.get(first_name='tiffany')
        t_av = Availability.objects.get(profile=t, time_available_utc=date)
        self.assertEqual(Command.delete_av_from_time_off(Command(), t, t_av, self.time_off), False)

    # holiday
    def test_holiday(self):
        self.init_profiles()
        date = datetime.datetime(2017, 11, 23, 12, 0)
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=date,
            time_available_utc=date
        )
        t = Profile.objects.get(first_name='tiffany')
        t_av = Availability.objects.get(profile=t, time_available_utc=date)
        self.assertEqual(Command.delete_av_from_holiday(Command(), t_av, self.time_off), True)

    # no holiday
    def test_no_holiday(self):
        self.init_profiles()
        date = datetime.datetime(2017, 11, 23, 12, 0)
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=date,
            time_available_utc=date
        )
        t = Profile.objects.get(first_name='tiffany')
        t_av = Availability.objects.get(profile=t, time_available_utc=date)
        self.assertEqual(Command.delete_av_from_holiday(Command(), t_av, self.time_off_no_holiday), False)
