from tablefor2.forms import *
from tablefor2.models import *

import datetime
import pytz


# determines what the UTC equivalent of the original time is
def calculate_utc(profile, time_available):
    timezone = dict(TIMEZONES).get(profile.timezone)
    local = pytz.timezone(timezone)
    string = time_available.strftime("%Y-%m-%d %H:%M:%S")
    naive = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    local_datetime = local.localize(naive)
    return local_datetime.astimezone(pytz.utc)


# calculate individual times from 8AM to 6PM
def calculate_ampm():
    times = []
    for i in range(8, 18):
        ampm = ''
        num = i
        if i < 12:
            ampm = 'AM'
        elif i == 12:
            ampm = 'PM'
        else:
            ampm = 'PM'
            num -= 12

        hour = '%s%s' % (num, ampm)
        half = '%s:30%s' % (num, ampm)

        times.append(hour)
        times.append(half)

    return times


# calculate the output string back into military time
def determine_ampm(time_string):
    full_time = time_string[:-2]
    ampm = time_string[-2:]
    if ampm == 'AM' or time_string[0:2] == '12':
        return full_time
    else:
        hour, minute = full_time.split(":")
        hour = int(hour) + 12
        return '%s:%s' % (str(hour), minute)


def calculate_recurring_values(recurring):
    recurring_values = []
    for r in recurring:
        rec = "%s-%s" % (r.day, r.time)
        recurring_values.append(rec)
    return recurring_values
