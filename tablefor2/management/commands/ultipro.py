from __future__ import print_function
from django.core.management.base import BaseCommand

import urllib2

from tablefor2.models import *
# from tablefor2.settings import BAMBOO_HR_API_KEY


class Command(BaseCommand):
    help = 'Pings UltiPro to see if people are at Mixpanel'
    HOST = 'https://service2.ultipro.com/'
    person_details_url = 'personnel/v1/person-details'

    def handle(self, *args, **options):
        employees = self.get_employees()
        print(employees)
        # self.check_profiles(employees)

    def get_employees(self):
        url = self.HOST + self.person_details_url
        print(url)
        content = urllib2.urlopen(self.HOST + self.person_details_url).read()
        return content
        # bamboo = PyBambooHR(subdomain='mixpanel', api_key=BAMBOO_HR_API_KEY)
        # directory = bamboo.get_employee_directory()
        current_directory = {}
        # for employee in directory:
        #     try:
        #         current_directory[employee.get('workEmail').lower()] = {
        #             'bamboohr_id': employee.get('id')
        #         }
        #     except AttributeError:
        #         pass
        # return current_directory

    def check_profiles(self, employees):
        for profile in Profile.objects.filter(accept_matches='Yes'):
            try:
                employees[profile.email]
            except KeyError:
                profile.accept_matches = "No"
                profile.save()
                print("Deactivated " + profile.email)
