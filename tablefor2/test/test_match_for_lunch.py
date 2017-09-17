from django.test import TestCase

from tablefor2.models import *
from tablefor2.management.commands.match_users import Command

import datetime
import pytz


class MatchTestCase(TestCase):
    mon = datetime.datetime(2018, 8, 21, 12, 0, tzinfo=pytz.UTC)
    tue = datetime.datetime(2018, 8, 22, 12, 0, tzinfo=pytz.UTC)
    wed = datetime.datetime(2018, 8, 23, 12, 0, tzinfo=pytz.UTC)
    thu = datetime.datetime(2018, 8, 24, 12, 0, tzinfo=pytz.UTC)
    fri = datetime.datetime(2018, 8, 25, 12, 0, tzinfo=pytz.UTC)

    profiles = {
        'christine': [datetime.datetime(2017, 7, 1), 'Engineering', 'TWF'],
        'jameson': [datetime.datetime(2017, 6, 1), 'Engineering', 'MTWRF'],
        'james': [datetime.datetime(2017, 6, 1), 'General & Administrative', 'MF'],
        'shimin': [datetime.datetime(2017, 4, 1), 'Engineering', 'TR'],
        'brooke': [datetime.datetime(2017, 3, 1), 'Sales', 'MTF'],
        'maddie': [datetime.datetime(2017, 2, 1), 'Success', 'MT'],
        'austin': [datetime.datetime(2017, 1, 31), 'Sales', 'MRF'],
        'rajiv': [datetime.datetime(2017, 1, 1), 'Engineering', 'W'],
        'jonathan': [datetime.datetime(2016, 12, 31), 'Engineering', 'W'],
        'kousha': [datetime.datetime(2016, 12, 1), 'Engineering', 'TW'],
        'lopa': [datetime.datetime(2016, 11, 30), 'General & Administrative', 'MTW'],
        'nicole': [datetime.datetime(2016, 11, 1), 'Design', 'MTW'],
        'tiffany': [datetime.datetime(2016, 10, 1), 'Support', 'MTR'],
        'janet': [datetime.datetime(2016, 8, 1), 'Engineering', 'TW'],
        'alex': [datetime.datetime(2016, 5, 1), 'General & Administrative', 'MWF'],
        'chi': [datetime.datetime(2016, 1, 1), 'Engineering', 'TW'],
        'joey': [datetime.datetime(2015, 7, 1), 'Success', 'MT'],
        'anthony': [datetime.datetime(2015, 4, 1), 'Sales', 'TWR'],
        'hilary': [datetime.datetime(2014, 11, 1), 'Support', 'TR'],
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
                frequency='Once a month',
                accept_matches='Yes'
            )

    def fresh_setup(self):
        self.init_profiles()
        for name, profile_values in self.profiles.iteritems():
            days = list(profile_values[2])
            for day in days:
                saved_day = ''
                if day == 'M':
                    saved_day = self.mon
                if day == 'T':
                    saved_day = self.tue
                if day == 'W':
                    saved_day = self.wed
                if day == 'R':
                    saved_day = self.thu
                if day == 'F':
                    saved_day = self.fri

                Availability.objects.create(
                    profile=Profile.objects.get(first_name=name),
                    time_available=saved_day,
                    time_available_utc=saved_day
                )

    def test_run_matches(self):
        '''
        Christine & Hilary - T
        Jameson & Anthony - T
        James & Joey - M
        Shimin & Tiffany - T
        Brooke & Chi - T
        Maddie & Alex F - M
        Austin & Nicole - M
        Rajiv & Lopa - W
        '''
        self.fresh_setup()
        christine = Profile.objects.get(first_name='christine')
        hilary = Profile.objects.get(first_name='hilary')
        jameson = Profile.objects.get(first_name='jameson')
        anthony = Profile.objects.get(first_name='anthony')
        james = Profile.objects.get(first_name='james')
        joey = Profile.objects.get(first_name='joey')
        shimin = Profile.objects.get(first_name='shimin')
        tiffany = Profile.objects.get(first_name='tiffany')
        brooke = Profile.objects.get(first_name='brooke')
        chi = Profile.objects.get(first_name='chi')
        maddie = Profile.objects.get(first_name='maddie')
        alex = Profile.objects.get(first_name='alex')
        austin = Profile.objects.get(first_name='austin')
        nicole = Profile.objects.get(first_name='nicole')
        rajiv = Profile.objects.get(first_name='rajiv')
        lopa = Profile.objects.get(first_name='lopa')

        christine_tue = Availability.objects.get(profile=christine, time_available_utc=self.tue)
        jameson_tue = Availability.objects.get(profile=jameson, time_available_utc=self.tue)
        james_mon = Availability.objects.get(profile=james, time_available_utc=self.mon)
        shimin_tue = Availability.objects.get(profile=shimin, time_available_utc=self.tue)
        brooke_tue = Availability.objects.get(profile=brooke, time_available_utc=self.tue)
        maddie_mon = Availability.objects.get(profile=maddie, time_available_utc=self.mon)
        austin_mon = Availability.objects.get(profile=austin, time_available_utc=self.mon)
        rajiv_wed = Availability.objects.get(profile=rajiv, time_available_utc=self.wed)

        matches = [
            [christine_tue, christine, hilary],
            [jameson_tue, jameson, anthony],
            [james_mon, james, joey],
            [shimin_tue, shimin, tiffany],
            [brooke_tue, brooke, chi],
            [maddie_mon, maddie, alex],
            [austin_mon, austin, nicole],
            [rajiv_wed, rajiv, lopa],
        ]

        self.assertEqual(Command.runs_matches(Command()), matches)
