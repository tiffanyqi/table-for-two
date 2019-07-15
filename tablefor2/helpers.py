import datetime

# calculate individual times from 8AM to 6PM
def calculate_ampm(match_type):
    times = []
    start_hour = 8 if match_type == 'one-on-one' else 12
    end_hour = 18 if match_type == 'one-on-one' else 13
    for i in range(start_hour, end_hour):
        ampm = ''
        num = i
        if i < 12:
            ampm = 'AM'
        elif i == 12:
            ampm = 'PM'
        else:
            ampm = 'PM'
            num -= 12

        hour = '%s:00%s' % (num, ampm)
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
        return '%s:%s' % (str(hour), minute)  # 13:00


# adds values for recurring in tables
def calculate_recurring_values(recurring):
    recurring_values = []
    for r in recurring:
        rec = "%s-%s" % (r.day, r.time)
        recurring_values.append(rec)
    return recurring_values


# find the next weekday after a given day, plus 7
# https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-a-date
def get_next_weekday(today, day, time):
    days_ahead = int(day) - today.weekday()
    next_weekday = today + datetime.timedelta(days_ahead+7)  # 2017-07-19 12:00:00+00:00

    time_string = time.split(':')
    return datetime.datetime.combine(next_weekday, datetime.time(int(time_string[0]), int(time_string[1])))

# returns a string somewhere in the position of 'string 1, string 2, and string 3'
def get_string_for_and_format(string, curr_index, array_len):
    if curr_index == array_len - 1:
        return 'and {}'.format(string)
    elif curr_index < array_len:
        return '{}, '.format(string)
