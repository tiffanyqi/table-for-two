import datetime
import json
import pytz

from django.test import TestCase

from tablefor2.app_helpers import calculate_utc, get_names_from_group_avs
from tablefor2.models import GroupAvailability, Profile


class AppHelpersTestCase(TestCase):
    def setup_profiles(self):
        # tiffany, Success, SF, No, once a month
        Profile.objects.create(
            first_name='tiffany',
            last_name='test',
            preferred_first_name='tiffany',
            email='tiffany@TEST-mixpanel.com',
            department='Success',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            frequency=1,
            date_entered_mixpanel=datetime.datetime(2016, 10, 31),
            match_type='one-on-one',
            distinct_id='tiffany'
        )
        # another, Success, SF, No, once a month
        Profile.objects.create(
            first_name='another',
            last_name='test',
            preferred_first_name='another',
            email='another@TEST-mixpanel.com',
            department='Success',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            frequency=1,
            date_entered_mixpanel=datetime.datetime(2016, 10, 31),
            match_type='one-on-one',
            distinct_id='another'
        )
        # Tim, Engineering, New York, Yes, once a month
        Profile.objects.create(
            first_name='tim',
            last_name='test',
            preferred_first_name='tim',
            email='tim@TEST-mixpanel.com',
            department='Engineering',
            location='New York',
            google_hangout='Yes',
            timezone='EST',
            match_type='one-on-one',
            frequency=1,
            date_entered_mixpanel=datetime.datetime(2013, 6, 1),
            distinct_id='tim'
        )
        # Karima, Success, Other, Yes, once a month
        Profile.objects.create(
            first_name='karima',
            last_name='test',
            preferred_first_name='karima',
            email='karima@TEST-mixpanel.com',
            department='Success',
            location='Other',
            google_hangout='Yes',
            match_type='one-on-one',
            timezone='CEST',
            frequency=1,
            date_entered_mixpanel=datetime.datetime(2016, 6, 1),
            distinct_id='karima'
        )

    def setup_avs(self):
        past = datetime.datetime(2016, 11, 5, 12, 0, tzinfo=pytz.UTC)
        emails = ['another@TEST-mixpanel.com', 'tim@TEST-mixpanel.com', 'karima@TEST-mixpanel.com']
        GroupAvailability.objects.create(
            profile=Profile.objects.get(email='tiffany@TEST-mixpanel.com'),
            time_available=past,
            time_available_utc=past,
            matched_group_users=json.dumps(emails),
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

    def test_get_names_from_group_avs(self):
        self.setup_profiles()
        self.setup_avs()
        t = Profile.objects.get(first_name='tiffany')
        avs = GroupAvailability.objects.filter(profile=t).exclude(matched_group_users=None)
        self.assertEqual(get_names_from_group_avs(avs), 'another test, tim test, and karima test')
