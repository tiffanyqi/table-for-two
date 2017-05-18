from django.core.management import call_command
from django.test import TestCase

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command

import datetime
import pytz


class MatchTestCase(TestCase):
    past = datetime.datetime(2016, 11, 5, 12, 0, tzinfo=pytz.UTC)
    past2 = datetime.datetime(2016, 12, 5, 12, 0, tzinfo=pytz.UTC)
    future = datetime.datetime(2017, 11, 1, 12, 0, tzinfo=pytz.UTC)
    future2 = datetime.datetime(2017, 11, 2, 12, 0, tzinfo=pytz.UTC)

    # setup
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
        # Karima, Success, Other, Yes, once a week
        Profile.objects.create(
            first_name='karima',
            last_name='el moujahid',
            preferred_name='karima',
            email='karima@mixpanel.com',
            department='Success',
            location='Other',
            google_hangout='Yes',
            frequency='Once a week',
            date_entered_mixpanel=datetime.datetime(2016, 06, 01)
        )
        # Tim, Engineering, New York, Yes, once a week
        Profile.objects.create(
            first_name='tim',
            last_name='trefen',
            preferred_name='tim',
            email='tim@mixpanel.com',
            department='Engineering',
            location='New York',
            google_hangout='Yes',
            frequency='Once a week',
            date_entered_mixpanel=datetime.datetime(2013, 06, 01)
        )
        # Mike, Sales, SF, Yes, once a week
        Profile.objects.create(
            first_name='michael',
            last_name='walker',
            preferred_name='mike',
            email='mike@mixpanel.com',
            department='Sales',
            location='San Francisco',
            google_hangout='Yes',
            frequency='Once a week',
            date_entered_mixpanel=datetime.datetime(2016, 01, 01)
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
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.future
        )

    def previous_matches_setup(self):
        '''
        Order by new hires: [Andrew, Tiffany, Karima, Mike, PJ, Tim]
        Past: Andrew and Tiffany
        Past2: Andrew and PJ
        Past: Tiffany and Andrew
        Past: Karima and Tim
        Past: Mike and PJ
        Past: PJ and Mike
        Past2: PJ and Andrew
        Past: Tim and Karima

        Matching algorithm:
        Future: Andrew and Mike
        Future: PJ and Tim
        '''
        self.init_profiles()
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past,
            matched_name='andrew huang',
            matched_email='andrew@not-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past2
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
            time_available=self.past2,
            matched_name='pj ople',
            matched_email='pj@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past,
            matched_name='mike walker',
            matched_email='mike@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past2,
            matched_name='andrew huang',
            matched_email='andrew@not-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.past,
            matched_name='tim trefen',
            matched_email='tim@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.past,
            matched_name='karima el moujahid',
            matched_email='karima@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.past,
            matched_name='pj ople',
            matched_email='pj@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.future
        )

    def future_matches_setup(self):
        '''
        Order by new hires: [Andrew, Tiffany, Karima, Mike, PJ, Tim]
        Past: Andrew and Tiffany
        Past2: Andrew and PJ
        Past: Tiffany and Andrew
        Past: Karima and Tim
        Past: Mike and PJ
        Past: PJ and Mike
        Past2: PJ and Andrew
        Past: Tim and Karima
        Future: Andrew and Mike
        Future: PJ and Tim

        Matching algorithm:
        Future2: NOTHING, because Mike has already been matched this week
        '''
        self.init_profiles()
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past,
            matched_name='andrew huang',
            matched_email='andrew@not-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.future2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.past,
            matched_name='tiffany qi',
            matched_email='tiffany@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.past2,
            matched_name='pj ople',
            matched_email='pj@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.future,
            matched_name='mike walker',
            matched_email='mike@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.future2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past,
            matched_name='mike walker',
            matched_email='mike@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past2,
            matched_name='andrew huang',
            matched_email='andrew@not-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.future,
            matched_name='tim trefen',
            matched_email='tim@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.future2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.past,
            matched_name='tim trefen',
            matched_email='tim@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.future2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.past,
            matched_name='karima el moujahid',
            matched_email='karima@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.future,
            matched_name='pj ople',
            matched_email='pj@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.future2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.past,
            matched_name='pj ople',
            matched_email='pj@mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.future,
            matched_name='andrew huang',
            matched_email='andrew@not-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.future2
        )

    # tests

    # case where users don't have any matches in the beginning
    def test_check_match(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')
        t_av = Availability.objects.get(profile=t, time_available=self.future)
        a_av = Availability.objects.get(profile=a, time_available=self.future)
        pj_av = Availability.objects.get(profile=pj, time_available=self.future)
        k_av = Availability.objects.get(profile=k, time_available=self.future)
        tim_av = Availability.objects.get(profile=tim, time_available=self.future)
        mike_av = Availability.objects.get(profile=mike, time_available=self.future)

        self.assertEqual(Command.check_match(Command(), a_av, t_av, a, t), True)
        self.assertEqual(Command.check_match(Command(), a_av, pj_av, a, pj), True)
        self.assertEqual(Command.check_match(Command(), a_av, k_av, a, k), False)
        self.assertEqual(Command.check_match(Command(), a_av, tim_av, a, tim), False)
        self.assertEqual(Command.check_match(Command(), a_av, mike_av, a, mike), True)
        self.assertEqual(Command.check_match(Command(), t_av, pj_av, t, pj), False)
        self.assertEqual(Command.check_match(Command(), t_av, a_av, t, a), True)
        self.assertEqual(Command.check_match(Command(), t_av, k_av, t, k), False)
        self.assertEqual(Command.check_match(Command(), t_av, tim_av, t, tim), False)
        self.assertEqual(Command.check_match(Command(), t_av, mike_av, t, mike), True)
        self.assertEqual(Command.check_match(Command(), pj_av, t_av, pj, t), False)
        self.assertEqual(Command.check_match(Command(), pj_av, a_av, pj, a), True)
        self.assertEqual(Command.check_match(Command(), pj_av, k_av, pj, k), False)
        self.assertEqual(Command.check_match(Command(), pj_av, tim_av, pj, tim), True)
        self.assertEqual(Command.check_match(Command(), pj_av, mike_av, pj, mike), True)
        self.assertEqual(Command.check_match(Command(), k_av, a_av, k, a), False)
        self.assertEqual(Command.check_match(Command(), k_av, t_av, k, t), False)
        self.assertEqual(Command.check_match(Command(), k_av, tim_av, k, tim), True)
        self.assertEqual(Command.check_match(Command(), k_av, pj_av, k, pj), False)
        self.assertEqual(Command.check_match(Command(), k_av, mike_av, k, mike), True)
        self.assertEqual(Command.check_match(Command(), tim_av, t_av, tim, t), False)
        self.assertEqual(Command.check_match(Command(), tim_av, a_av, tim, a), False)
        self.assertEqual(Command.check_match(Command(), tim_av, pj_av, tim, pj), True)
        self.assertEqual(Command.check_match(Command(), tim_av, k_av, tim, k), True)
        self.assertEqual(Command.check_match(Command(), tim_av, mike_av, tim, mike), True)
        self.assertEqual(Command.check_match(Command(), mike_av, t_av, mike, t), True)
        self.assertEqual(Command.check_match(Command(), mike_av, a_av, mike, a), True)
        self.assertEqual(Command.check_match(Command(), mike_av, pj_av, mike, pj), True)
        self.assertEqual(Command.check_match(Command(), mike_av, k_av, mike, k), True)
        # self.assertEqual(Command.check_match(Command(), mike_av, tim_av, mike, tim), True)

    # case where there are matches in the beginning
    def test_check_match_with_matches(self):
        self.previous_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')
        t_av = Availability.objects.get(profile=t, time_available=self.future)
        a_av = Availability.objects.get(profile=a, time_available=self.future)
        pj_av = Availability.objects.get(profile=pj, time_available=self.future)
        k_av = Availability.objects.get(profile=k, time_available=self.future)
        tim_av = Availability.objects.get(profile=tim, time_available=self.future)
        mike_av = Availability.objects.get(profile=mike, time_available=self.future)

        self.assertEqual(Command.check_match(Command(), a_av, t_av, a, t), False)
        self.assertEqual(Command.check_match(Command(), a_av, pj_av, a, pj), False)
        self.assertEqual(Command.check_match(Command(), a_av, k_av, a, k), False)
        self.assertEqual(Command.check_match(Command(), a_av, tim_av, a, tim), False)
        self.assertEqual(Command.check_match(Command(), a_av, mike_av, a, mike), True)
        self.assertEqual(Command.check_match(Command(), t_av, pj_av, t, pj), False)
        self.assertEqual(Command.check_match(Command(), t_av, a_av, t, a), False)
        self.assertEqual(Command.check_match(Command(), t_av, k_av, t, k), False)
        self.assertEqual(Command.check_match(Command(), t_av, tim_av, t, tim), False)
        self.assertEqual(Command.check_match(Command(), t_av, mike_av, t, mike), True)
        self.assertEqual(Command.check_match(Command(), pj_av, t_av, pj, t), False)
        self.assertEqual(Command.check_match(Command(), pj_av, a_av, pj, a), False)
        self.assertEqual(Command.check_match(Command(), pj_av, k_av, pj, k), False)
        self.assertEqual(Command.check_match(Command(), pj_av, tim_av, pj, tim), True)
        self.assertEqual(Command.check_match(Command(), pj_av, pj_av, pj, mike), False)
        self.assertEqual(Command.check_match(Command(), k_av, a_av, k, a), False)
        self.assertEqual(Command.check_match(Command(), k_av, t_av, k, t), False)
        self.assertEqual(Command.check_match(Command(), k_av, tim_av, k, tim), False)
        self.assertEqual(Command.check_match(Command(), k_av, pj_av, k, pj), False)
        self.assertEqual(Command.check_match(Command(), k_av, mike_av, k, mike), True)
        self.assertEqual(Command.check_match(Command(), tim_av, t_av, tim, t), False)
        self.assertEqual(Command.check_match(Command(), tim_av, a_av, tim, a), False)
        self.assertEqual(Command.check_match(Command(), tim_av, pj_av, tim, pj), True)
        self.assertEqual(Command.check_match(Command(), tim_av, k_av, tim, k), False)
        self.assertEqual(Command.check_match(Command(), tim_av, mike_av, tim, mike), True)
        self.assertEqual(Command.check_match(Command(), mike_av, t_av, mike, t), True)
        self.assertEqual(Command.check_match(Command(), mike_av, a_av, mike, a), True)
        self.assertEqual(Command.check_match(Command(), mike_av, pj_av, mike, pj), False)
        self.assertEqual(Command.check_match(Command(), mike_av, k_av, mike, k), True)
        self.assertEqual(Command.check_match(Command(), mike_av, tim_av, mike, tim), True)

    def test_match_and_run_future_first_day(self):
        self.previous_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')
        t_av_past = Availability.objects.get(profile=t, time_available=self.past)
        a_av_past = Availability.objects.get(profile=a, time_available=self.past)
        mike_av_past2 = Availability.objects.get(profile=mike, time_available=self.past2)
        t_av_future = Availability.objects.get(profile=t, time_available=self.future)
        a_av_future = Availability.objects.get(profile=a, time_available=self.future)
        pj_av_future = Availability.objects.get(profile=pj, time_available=self.future)
        k_av_future = Availability.objects.get(profile=k, time_available=self.future)
        tim_av_future = Availability.objects.get(profile=tim, time_available=self.future)
        mike_av_future = Availability.objects.get(profile=mike, time_available=self.future)

        self.assertEqual(t_av_past.matched_name, 'andrew huang')
        self.assertEqual(a_av_past.matched_name, 'tiffany qi')
        self.assertEqual(mike_av_past2.matched_name, None)

        future_availabilities = {
            1509537600.0: [a_av_future, t_av_future, k_av_future, mike_av_future, pj_av_future, tim_av_future],
        }
        matches = [
            [1509537600.0, a, mike],
            [1509537600.0, pj, tim]
        ]
        self.assertEqual(Command.runs_matches(Command(), future_availabilities), matches)

    # case where there's two day in a row, but folks shouldn't be matched
    def test_match_and_run_future_second_day(self):
        self.future_matches_setup()

        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')
        t_av_future = Availability.objects.get(profile=t, time_available=self.future)
        a_av_future = Availability.objects.get(profile=a, time_available=self.future)
        pj_av_future = Availability.objects.get(profile=pj, time_available=self.future)
        k_av_future = Availability.objects.get(profile=k, time_available=self.future)
        tim_av_future = Availability.objects.get(profile=tim, time_available=self.future)
        mike_av_future = Availability.objects.get(profile=mike, time_available=self.future)
        t_av_future2 = Availability.objects.get(profile=t, time_available=self.future2)
        a_av_future2 = Availability.objects.get(profile=a, time_available=self.future2)
        pj_av_future2 = Availability.objects.get(profile=pj, time_available=self.future2)
        k_av_future2 = Availability.objects.get(profile=k, time_available=self.future2)
        tim_av_future2 = Availability.objects.get(profile=tim, time_available=self.future2)
        mike_av_future2 = Availability.objects.get(profile=mike, time_available=self.future2)

        future_availabilities = {
            1509537600.0: [a_av_future, t_av_future, k_av_future, mike_av_future, pj_av_future, tim_av_future],
            1509624000.0: [a_av_future2, t_av_future2, k_av_future2, mike_av_future2, pj_av_future2, tim_av_future2]
        }
        matches = []
        self.assertEqual(Command.runs_matches(Command(), future_availabilities), matches)

    def test_check_google_hangout(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')

        self.assertEqual(Command.check_google_hangout(Command(), t, a), False)
        self.assertEqual(Command.check_google_hangout(Command(), t, pj), False)
        self.assertEqual(Command.check_google_hangout(Command(), pj, k), True)

    def test_check_locations(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')

        self.assertEqual(Command.check_locations(Command(), t, a), True)
        self.assertEqual(Command.check_locations(Command(), k, pj), False)
        self.assertEqual(Command.check_locations(Command(), k, tim), False)
        self.assertEqual(Command.check_locations(Command(), tim, t), False)

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

        self.assertEqual(Command.check_previous_matches(Command(), a, t), True)
        self.assertEqual(Command.check_previous_matches(Command(), a, pj), True)

    def test_check_previous_matches_with_matches(self):
        self.previous_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')

        self.assertEqual(Command.check_previous_matches(Command(), a, t), False)
        self.assertEqual(Command.check_previous_matches(Command(), a, pj), False)
        self.assertEqual(Command.check_previous_matches(Command(), a, mike), True)
        self.assertEqual(Command.check_previous_matches(Command(), k, mike), True)
        self.assertEqual(Command.check_previous_matches(Command(), k, tim), False)

    def test_check_previous_matches_with_future_matches(self):
        self.future_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')

        self.assertEqual(Command.check_previous_matches(Command(), a, t), False)
        self.assertEqual(Command.check_previous_matches(Command(), a, pj), False)
        self.assertEqual(Command.check_previous_matches(Command(), a, mike), False)
        self.assertEqual(Command.check_previous_matches(Command(), k, mike), True)
        self.assertEqual(Command.check_previous_matches(Command(), k, tim), False)

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

    def test_check_frequency_previous(self):
        self.previous_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        mike = Profile.objects.get(first_name='michael')
        t_av = Availability.objects.get(profile=t, time_available=self.future)
        a_av = Availability.objects.get(profile=a, time_available=self.future)
        mike_av = Availability.objects.get(profile=mike, time_available=self.future)

        self.assertEqual(Command.check_frequency(Command(), t_av, t), True)
        self.assertEqual(Command.check_frequency(Command(), a_av, a), True)

        # case where users just were matched
        mike_av.matched_name = 'andrew huang'
        mike_av.matched_email = 'andrew@not-mixpanel.com'
        mike_av.save()
        a_av.matched_name = 'mike walker'
        a_av.matched_email = 'mike@mixpanel.com'
        a_av.save()

        self.assertEqual(Command.check_frequency(Command(), a_av, a), False)
        self.assertEqual(Command.check_frequency(Command(), mike_av, mike), False)
        self.assertEqual(Command.check_frequency(Command(), t_av, t), True)

    def test_check_frequency_future(self):
        self.future_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')
        t_av = Availability.objects.get(profile=t, time_available=self.future2)
        a_av = Availability.objects.get(profile=a, time_available=self.future2)
        pj_av = Availability.objects.get(profile=pj, time_available=self.future2)
        k_av = Availability.objects.get(profile=k, time_available=self.future2)
        tim_av = Availability.objects.get(profile=tim, time_available=self.future2)
        mike_av = Availability.objects.get(profile=mike, time_available=self.future2)

        self.assertEqual(Command.check_frequency(Command(), t_av, t), True)
        self.assertEqual(Command.check_frequency(Command(), a_av, a), False)
        self.assertEqual(Command.check_frequency(Command(), pj_av, pj), False)
        self.assertEqual(Command.check_frequency(Command(), k_av, k), True)
        self.assertEqual(Command.check_frequency(Command(), tim_av, tim), False)
        self.assertEqual(Command.check_frequency(Command(), mike_av, mike), False)

    def test_setup(self):
        self.fresh_setup()
        avs = Availability.objects.all()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        tim = Profile.objects.get(first_name='tim')
        t_av_past = Availability.objects.get(profile=t, time_available=self.past)
        a_av_past = Availability.objects.get(profile=a, time_available=self.past)
        tim_av_past = Availability.objects.get(profile=tim, time_available=self.past)
        a_av_future = Availability.objects.get(profile=a, time_available=self.future)
        tim_av_future = Availability.objects.get(profile=tim, time_available=self.future)

        self.assertIn(a_av_past, Command.setup(Command(), avs)[1478347200.0])
        self.assertIn(t_av_past, Command.setup(Command(), avs)[1478347200.0])
        self.assertIn(tim_av_past, Command.setup(Command(), avs)[1478347200.0])
        self.assertIn(a_av_future, Command.setup(Command(), avs)[1509537600.0])
        self.assertIn(tim_av_future, Command.setup(Command(), avs)[1509537600.0])
        self.assertNotIn(a_av_past, Command.setup(Command(), avs)[1509537600.0])
        self.assertNotIn(a_av_future, Command.setup(Command(), avs)[1478347200.0])
