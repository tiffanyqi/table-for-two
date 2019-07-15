import datetime
import json
import pytz

from tablefor2.forms import TIMEZONES
from tablefor2.helpers import get_string_for_and_format
from tablefor2.models import Profile

# determines what the UTC equivalent of the original time is
def calculate_utc(profile, time_available):
    timezone = dict(TIMEZONES).get(profile.timezone)
    local = pytz.timezone(timezone)
    string = time_available.strftime("%Y-%m-%d %H:%M:%S")
    naive = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    local_datetime = local.localize(naive)
    return local_datetime.astimezone(pytz.utc)  # 2017-07-19 12:00:00+00:00


def get_names_from_group_avs(avs):
    names = ''
    for av in avs:
        name_string = ''
        emails = json.loads(av.matched_group_users)
        for i, email in enumerate(emails):
            prof = Profile.objects.get(email=email)
            name = '{} {}'.format(prof.preferred_first_name, prof.last_name)
            name_string += get_string_for_and_format(name, i, len(emails))
        names += name_string
    return names
