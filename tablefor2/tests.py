from django.core.management import call_command
from django.test import TestCase

from tablefor2.helpers import calculate_utc, determine_ampm, get_next_weekday
from tablefor2.models import *
from tablefor2.management.commands.match_users import Command

import datetime
import pytz


class MatchTestCase(TestCase):
    past = datetime.datetime(2016, 11, 5, 12, 0, tzinfo=pytz.UTC)  # 1478347200
    past2 = datetime.datetime(2016, 12, 5, 12, 0, tzinfo=pytz.UTC)
    future = datetime.datetime(2017, 11, 1, 12, 0, tzinfo=pytz.UTC)  # 1509537600
    future2 = datetime.datetime(2017, 11, 2, 12, 0, tzinfo=pytz.UTC)

    # setup
    def init_profiles(self):
        # tiffany, Success, SF, No, once a month
        Profile.objects.create(
            first_name='tiffany',
            last_name='qi',
            preferred_name='tiffany',
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
        # andrew, Engineering, SF, No, once a month
        Profile.objects.create(
            first_name='andrew',
            last_name='huang',
            preferred_name='andrew',
            email='andrew@not-TEST-mixpanel.com',
            department='Engineering',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            frequency='Once a month',
            accept_matches='Yes',
            date_entered_mixpanel=datetime.datetime(2016, 11, 01),
            distinct_id='andrew'
        )
        # PJ, Success, SF, Yes, once a month
        Profile.objects.create(
            first_name='philip',
            last_name='ople',
            preferred_name='pj',
            email='pj@TEST-mixpanel.com',
            department='Success',
            location='San Francisco',
            timezone='PST',
            google_hangout='Yes',
            frequency='Once a month',
            accept_matches='Yes',
            date_entered_mixpanel=datetime.datetime(2015, 11, 01),
            distinct_id='pj'
        )
        # Karima, Success, Other, Yes, once a month
        Profile.objects.create(
            first_name='karima',
            last_name='el moujahid',
            preferred_name='karima',
            email='karima@TEST-mixpanel.com',
            department='Success',
            location='Other',
            google_hangout='Yes',
            timezone='CEST',
            frequency='Once a month',
            accept_matches='Yes',
            date_entered_mixpanel=datetime.datetime(2016, 06, 01),
            distinct_id='karima'
        )
        # Tim, Engineering, New York, Yes, once a month
        Profile.objects.create(
            first_name='tim',
            last_name='trefen',
            preferred_name='tim',
            email='tim@TEST-mixpanel.com',
            department='Engineering',
            location='New York',
            google_hangout='Yes',
            timezone='EST',
            frequency='Once a month',
            accept_matches='Yes',
            date_entered_mixpanel=datetime.datetime(2013, 06, 01),
            distinct_id='tim'
        )
        # Mike, Sales, SF, Yes, once a month
        Profile.objects.create(
            first_name='michael',
            last_name='walker',
            preferred_name='mike',
            email='mike@TEST-mixpanel.com',
            department='Sales',
            location='San Francisco',
            timezone='PST',
            google_hangout='Yes',
            frequency='Once a month',
            accept_matches='Yes',
            date_entered_mixpanel=datetime.datetime(2016, 01, 01),
            distinct_id='mike'
        )
        # Poop, Engineering, SF, Yes, once a month
        Profile.objects.create(
            first_name='poop',
            last_name='test',
            preferred_name='poop',
            email='poop@TEST-mixpanel.com',
            department='Engineering',
            location='San Francisco',
            timezone='PST',
            google_hangout='Yes',
            frequency='Once a month',
            accept_matches='No',
            date_entered_mixpanel=datetime.datetime(2016, 01, 01),
            distinct_id='poop'
        )

    def fresh_setup(self):
        '''
        Order by new hires: [Andrew, Tiffany, Karima, Mike, PJ, Tim]
        Past: Andrew and PJ
        Past: Karima and Mike
        Past2: Andrew and Mike
        Past2: Karima and Tim
        Past2: Mike and PJ
        Future: Andrew and Tiffany
        Future: Mike and Tim
        '''
        self.init_profiles()
        Availability.objects.create(
            profile=Profile.objects.get(first_name='poop'),
            time_available=self.past,
            time_available_utc=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past,
            time_available_utc=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.past,
            time_available_utc=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past,
            time_available_utc=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.past,
            time_available_utc=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.past,
            time_available_utc=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.past,
            time_available_utc=self.past
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.future,
            time_available_utc=self.future
        )

    def previous_matches_setup(self):
        '''
        The setup:
        Past: Andrew and Tiffany
        Past: Karima and Tim
        Past: PJ and Mike
        Past2: Andrew and PJ
        '''
        self.init_profiles()
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='andrew huang',
            matched_email='andrew@not-TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past2,
            time_available_utc=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='tiffany qi',
            matched_email='tiffany@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.past2,
            time_available_utc=self.past2,
            matched_name='pj ople',
            matched_email='pj@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='mike walker',
            matched_email='mike@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past2,
            time_available_utc=self.past2,
            matched_name='andrew huang',
            matched_email='andrew@not-TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='tim trefen',
            matched_email='tim@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.past2,
            time_available_utc=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='karima el moujahid',
            matched_email='karima@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.past2,
            time_available_utc=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='pj ople',
            matched_email='pj@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.past2,
            time_available_utc=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.future,
            time_available_utc=self.future
        )

    def future_matches_setup(self):
        '''
        The setup:
        Past: Andrew and Tiffany
        Past: Karima and Tim
        Past: PJ and Mike
        Past2: Andrew and PJ
        Future: Andrew and Mike
        Future: PJ and Tim
        '''
        self.init_profiles()
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='andrew huang',
            matched_email='andrew@not-TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.past2,
            time_available_utc=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tiffany'),
            time_available=self.future2,
            time_available_utc=self.future2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='tiffany qi',
            matched_email='tiffany@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.past2,
            time_available_utc=self.past2,
            matched_name='pj ople',
            matched_email='pj@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.future,
            time_available_utc=self.future,
            matched_name='mike walker',
            matched_email='mike@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='andrew'),
            time_available=self.future2,
            time_available_utc=self.future2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='mike walker',
            matched_email='mike@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.past2,
            time_available_utc=self.past2,
            matched_name='andrew huang',
            matched_email='andrew@not-TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.future,
            time_available_utc=self.future,
            matched_name='tim trefen',
            matched_email='tim@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='philip'),
            time_available=self.future2,
            time_available_utc=self.future2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='tim trefen',
            matched_email='tim@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.past2,
            time_available_utc=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.future,
            time_available_utc=self.future
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='karima'),
            time_available=self.future2,
            time_available_utc=self.future2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='karima el moujahid',
            matched_email='karima@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.past2,
            time_available_utc=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.future,
            time_available_utc=self.future,
            matched_name='pj ople',
            matched_email='pj@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='tim'),
            time_available=self.future2,
            time_available_utc=self.future2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.past,
            time_available_utc=self.past,
            matched_name='pj ople',
            matched_email='pj@TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.past2,
            time_available_utc=self.past2
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.future,
            time_available_utc=self.future,
            matched_name='andrew huang',
            matched_email='andrew@not-TEST-mixpanel.com'
        )
        Availability.objects.create(
            profile=Profile.objects.get(first_name='michael'),
            time_available=self.future2,
            time_available_utc=self.future2
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
        t_av = Availability.objects.get(profile=t, time_available_utc=self.future)
        a_av = Availability.objects.get(profile=a, time_available_utc=self.future)
        pj_av = Availability.objects.get(profile=pj, time_available_utc=self.future)
        k_av = Availability.objects.get(profile=k, time_available_utc=self.future)
        tim_av = Availability.objects.get(profile=tim, time_available_utc=self.future)
        mike_av = Availability.objects.get(profile=mike, time_available_utc=self.future)

        self.assertEqual(Command.check_match(Command(), a_av, t_av, a, t), True)
        self.assertEqual(Command.check_match(Command(), a_av, pj_av, a, pj), True)
        self.assertEqual(Command.check_match(Command(), a_av, k_av, a, k), False)
        self.assertEqual(Command.check_match(Command(), a_av, tim_av, a, tim), False)
        self.assertEqual(Command.check_match(Command(), a_av, mike_av, a, mike), True)
        self.assertEqual(Command.check_match(Command(), t_av, pj_av, t, pj), False)
        self.assertEqual(Command.check_match(Command(), t_av, a_av, t, a), True)
        self.assertEqual(Command.check_match(Command(), t_av, k_av, t, k), False)
        self.assertEqual(Command.check_match(Command(), t_av, tim_av, t, tim), True)
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
        self.assertEqual(Command.check_match(Command(), tim_av, t_av, tim, t), True)
        self.assertEqual(Command.check_match(Command(), tim_av, a_av, tim, a), False)
        self.assertEqual(Command.check_match(Command(), tim_av, pj_av, tim, pj), True)
        self.assertEqual(Command.check_match(Command(), tim_av, k_av, tim, k), True)
        self.assertEqual(Command.check_match(Command(), tim_av, mike_av, tim, mike), True)
        self.assertEqual(Command.check_match(Command(), mike_av, t_av, mike, t), True)
        self.assertEqual(Command.check_match(Command(), mike_av, a_av, mike, a), True)
        self.assertEqual(Command.check_match(Command(), mike_av, pj_av, mike, pj), True)
        self.assertEqual(Command.check_match(Command(), mike_av, k_av, mike, k), True)
        self.assertEqual(Command.check_match(Command(), mike_av, tim_av, mike, tim), True)

    # case where there are matches in the beginning
    def test_check_match_with_matches(self):
        self.previous_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')
        t_av = Availability.objects.get(profile=t, time_available_utc=self.future)
        a_av = Availability.objects.get(profile=a, time_available_utc=self.future)
        pj_av = Availability.objects.get(profile=pj, time_available_utc=self.future)
        k_av = Availability.objects.get(profile=k, time_available_utc=self.future)
        tim_av = Availability.objects.get(profile=tim, time_available_utc=self.future)
        mike_av = Availability.objects.get(profile=mike, time_available_utc=self.future)

        self.assertEqual(Command.check_match(Command(), a_av, t_av, a, t), False)
        self.assertEqual(Command.check_match(Command(), a_av, pj_av, a, pj), False)
        self.assertEqual(Command.check_match(Command(), a_av, k_av, a, k), False)
        self.assertEqual(Command.check_match(Command(), a_av, tim_av, a, tim), False)
        self.assertEqual(Command.check_match(Command(), a_av, mike_av, a, mike), True)
        self.assertEqual(Command.check_match(Command(), t_av, pj_av, t, pj), False)
        self.assertEqual(Command.check_match(Command(), t_av, a_av, t, a), False)
        self.assertEqual(Command.check_match(Command(), t_av, k_av, t, k), False)
        self.assertEqual(Command.check_match(Command(), t_av, tim_av, t, tim), True)
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
        self.assertEqual(Command.check_match(Command(), tim_av, t_av, tim, t), True)
        self.assertEqual(Command.check_match(Command(), tim_av, a_av, tim, a), False)
        self.assertEqual(Command.check_match(Command(), tim_av, pj_av, tim, pj), True)
        self.assertEqual(Command.check_match(Command(), tim_av, k_av, tim, k), False)
        self.assertEqual(Command.check_match(Command(), tim_av, mike_av, tim, mike), True)
        self.assertEqual(Command.check_match(Command(), mike_av, t_av, mike, t), True)
        self.assertEqual(Command.check_match(Command(), mike_av, a_av, mike, a), True)
        self.assertEqual(Command.check_match(Command(), mike_av, pj_av, mike, pj), False)
        self.assertEqual(Command.check_match(Command(), mike_av, k_av, mike, k), True)
        self.assertEqual(Command.check_match(Command(), mike_av, tim_av, mike, tim), True)

    def test_match_and_run_fresh_first_day(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')
        t_av_past = Availability.objects.get(profile=t, time_available_utc=self.past)
        a_av_future = Availability.objects.get(profile=a, time_available_utc=self.future)
        t_av_future = Availability.objects.get(profile=t, time_available_utc=self.future)
        k_av_future = Availability.objects.get(profile=k, time_available_utc=self.future)
        matches = [
            [a_av_future, a, pj],
            [t_av_future, t, tim],
            [k_av_future, k, mike]
        ]

        self.assertEqual(t_av_past.matched_name, None)
        self.assertEqual(Command.runs_matches(Command()), matches)

    def test_match_and_run_future_first_day(self):
        self.previous_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')
        t_av_past = Availability.objects.get(profile=t, time_available_utc=self.past)
        a_av_past = Availability.objects.get(profile=a, time_available_utc=self.past)
        a_av_future = Availability.objects.get(profile=a, time_available_utc=self.future)
        t_av_future = Availability.objects.get(profile=t, time_available_utc=self.future)
        mike_av_past2 = Availability.objects.get(profile=mike, time_available_utc=self.past2)

        self.assertEqual(t_av_past.matched_name, 'andrew huang')
        self.assertEqual(a_av_past.matched_name, 'tiffany qi')
        self.assertEqual(mike_av_past2.matched_name, None)

        matches = [
            [a_av_future, a, mike],
            [t_av_future, t, tim]
        ]
        self.assertEqual(Command.runs_matches(Command()), matches)

    # case where there's two day in a row, but folks shouldn't be matched
    def test_match_and_run_future_second_day(self):
        self.future_matches_setup()
        self.assertEqual(Command.runs_matches(Command()), [])

    def test_check_google_hangout(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')

        self.assertEqual(Command.check_google_hangout(Command(), t, a), False)
        self.assertEqual(Command.check_google_hangout(Command(), t, pj), True)
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
        t_av = Availability.objects.get(profile=t, time_available_utc=self.future)
        a_av = Availability.objects.get(profile=a, time_available_utc=self.future)
        pj_av = Availability.objects.get(profile=pj, time_available_utc=self.future)

        # case where users don't have any matches in the beginning
        self.assertEqual(Command.check_not_currently_matched(Command(), a_av), True)
        self.assertEqual(Command.check_not_currently_matched(Command(), t_av), True)
        self.assertEqual(Command.check_not_currently_matched(Command(), pj_av), True)

        # case where users just were matched
        t_av.matched_name = 'andrew huang'
        t_av.matched_email = 'andrew@not-TEST-mixpanel.com'
        a_av.matched_name = 'tiffany qi'
        a_av.matched_email = 'tiffany@TEST-mixpanel.com'

        self.assertEqual(Command.check_not_currently_matched(Command(), a_av), False)
        self.assertEqual(Command.check_not_currently_matched(Command(), t_av), False)
        self.assertEqual(Command.check_not_currently_matched(Command(), pj_av), True)

    def test_check_frequency_previous(self):
        self.previous_matches_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        mike = Profile.objects.get(first_name='michael')
        t_av = Availability.objects.get(profile=t, time_available_utc=self.future)
        a_av = Availability.objects.get(profile=a, time_available_utc=self.future)
        mike_av = Availability.objects.get(profile=mike, time_available_utc=self.future)

        self.assertEqual(Command.check_frequency(Command(), t_av, t), True)
        self.assertEqual(Command.check_frequency(Command(), a_av, a), True)

        # case where users just were matched
        mike_av.matched_name = 'andrew huang'
        mike_av.matched_email = 'andrew@not-TEST-mixpanel.com'
        mike_av.save()
        a_av.matched_name = 'mike walker'
        a_av.matched_email = 'mike@TEST-mixpanel.com'
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
        t_av = Availability.objects.get(profile=t, time_available_utc=self.future2)
        a_av = Availability.objects.get(profile=a, time_available_utc=self.future2)
        pj_av = Availability.objects.get(profile=pj, time_available_utc=self.future2)
        k_av = Availability.objects.get(profile=k, time_available_utc=self.future2)
        tim_av = Availability.objects.get(profile=tim, time_available_utc=self.future2)
        mike_av = Availability.objects.get(profile=mike, time_available_utc=self.future2)

        self.assertEqual(Command.check_frequency(Command(), t_av, t), True)
        self.assertEqual(Command.check_frequency(Command(), a_av, a), False)
        self.assertEqual(Command.check_frequency(Command(), pj_av, pj), False)
        self.assertEqual(Command.check_frequency(Command(), k_av, k), True)
        self.assertEqual(Command.check_frequency(Command(), tim_av, tim), False)
        self.assertEqual(Command.check_frequency(Command(), mike_av, mike), False)

    def test_check_accept_matches(self):
        self.fresh_setup()
        poop = Profile.objects.get(first_name='poop')
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')

        self.assertEqual(Command.check_accept_matches(Command(), t, a), True)
        self.assertEqual(Command.check_accept_matches(Command(), poop, a), False)


class RecurringAvailabilityTest(TestCase):
    def setup_profiles(self):
        # tiffany, Success, SF, No, once a month
        Profile.objects.create(
            first_name='tiffany',
            last_name='qi',
            preferred_name='tiffany',
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

    # you'll have to change this
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
        self.assertEqual([av1, av2, av3], Command.create_availabilities(Command()))

    # you'll have to change this
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
        # self.assertEqual([av1, av2], Command.delete_availabilities(Command()))  # why not equal??


class HelpersTest(TestCase):
    def setup_profiles(self):
        # tiffany, Success, SF, No, once a month
        Profile.objects.create(
            first_name='tiffany',
            last_name='qi',
            preferred_name='tiffany',
            email='tiffany@TEST-mixpanel.com',
            department='Success',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            frequency='Once a month',
            date_entered_mixpanel=datetime.datetime(2016, 10, 31),
            distinct_id='tiffany'
        )
        # Tim, Engineering, New York, Yes, once a month
        Profile.objects.create(
            first_name='tim',
            last_name='trefen',
            preferred_name='tim',
            email='tim@TEST-mixpanel.com',
            department='Engineering',
            location='New York',
            google_hangout='Yes',
            timezone='EST',
            frequency='Once a month',
            date_entered_mixpanel=datetime.datetime(2013, 06, 01),
            distinct_id='tim'
        )
        # Karima, Success, Other, Yes, once a month
        Profile.objects.create(
            first_name='karima',
            last_name='el moujahid',
            preferred_name='karima',
            email='karima@TEST-mixpanel.com',
            department='Success',
            location='Other',
            google_hangout='Yes',
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

    # you'll have to change this
    def test_get_next_weekday(self):
        self.assertEqual(get_next_weekday('0', '12:00'), datetime.datetime(2017, 8, 7, 12, 0))
        self.assertEqual(get_next_weekday('1', '1:00'), datetime.datetime(2017, 8, 8, 1, 0))
        self.assertEqual(get_next_weekday('4', '15:30'), datetime.datetime(2017, 8, 11, 15, 30))
