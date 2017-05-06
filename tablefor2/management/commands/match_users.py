from django.core.management.base import BaseCommand, CommandError

from tablefor2.forms import *


class Command(BaseCommand):
    help = 'Matches users'
    '''
    Matching Process:
    - Runs this command at 3pm on all Availabilities that do not have
    a matched_name from tomorrow until a week from tomorrow.
    - Compares only users who have a different profile.department and
    do not have previous Availabilities with the same matched_name
    - Matches the user if they are in the same location first, else
    will check whether they are both open to a google_hangout
    - Prioritizes new Mixpanel hires.
    - Ensure that the frequency has not yet been satisifed
    - If two users finally fits all all of these criteria, we'll take
    the two Availability models and set the matched_name and matched_email
    '''

    def handle(self, *args, **options):
        # time_available__gte date.today()
        availabilities = Availability.objects.all()  # filter
        for availability in availabilities:
            profile = availability.profile
            time_available = availability.time_available
            same_times = Availability.objects.filter(time_available=time_available)
