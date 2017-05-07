from django.core.management import call_command
from django.test import TestCase
from tablefor2.models import *

import datetime


class MatchTestCase(TestCase):
    past = datetime.datetime(2016, 11, 5, 12, 0)
    future = datetime.datetime(2017, 11, 5, 12, 0)  # UTC

    def setup(self):
        # tiffany, Success, SF, No, once a week
        t = Profile.objects.create(
            first_name='tiffany',
            last_name='qi',
            preferred_name='tiffany',
            email='tiffany@mixpanel.com',
            department='Success',
            location='San Francisco',
            google_hangout='No',
            frequency='Once a week',
            date_entered_mixpanel=datetime.datetime(2016, 10, 31)
        )
        Availability.objects.create(
            profile=t,
            time_available=self.past
        )
        Availability.objects.create(
            profile=t,
            time_available=self.future
        )

        # andrew, Engineering, SF, No, once a week
        a = Profile.objects.create(
            first_name='andrew',
            last_name='huang',
            preferred_name='andrew',
            email='andrew@not-mixpanel.com',
            department='Engineering',
            location='San Francisco',
            google_hangout='No',
            frequency='Once a week',
            date_entered_mixpanel=datetime.datetime(2016, 11, 01)
        )
        Availability.objects.create(
            profile=a,
            time_available=self.past
        )
        Availability.objects.create(
            profile=a,
            time_available=self.future
        )

        # PJ, Success, SF, No, once a week
        pj = Profile.objects.create(
            first_name='philip',
            last_name='ople',
            preferred_name='pj',
            email='pj@mixpanel.com',
            department='Success',
            location='San Francisco',
            google_hangout='Yes',
            frequency='Once a week',
            date_entered_mixpanel=datetime.datetime(2015, 11, 01)
        )
        Availability.objects.create(
            profile=pj,
            time_available=self.past
        )
        Availability.objects.create(
            profile=pj,
            time_available=self.future
        )

    def test_availability_match(self):
        self.setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        t_availability = Availability.objects.get(profile=t, time_available=self.future)
        a_availability = Availability.objects.get(profile=a, time_available=self.future)

        call_command('match_users')
        self.assertEqual(t_availability.matched_name, 'andrew huang')
        self.assertEqual(a_availability.matched_name, 'tiffany qi')
