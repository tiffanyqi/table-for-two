from django.core.management import call_command
from django.test import TestCase
from tablefor2.models import *

import datetime


class MatchTestCase(TestCase):
    past = datetime.datetime(2016, 11, 5, 12, 0)
    future = datetime.datetime(2017, 11, 5, 12, 0)

    # https://hprog99.wordpress.com/2014/08/14/how-to-setup-django-cron-jobs/comment-page-1/

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

   #  def test_none_match(self):
        # none = Profile.objects.get(first_name=None)
        # run cron
        # assert availabilities are none

    def test_availability_match(self):
        self.setup()
        t = Profile.objects.get(first_name='tiffany')
        a = Profile.objects.get(first_name='andrew')
        t_availability = Availability.objects.get(profile=t, time_available=self.future)
        a_availability = Availability.objects.get(profile=a, time_available=self.future)

        call_command('match_users')
        self.assertEqual(t_availability.matched_name, 'andrew huang')
        self.assertEqual(a_availability.matched_name, 'tiffany qi')

    def test_location_match(self):
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

    # def test_department_match(self):
        #hi

    # def test_google_hangout_match(self):
        #hi

    # def test_frequency_match(self):
        #hi

    # def test_new_hire_match(self):
        #hi

    # def test_not previous_match(self):
        #hi
