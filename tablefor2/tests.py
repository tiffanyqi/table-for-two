from django.test import TestCase
from tablefor2.models import *

import datetime


class MatchTestCase(TestCase):
    past = datetime.datetime(2016, 11, 5, 12, 0)
    future = datetime.datetime(2017, 11, 5, 12, 0)

    def setup(self):
        # none
        # none = Profile.objects.create(
        #     first_name=None,
        #     email=None,
        #     department=None,
        #     location=None,
        #     google_hangout=None,
        #     frequency=None,
        #     date_entered_mixpanel=None
        # )

        # tiffany, Success, SF, No, once a week
        t = Profile.objects.create(
            first_name='tiffany',
            email='tiffany.qi@mixpanel.com',
            department='Success',
            location='San Francisco',
            google_hangout='No',
            frequency='Once a week',
            date_entered_mixpanel=datetime.datetime(2016, 10, 31)
        )
        Availability.objects.create(
            profile=t,
            time_available=past
        )
        Availability.objects.create(
            profile=t,
            time_available=future
        )

        # andrew, Engineering, SF, No, once a week
        a = Profile.objects.create(
            first_name='andrew',
            email='andrew@not-mixpanel.com',
            department='Engineering',
            location='San Francisco',
            google_hangout='No',
            frequency='Once a week',
            date_entered_mixpanel=datetime.datetime(2016, 11, 01)
        )
        Availability.objects.create(
            profile=a,
            time_available=past
        )
        Availability.objects.create(
            profile=a,
            time_available=future
        )

        # PJ, Success, SF, No, once a week
        pj = Profile.objects.create(
            first_name='pj',
            email='pj@mixpanel.com',
            department='Success',
            location='San Francisco',
            google_hangout='Yes',
            frequency='Once a week',
            date_entered_mixpanel=datetime.datetime(2015, 11, 01)
        )
        Availability.objects.create(
            profile=pj,
            time_available=past
        )
        Availability.objects.create(
            profile=pj,
            time_available=future
        )

    def test_none_match(self):
        # none = Profile.objects.get(first_name=None)
        # run cron
        # assert availabilities are none

    def test_availability_match(self):
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        t_availability = Availability.objects.get(profile=t, time_available=future)
        a_availability = Availability.objects.get(profile=a, time_available=future)
        # run cron
        # assert that t_availability.matched_name = 'andrew'
        # assert that a_availability.matched_name = 'tiffany'

    def test_location_match(self):
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        t_availability = Availability.objects.get(profile=t, time_available=past)
        a_availability = Availability.objects.get(profile=a, time_available=past)
        pj_availability = Availability.objects.get(profile=pj, time_available=past)
        # run cron
        # assert that t_availability.matched_name = 'andrew'
        # assert that a_availability.matched_name = 'tiffany'
        # assert that pj_availability.matched_name = None

    def test_department_match(self):
        #hi

    def test_google_hangout_match(self):
        #hi

    def test_frequency_match(self):
        #hi

    def test_new_hire_match(self):
        #hi
