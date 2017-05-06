from django.core.management.base import BaseCommand

from tablefor2.models import *

import datetime


class Command(BaseCommand):
    help = 'Matches users'
    '''
    Matching Process:
    - [ ] Runs this command at 3pm on all Availabilities that do not have
    a matched_name from tomorrow until a week from tomorrow.
    - [x] Prioritizes new Mixpanel hires.
    - [ ] Compares only users who have a different profile.department and
    do not have previous Availabilities with the same matched_name
    - [ ] Matches the user if they are in the same location first, else
    will check whether they are both open to a google_hangout
    - [ ] Check if they haven't been matched before
    - [ ] (V2) Ensure that the frequency has not yet been satisifed
    - [ ] If two users finally fits all all of these criteria, we'll take
    the two Availability models and set the matched_name and matched_email
    '''

    def handle(self, *args, **options):
        today = datetime.date.today()
        availabilities = Availability.objects.filter(time_available__gte=today, matched_name=None).order_by('time_available', '-profile__date_entered_mixpanel')

        # for every single availability in the future that hasn't been matched
        for availability in availabilities:
            time_available = availability.time_available
            current_times = Availability.objects.filter(time_available=time_available)

            # in every availability for the same time slot
            matches = []
            count = 0
            for av_a in current_times:
                count += 1
                for av_b in current_times[count:]:
                    profile_a = Profile.objects.get(email=av_a.profile)
                    profile_b = Profile.objects.get(email=av_b.profile)
                    # previous_matches

                    # if original was matched, match the other one too
                    if av_a in matches:
                        self.match_profile(av_a, av_b, matches)

                    # if both haven't been matched yet, check
                    elif av_a not in matches and av_b not in matches:
                        if profile_a.department != profile_b.department:
                            if profile_a.location == profile_b.location:
                                self.match_profile(av_a, av_b, matches)
                            elif profile_a.google_hangout == 'Yes' and profile_b.google_hangout == 'Yes':
                                self.match_profile(av_a, av_b, matches)

    def match_profile(self, av_a, av_b, matches):
        profile_b = av_b.profile
        av_a.matched_name = profile_b.preferred_name + ' ' + profile_b.last_name
        av_a.matched_email = profile_b.email
        av_a.save()
        matches.append(av_a)
