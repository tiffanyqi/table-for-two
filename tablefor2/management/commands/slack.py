from __future__ import print_function
from django.core.management.base import BaseCommand

import json
from slackclient import SlackClient

from tablefor2.models import *
from tablefor2.settings import SLACK_TOKEN


class Command(BaseCommand):
    help = 'Pings Slack to see if people are at Mixpanel'

    def handle(self, *args, **options):
        employees = self.get_employees()
        self.check_profiles(employees)

    def get_employees(self):	
        """	
        Get a list of all employees from Slack	
        """	
        sc = SlackClient(SLACK_TOKEN)
        slack_users = sc.api_call("users.list")['members']
        current_directory = {}	
        for employee in slack_users:
            if not employee['deleted'] and not employee['is_bot'] and not employee['id'] == 'USLACKBOT' and not employee['is_restricted']:
                profile = employee.get('profile')
                if 'email' in profile.keys():
                    current_directory[profile['email']] = {	
                        'slack_id': employee['id']
                    }
        return current_directory	

    def check_profiles(self, employees):	
        """	
        Checks to see if the matching profiles are valid employees, otherwise	
        set to not accepting matches	
        """	
        for profile in Profile.objects.filter(frequency__gt=0):	
            try:	
                employees[profile.email]	
            except KeyError:	
                profile.frequency = 0	
                profile.save()	
                print("Deactivated " + profile.email)