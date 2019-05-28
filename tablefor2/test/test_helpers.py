from django.test import TestCase

from tablefor2.helpers import calculate_utc, determine_ampm, get_next_weekday
from tablefor2.models import *

import datetime
import pytz


class HelpersTestCast(TestCase):
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
            date_entered_mixpanel=datetime.datetime(2016, 10, 31),
            match_type='one-on-one',
            distinct_id='tiffany'
        )
        # Tim, Engineering, New York, Yes, once a month
        Profile.objects.create(
            first_name='tim',
            last_name='trefen',
            preferred_first_name='tim',
            email='tim@TEST-mixpanel.com',
            department='Engineering',
            location='New York',
            google_hangout='Yes',
            timezone='EST',
            match_type='one-on-one',
            frequency='Once a month',
            date_entered_mixpanel=datetime.datetime(2013, 06, 01),
            distinct_id='tim'
        )
        # Karima, Success, Other, Yes, once a month
        Profile.objects.create(
            first_name='karima',
            last_name='el moujahid',
            preferred_first_name='karima',
            email='karima@TEST-mixpanel.com',
            department='Success',
            location='Other',
            google_hangout='Yes',
            match_type='one-on-one',
            timezone='CEST',
            frequency='Once a month',
            date_entered_mixpanel=datetime.datetime(2016, 06, 01),
            distinct_id='karima'
        )

    def test_calculate_utc(self):
        self.setup_profiles()
        t = Profile.objects.get(first_name='tiffany')
        tim = Profile.objects.get(first_name='tim')
        k = Profile.objects.get(first_name='karima')

        # not daylight savings
        self.assertEqual(calculate_utc(t, datetime.datetime(2016, 1, 5, 12, 0)), datetime.datetime(2016, 1, 5, 20, 0, tzinfo=pytz.UTC))
        self.assertEqual(calculate_utc(tim, datetime.datetime(2016, 1, 5, 15, 0)), datetime.datetime(2016, 1, 5, 20, 0, tzinfo=pytz.UTC))
        self.assertEqual(calculate_utc(k, datetime.datetime(2016, 1, 5, 21, 0)), datetime.datetime(2016, 1, 5, 20, 0, tzinfo=pytz.UTC))

        # daylight savings
        self.assertEqual(calculate_utc(t, datetime.datetime(2017, 5, 21, 11, 30)), datetime.datetime(2017, 5, 21, 18, 30, tzinfo=pytz.UTC))
        self.assertEqual(calculate_utc(tim, datetime.datetime(2017, 5, 21, 14, 30)), datetime.datetime(2017, 5, 21, 18, 30, tzinfo=pytz.UTC))
        self.assertEqual(calculate_utc(k, datetime.datetime(2017, 5, 21, 20, 30)), datetime.datetime(2017, 5, 21, 18, 30, tzinfo=pytz.UTC))

    def test_determine_ampm(self):
        self.assertEqual(determine_ampm('12:00PM'), '12:00')
        self.assertEqual(determine_ampm('5:00PM'), '17:00')
        self.assertEqual(determine_ampm('1:00PM'), '13:00')
        self.assertEqual(determine_ampm('10:00AM'), '10:00')
        self.assertEqual(determine_ampm('9:30AM'), '9:30')

    def test_get_next_weekday(self):
        today = datetime.datetime(2017, 8, 21)
        self.assertEqual(get_next_weekday(today, '0', '12:00'), datetime.datetime(2017, 8, 28, 12, 0))
        self.assertEqual(get_next_weekday(today, '1', '1:00'), datetime.datetime(2017, 8, 29, 1, 0))
        self.assertEqual(get_next_weekday(today, '4', '15:30'), datetime.datetime(2017, 9, 1, 15, 30))

        today = datetime.datetime(2017, 8, 24)
        self.assertEqual(get_next_weekday(today, '0', '12:00'), datetime.datetime(2017, 8, 28, 12, 0))
        self.assertEqual(get_next_weekday(today, '1', '1:00'), datetime.datetime(2017, 8, 29, 1, 0))
        self.assertEqual(get_next_weekday(today, '4', '15:30'), datetime.datetime(2017, 9, 1, 15, 30))
