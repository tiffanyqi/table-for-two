from __future__ import print_function
from django.core.management.base import BaseCommand

from PyBambooHR import PyBambooHR

from tablefor2.models import *
from tablefor2.settings import BAMBOO_HR_API_KEY


class Command(BaseCommand):
    help = 'Pings BambooHR to see if people are at Mixpanel'

    def handle(self, *args, **options):
        employees = self.get_employees()
        self.check_profiles(employees)
        # print(employees)

    def get_employees(self):
        bamboo = PyBambooHR(subdomain='mixpanel', api_key=BAMBOO_HR_API_KEY)
        directory = bamboo.get_employee_directory()
        current_directory = {}
        for employee in directory:
            current_directory[employee.get('workEmail')] = {
                'bamboohr_id': employee.get('id'),
                'photo_url': employee.get('photoUrl')
            }
        return current_directory

    def check_profiles(self, employees):
        for profile in Profile.objects.filter(accept_matches='Yes'):
            try:
                employees[profile.email]
            except KeyError:
                profile.accept_matches = "No"
                profile.save()
                print("Deactivated " + profile.email)
