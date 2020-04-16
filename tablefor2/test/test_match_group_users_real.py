from django.test import TestCase

import datetime
import json
import pytz

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command


class GroupMatchUsersTestCaseReal(TestCase):
    jul22 = datetime.datetime(2030, 7, 22, 19, 0, tzinfo=pytz.UTC)
    jul23 = datetime.datetime(2030, 7, 23, 19, 0, tzinfo=pytz.UTC)
    jul24 = datetime.datetime(2030, 7, 24, 19, 0, tzinfo=pytz.UTC)
    jul25 = datetime.datetime(2030, 7, 25, 19, 0, tzinfo=pytz.UTC)
    jul26 = datetime.datetime(2030, 7, 26, 19, 0, tzinfo=pytz.UTC)
    jul29 = datetime.datetime(2030, 7, 29, 19, 0, tzinfo=pytz.UTC)
    jul30 = datetime.datetime(2030, 7, 30, 19, 0, tzinfo=pytz.UTC)
    jul31 = datetime.datetime(2030, 7, 31, 19, 0, tzinfo=pytz.UTC)
    aug1 = datetime.datetime(2030, 8, 1, 19, 0, tzinfo=pytz.UTC)
    aug2 = datetime.datetime(2030, 8, 2, 19, 0, tzinfo=pytz.UTC)

    cst_jul22 = datetime.datetime(2030, 7, 22, 17, 0, tzinfo=pytz.UTC)
    cst_jul23 = datetime.datetime(2030, 7, 23, 17, 0, tzinfo=pytz.UTC)
    cst_jul24 = datetime.datetime(2030, 7, 24, 17, 0, tzinfo=pytz.UTC)
    cst_jul25 = datetime.datetime(2030, 7, 25, 17, 0, tzinfo=pytz.UTC)
    cst_jul26 = datetime.datetime(2030, 7, 26, 17, 0, tzinfo=pytz.UTC)
    cst_jul29 = datetime.datetime(2030, 7, 29, 17, 0, tzinfo=pytz.UTC)
    cst_jul30 = datetime.datetime(2030, 7, 30, 17, 0, tzinfo=pytz.UTC)
    cst_jul31 = datetime.datetime(2030, 7, 31, 17, 0, tzinfo=pytz.UTC)
    cst_aug1 = datetime.datetime(2030, 8, 1, 17, 0, tzinfo=pytz.UTC)
    cst_aug2 = datetime.datetime(2030, 8, 2, 17, 0, tzinfo=pytz.UTC)

    feb15 = datetime.datetime(2030, 2, 15, 20, 0, tzinfo=pytz.UTC)
    mar25 = datetime.datetime(2030, 3, 25, 19, 0, tzinfo=pytz.UTC)
    apr29 = datetime.datetime(2030, 4, 29, 19, 0, tzinfo=pytz.UTC)

    # setup
    def init_profiles(self):
        Profile.objects.create(
            first_name='Cherise',
            last_name='test',
            preferred_first_name='Cherise',
            email='cherise@TEST-mixpanel.com',
            department='Support',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            frequency=1,
            match_type='group',
            date_entered_mixpanel=datetime.datetime(2017, 8, 28),
            distinct_id='cherise'
        )
        Profile.objects.create(
            first_name='Rishi',
            last_name='test',
            preferred_first_name='Rishi',
            email='rishi@TEST-mixpanel.com',
            department='Support',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            frequency=1,
            match_type='group',
            date_entered_mixpanel=datetime.datetime(2019, 6, 3),
            distinct_id='rishi'
        )
        Profile.objects.create(
            first_name='Hannah',
            last_name='test',
            preferred_first_name='Hannah',
            email='Hannah@TEST-mixpanel.com',
            department='Marketing',
            location='San Francisco',
            timezone='PST',
            google_hangout='No',
            frequency=1,
            match_type='group',
            date_entered_mixpanel=datetime.datetime(2019, 2, 16),
            distinct_id='hannah'
        )
        Profile.objects.create(
            first_name='Lashay',
            last_name='test',
            preferred_first_name='Lashay',
            email='Lashay@TEST-mixpanel.com',
            department='Sales',
            location='San Francisco',
            timezone='PST',
            google_hangout='Yes',
            frequency=1,
            match_type='group',
            date_entered_mixpanel=datetime.datetime(2019, 6, 3),
            distinct_id='lashay'
        )
        Profile.objects.create(
            first_name='Anlu',
            last_name='test',
            preferred_first_name='Anlu',
            email='Anlu@TEST-mixpanel.com',
            department='Engineering',
            location='San Francisco',
            timezone='CST',
            google_hangout='Yes',
            frequency=4,
            match_type='group',
            date_entered_mixpanel=datetime.datetime(2011, 5, 1),
            distinct_id='Anlu'
        )
        Profile.objects.create(
            first_name='Anya',
            last_name='test',
            preferred_first_name='Anya',
            email='Anya@TEST-mixpanel.com',
            department='Marketing',
            location='San Francisco',
            timezone='PST',
            google_hangout='Yes',
            frequency=2,
            match_type='group',
            date_entered_mixpanel=datetime.datetime(2019, 7, 8),
            distinct_id='Anya'
        )

    def fresh_setup(self):
        self.init_profiles()
        availabilities_map = {
            'Cherise': [self.jul22, self.jul23, self.jul24, self.jul26, self.jul29, self.jul30, self.jul31, self.aug2],
            'Rishi': [self.jul22, self.jul23, self.jul24, self.jul26, self.jul29, self.jul30, self.jul31, self.aug2],
            'Hannah': [self.jul22, self.jul23, self.jul24, self.jul25, self.jul26, self.jul29, self.jul30, self.jul31, self.aug1, self.aug2],
            'Lashay': [self.jul23, self.jul30],
            'Anlu': [self.cst_jul22, self.cst_jul23, self.cst_jul24, self.cst_jul25, self.cst_jul26, self.cst_jul29, self.cst_jul30, self.cst_jul31, self.cst_aug1, self.cst_aug2],
            'Anya': [self.jul25, self.jul26, self.aug1, self.aug2],
        }
        for first_name, availabilities in availabilities_map.iteritems():
            for av in availabilities:
                GroupAvailability.objects.create(
                    profile=Profile.objects.get(first_name=first_name),
                    time_available=av,
                    time_available_utc=av
                )
        cherise = Profile.objects.get(first_name='Cherise')
        Availability.objects.create(
            profile=cherise,
            time_available=self.feb15,
            time_available_utc=self.feb15,
            matched_name='Andrew',
            matched_email='Andrew@test@mixpanel.com',
        )
        Availability.objects.create(
            profile=cherise,
            time_available=self.mar25,
            time_available_utc=self.mar25,
            matched_name='Brad',
            matched_email='Brad@test@mixpanel.com',
        )
        Availability.objects.create(
            profile=cherise,
            time_available=self.apr29,
            time_available_utc=self.apr29,
            matched_name='Jake',
            matched_email='Jake@test@mixpanel.com',
        )

    def test_match_and_run(self):
        self.fresh_setup()
        cherise = Profile.objects.get(first_name='Cherise')
        rishi = Profile.objects.get(first_name='Rishi')
        hannah = Profile.objects.get(first_name='Hannah')
        anya = Profile.objects.get(first_name='Anya')
        group = {self.jul26: [cherise, rishi, hannah, anya]}
        self.assertEqual(Command.run_group_matches(Command()), group)
