from django.core.management import call_command
from django.test import TestCase

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command

import datetime


class MatchTestCase(TestCase):
    past = datetime.datetime(2016, 11, 5, 12, 0)
    future = datetime.datetime(2017, 11, 5, 12, 0)  # UTC

    def init_profiles(self):
        # tiffany, Success, SF, No, once a week
        Profile.objects.create(
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
        # andrew, Engineering, SF, No, once a week
        Profile.objects.create(
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
        # PJ, Success, SF, Yes, once a week
        Profile.objects.create(
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

    def fresh_setup(self):
        self.init_profiles()
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.future
        )

    def previous_matches_setup(self):
        self.init_profiles()
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past,
            matched_name='andrew huang',
            matched_email='andrew@not-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.past,
            matched_name='tiffany qi',
            matched_email='tiffany@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.future
        )

    def test_match(self):
        self.previous_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        t_av = Availability.objects.get(profile=t, time_available=self.past)
        a_av = Availability.objects.get(profile=a, time_available=self.past)
        pj_av = Availability.objects.get(profile=pj, time_available=self.past)

        self.assertEqual(t_av.matched_name, 'andrew huang')
        self.assertEqual(a_av.matched_name, 'tiffany qi')
        self.assertEqual(pj_av.matched_name, None)

    def test_check_match(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        t_av = Availability.objects.get(profile=t, time_available=self.future)
        a_av = Availability.objects.get(profile=a, time_available=self.future)
        pj_av = Availability.objects.get(profile=pj, time_available=self.future)

        # case where users don't have any matches in the beginning
        self.assertEqual(Command.check_match(Command(), a_av, a, t), True)
        self.assertEqual(Command.check_match(Command(), a_av, a, pj), True)
        self.assertEqual(Command.check_match(Command(), t_av, t, pj), False)
        self.assertEqual(Command.check_match(Command(), t_av, t, a), True)
        self.assertEqual(Command.check_match(Command(), pj_av, pj, t), False)
        self.assertEqual(Command.check_match(Command(), pj_av, pj, a), True)

    def test_check_match_with_matches(self):
        self.previous_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        t_av = Availability.objects.get(profile=t, time_available=self.future)
        a_av = Availability.objects.get(profile=a, time_available=self.future)
        pj_av = Availability.objects.get(profile=pj, time_available=self.future)

        # case where there are matches in the beginning
        self.assertEqual(Command.check_match(Command(), a_av, a, t), False)
        self.assertEqual(Command.check_match(Command(), a_av, a, pj), True)
        self.assertEqual(Command.check_match(Command(), t_av, t, pj), False)
        self.assertEqual(Command.check_match(Command(), t_av, t, a), False)
        self.assertEqual(Command.check_match(Command(), pj_av, pj, t), False)
        self.assertEqual(Command.check_match(Command(), pj_av, pj, a), True)

    def test_check_google_hangout(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')

        self.assertEqual(Command.check_google_hangout(Command(), t, a), False)
        self.assertEqual(Command.check_google_hangout(Command(), t, pj), False)

    def test_check_locations(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')

        self.assertEqual(Command.check_locations(Command(), t, a), True)
        self.assertEqual(Command.check_locations(Command(), t, pj), True)

    def test_check_departments(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')

        self.assertEqual(Command.check_departments(Command(), t, a), True)
        self.assertEqual(Command.check_departments(Command(), t, pj), False)

    def test_check_previous_matches(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')

        # case where users don't have any matches in the beginning
        self.assertEqual(Command.check_previous_matches(Command(), a, t), True)
        self.assertEqual(Command.check_previous_matches(Command(), a, pj), True)
        self.assertEqual(Command.check_previous_matches(Command(), t, pj), True)

    def test_check_not_currently_matched(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        t_av = Availability.objects.get(profile=t, time_available=self.future)
        a_av = Availability.objects.get(profile=a, time_available=self.future)
        pj_av = Availability.objects.get(profile=pj, time_available=self.future)

        # case where users don't have any matches in the beginning
        self.assertEqual(Command.check_not_currently_matched(Command(), a_av), True)
        self.assertEqual(Command.check_not_currently_matched(Command(), t_av), True)
        self.assertEqual(Command.check_not_currently_matched(Command(), pj_av), True)

        # case where users just were matched
        t_av.matched_name = 'andrew huang'
        t_av.matched_email = 'andrew@not-mixpanel.com'
        a_av.matched_name = 'tiffany qi'
        a_av.matched_email = 'tiffany@mixpanel.com'

        self.assertEqual(Command.check_not_currently_matched(Command(), a_av), False)
        self.assertEqual(Command.check_not_currently_matched(Command(), t_av), False)
        self.assertEqual(Command.check_not_currently_matched(Command(), pj_av), True)

    def test_setup(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        # at some point

    def test_none(self):
        self.fresh_setup()
        # at some point
