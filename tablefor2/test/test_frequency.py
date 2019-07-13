from django.test import TestCase

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command

import datetime
import pytz


class FrequencyTestCase(TestCase):
    start = datetime.datetime(2016, 1, 1)
    week1 = datetime.datetime(2030, 11, 2, 12, 0, tzinfo=pytz.UTC)
    week2 = datetime.datetime(2030, 11, 14, 12, 0, tzinfo=pytz.UTC)
    week3 = datetime.datetime(2030, 11, 21, 12, 0, tzinfo=pytz.UTC)
    week4 = datetime.datetime(2030, 11, 28, 12, 0, tzinfo=pytz.UTC)

    profiles = {
        'none': [start, 'Engineering', 0],
        'one': [start, 'Sales', 1],
        'two': [start, 'General & Administrative', 2],
        'three': [start, 'Support', 3],
        'four': [start, 'Design', 4],
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
                frequency=profile_values[2],
            )

    def fresh_setup(self):
        self.init_profiles()
        weeks = [self.week1, self.week2, self.week3, self.week4]
        for name, profile_values in self.profiles.iteritems():
            for week in weeks:
                Availability.objects.create(
                    profile=Profile.objects.get(first_name=name),
                    time_available=week,
                    time_available_utc=week
                )

    def test_frequencies(self):
        self.fresh_setup()
        none_p = Profile.objects.get(first_name='none')
        one_p = Profile.objects.get(first_name='one')
        two_p = Profile.objects.get(first_name='two')
        three_p = Profile.objects.get(first_name='three')
        four_p = Profile.objects.get(first_name='four')

        none_p_av = Availability.objects.get(profile=none_p, time_available_utc=self.week1)
        one_p_av_1 = Availability.objects.get(profile=one_p, time_available_utc=self.week1)
        two_p_av_1 = Availability.objects.get(profile=two_p, time_available_utc=self.week1)
        three_p_av_1 = Availability.objects.get(profile=three_p, time_available_utc=self.week1)
        four_p_av_1 = Availability.objects.get(profile=four_p, time_available_utc=self.week1)
        one_p_av_2 = Availability.objects.get(profile=one_p, time_available_utc=self.week2)
        two_p_av_2 = Availability.objects.get(profile=two_p, time_available_utc=self.week2)
        three_p_av_2 = Availability.objects.get(profile=three_p, time_available_utc=self.week2)
        four_p_av_2 = Availability.objects.get(profile=four_p, time_available_utc=self.week2)
        one_p_av_3 = Availability.objects.get(profile=one_p, time_available_utc=self.week3)
        two_p_av_3 = Availability.objects.get(profile=two_p, time_available_utc=self.week3)
        three_p_av_3 = Availability.objects.get(profile=three_p, time_available_utc=self.week3)
        four_p_av_3 = Availability.objects.get(profile=four_p, time_available_utc=self.week3)
        one_p_av_4 = Availability.objects.get(profile=one_p, time_available_utc=self.week4)
        two_p_av_4 = Availability.objects.get(profile=two_p, time_available_utc=self.week4)
        three_p_av_4 = Availability.objects.get(profile=three_p, time_available_utc=self.week4)
        four_p_av_4 = Availability.objects.get(profile=four_p, time_available_utc=self.week4)

        self.assertEqual(Command.check_frequency(Command(), none_p_av, none_p), True) # because we filter out this elsewhere
        self.assertEqual(Command.check_frequency(Command(), one_p_av_1, one_p), True)

        # case where users just were matched
        one_p_av_1.matched_name = 'two test'
        one_p_av_1.matched_email = 'two@not-TEST-mixpanel.com'
        one_p_av_1.save()
        two_p_av_1.matched_name = 'one test'
        two_p_av_1.matched_email = 'one@not-TEST-mixpanel.com'
        two_p_av_1.save()
        three_p_av_1.matched_name = 'four test'
        three_p_av_1.matched_email = 'four@not-TEST-mixpanel.com'
        three_p_av_1.save()
        four_p_av_1.matched_name = 'three test'
        four_p_av_1.matched_email = 'three@not-TEST-mixpanel.com'
        four_p_av_1.save()

        self.assertEqual(Command.check_frequency(Command(), one_p_av_1, one_p), False)
        self.assertEqual(Command.check_frequency(Command(), two_p_av_1, two_p), False)
        self.assertEqual(Command.check_frequency(Command(), three_p_av_1, three_p), False)
        self.assertEqual(Command.check_frequency(Command(), four_p_av_1, four_p), False)

        self.assertEqual(Command.check_frequency(Command(), one_p_av_2, one_p), False)
        self.assertEqual(Command.check_frequency(Command(), two_p_av_2, two_p), False)
        self.assertEqual(Command.check_frequency(Command(), three_p_av_2, three_p), False)
        self.assertEqual(Command.check_frequency(Command(), four_p_av_2, four_p), True)

        self.assertEqual(Command.check_frequency(Command(), one_p_av_3, one_p), False)
        self.assertEqual(Command.check_frequency(Command(), two_p_av_3, two_p), False)
        self.assertEqual(Command.check_frequency(Command(), three_p_av_3, three_p), True)
        self.assertEqual(Command.check_frequency(Command(), four_p_av_3, four_p), True)

        self.assertEqual(Command.check_frequency(Command(), one_p_av_4, one_p), False)
        self.assertEqual(Command.check_frequency(Command(), two_p_av_4, two_p), True)
        self.assertEqual(Command.check_frequency(Command(), three_p_av_4, three_p), True)
        self.assertEqual(Command.check_frequency(Command(), four_p_av_4, four_p), True)
