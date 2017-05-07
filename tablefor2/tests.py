from django.core.management import call_command
from django.test import TestCase

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command

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

    def test_high_level_match(self):
        self.setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        t_availability = Availability.objects.get(profile=t, time_available=self.future)
        a_availability = Availability.objects.get(profile=a, time_available=self.future)
        pj_availability = Availability.objects.get(profile=pj, time_available=self.future)

        call_command('match_users')
        self.assertEqual(t_availability.matched_name, 'andrew huang')
        self.assertEqual(a_availability.matched_name, 'tiffany qi')
        self.assertEqual(pj_availability.matched_name, None)

    def test_check_match(self):
        self.setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')

        call_command('match_users')
        self.assertEqual(Command.check_match(Command(), t, a), True)
        self.assertEqual(Command.check_match(Command(), a, t), True)
        self.assertEqual(Command.check_match(Command(), t, pj), False)
        self.assertEqual(Command.check_match(Command(), a, pj), False)
        self.assertEqual(Command.check_match(Command(), pj, t), False)
        self.assertEqual(Command.check_match(Command(), pj, a), False)

    def test_check_google_hangout(self):
        self.setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')

        self.assertEqual(Command.check_google_hangout(Command(), t, a), False)

    def test_check_locations(self):
        self.setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')

        self.assertEqual(Command.check_locations(Command(), t, a), True)

    def test_check_departments(self):
        self.setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')

        self.assertEqual(Command.check_departments(Command(), t, a), True)
        self.assertEqual(Command.check_departments(Command(), t, pj), False)

    def test_check_previous_matches(self):
        self.setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        # at some point

    def test_setup(self):
        self.setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        # at some point
