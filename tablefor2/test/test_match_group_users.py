from django.test import TestCase

import datetime
import json
import pytz

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command


class GroupMatchUsersTestCase(TestCase):
    past = datetime.datetime(2016, 11, 5, 12, 0, tzinfo=pytz.UTC)  # 1478347200
    future = datetime.datetime(2019, 11, 1, 12, 0, tzinfo=pytz.UTC)
    future2 = datetime.datetime(2019, 11, 2, 12, 0, tzinfo=pytz.UTC)
    first_names = ['tiffany', 'andrew', 'philip', 'karima', 'tim', 'michael']

    # setup
    def init_profiles(self):
        """
        Tiffany - group, success, PST
        Andrew - group, eng, PST
        PJ - group, success, PST
        Karima - group, success, CEST
        Tim - group, eng, PST
        Mike - group, sales, PST
        """

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
            frequency=1,
            match_type='group',
            date_entered_mixpanel=datetime.datetime(2016, 10, 31),
            distinct_id='tiffany'
        )
        # andrew, Engineering, SF, No, once a month
        Profile.objects.create(
            first_name='andrew',
            last_name='test',
            preferred_first_name='andrew',
            email='andrew@not-TEST-mixpanel.com',
            department='Engineering',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            match_type='group',
            frequency=1,
            date_entered_mixpanel=datetime.datetime(2016, 11, 1),
            distinct_id='andrew'
        )
        # PJ, Success, SF, Yes, once a month
        Profile.objects.create(
            first_name='philip',
            last_name='test',
            preferred_first_name='pj',
            email='pj@TEST-mixpanel.com',
            department='Success',
            location='San Francisco',
            timezone='PST',
            match_type='group',
            google_hangout='Yes',
            frequency=1,
            date_entered_mixpanel=datetime.datetime(2015, 11, 1),
            distinct_id='pj'
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
            match_type='group',
            timezone='CEST',
            frequency=1,
            date_entered_mixpanel=datetime.datetime(2016, 6, 1),
            distinct_id='karima'
        )
        # Tim, Engineering, PST, Yes, once a month
        Profile.objects.create(
            first_name='tim',
            last_name='test',
            preferred_first_name='tim',
            email='tim@TEST-mixpanel.com',
            department='Engineering',
            location='San Francisco',
            google_hangout='Yes',
            match_type='group',
            timezone='PST',
            frequency=1,
            date_entered_mixpanel=datetime.datetime(2013, 6, 1),
            distinct_id='tim'
        )
        # Mike, Sales, SF, Yes, once a month
        Profile.objects.create(
            first_name='michael',
            last_name='test',
            preferred_first_name='mike',
            email='mike@TEST-mixpanel.com',
            department='Sales',
            location='San Francisco',
            timezone='PST',
            google_hangout='Yes',
            match_type='group',
            frequency=1,
            date_entered_mixpanel=datetime.datetime(2016, 1, 1),
            distinct_id='mike'
        )

    def fresh_setup(self):
        self.init_profiles()
        availabilities_map = {
            'tiffany': [self.future, self.future2],
            'andrew': [self.future, self.future2],
            'philip': [self.future, self.future2],
            'karima': [self.future],
            'tim': [self.future2],
            'michael': [self.future, self.future2],
        }
        for first_name, availabilities in availabilities_map.iteritems():
            GroupAvailability.objects.create(
                profile=Profile.objects.get(first_name=first_name),
                time_available=self.past,
                time_available_utc=self.past
            )
            for av in availabilities:
                GroupAvailability.objects.create(
                    profile=Profile.objects.get(first_name=first_name),
                    time_available=av,
                    time_available_utc=av
                )

    # tests

    # case where users don't have any matches in the beginning
    def test_check_group_match(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')
        t_av = GroupAvailability.objects.get(profile=t, time_available_utc=self.future)
        a_av = GroupAvailability.objects.get(profile=a, time_available_utc=self.future)
        pj_av = GroupAvailability.objects.get(profile=pj, time_available_utc=self.future)
        k_av = GroupAvailability.objects.get(profile=k, time_available_utc=self.future)
        tim_av = GroupAvailability.objects.get(profile=tim, time_available_utc=self.future2)
        mike_av = GroupAvailability.objects.get(profile=mike, time_available_utc=self.future)

        group = []
        self.assertEqual(Command.check_fuzzy_match(Command(), t, t_av, group), True)
        group.append(t)
        self.assertEqual(Command.check_fuzzy_match(Command(), a, a_av, group), True)
        group.append(a)
        self.assertEqual(Command.check_fuzzy_match(Command(), pj, pj_av, group), True)
        group.append(pj)
        self.assertEqual(Command.check_fuzzy_match(Command(), k, k_av, group), False)
        self.assertEqual(Command.check_fuzzy_match(Command(), tim, tim_av, group), True)
        group.append(tim)
        self.assertEqual(Command.check_fuzzy_match(Command(), mike, mike_av, group), True) # actually true for the way we limit on run matches not check fuzzy match

    def test_match_and_run_fresh_first_day(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        tim = Profile.objects.get(first_name='tim')
        group = {self.future2: [t, a, pj, tim]}
        self.assertEqual(Command.run_group_matches(Command()), group)

    def test_check_fuzzy_departments(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')

        group = []
        self.assertEqual(Command.check_fuzzy_departments(Command(), t, group), True)
        group.append(t)
        self.assertEqual(Command.check_fuzzy_departments(Command(), a, group), True)
        group.append(a)
        self.assertEqual(Command.check_fuzzy_departments(Command(), pj, group), True)
        group.append(pj)
        self.assertEqual(Command.check_fuzzy_departments(Command(), k, group), False)
        self.assertEqual(Command.check_fuzzy_departments(Command(), mike, group), True)

    def test_check_not_currently_matched(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        t_av = GroupAvailability.objects.get(profile=t, time_available_utc=self.future)
        a_av = GroupAvailability.objects.get(profile=a, time_available_utc=self.future)
        pj_av = GroupAvailability.objects.get(profile=pj, time_available_utc=self.future)

        # case where users don't have any matches in the beginning
        self.assertEqual(Command.check_not_currently_matched(Command(), a_av), True)
        self.assertEqual(Command.check_not_currently_matched(Command(), t_av), True)
        self.assertEqual(Command.check_not_currently_matched(Command(), pj_av), True)

    def test_frequency(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        t_av = GroupAvailability.objects.get(profile=t, time_available_utc=self.future)
        self.assertEqual(Command.check_frequency(Command(), t_av, t), True)

    def test_group_match(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        matches = [t, a, pj, k]
        emails = [t.email, a.email, pj.email, k.email]
        Command.match_group(Command(), self.past, matches)
        for prof in matches:
            av = GroupAvailability.objects.get(time_available_utc=self.past, profile=prof)
            self.assertEqual(av.matched_group_users, json.dumps(emails))

    def test_check_fuzzy_previous_matches(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')

        group = [t]
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), tim, group), True)
        group = [a, pj]
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), tim, group), True)

        group = [t, a, pj, k]
        Command.match_group(Command(), self.past, group)
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), tim, group), True)
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), t, group), False)
        group = [t, pj, k]
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), a, group), False)
        group = [t]
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), a, group), True)

    def test_check_fuzzy_double_previous_matches(self):
        self.fresh_setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        pj = Profile.objects.get(first_name='philip')
        k = Profile.objects.get(first_name='karima')
        tim = Profile.objects.get(first_name='tim')
        mike = Profile.objects.get(first_name='michael')

        matches = [t, a, pj, k]
        emails = [prof.email for prof in matches]
        for prof in matches:
            av = GroupAvailability.objects.get(time_available_utc=self.past, profile=prof)
            av.matched_group_users = json.dumps(emails)
            av.save()

        new_matches = [tim, a, pj, mike]
        Command.match_group(Command(), self.future2, new_matches)
        group = [t]
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), tim, group), True)
        group = [a, pj]
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), tim, group), False)
        group = [a, t]
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), mike, group), True)
        group = [a, t, k]
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), mike, group), True)
        group = [mike, t, a]
        self.assertEqual(Command.check_fuzzy_previous_matches(Command(), k, group), False)
