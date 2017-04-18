# Table For Two


## TODOs
- [x] Create home_logged_out page
- [x] Create database and model
- [ ] Create signup flow
- [ ] Connect to bambooHR?


## Features
- Connect data from bambooHR
- Set your profile settings (location? willing to google hangout if not in the same location?)
- Set your availability on calendar and see your Mixpanel calendar
- Get the set of people and match people based on diff division (Can't with the same person afterwards)
- With a match, send out a calendar invite
- Weekly email reminder to do a tf2 (Mixpanel? Or set calendar invite for 9am every Monday)


## Matching process

### Matching algorithm (in order)
- For every availability, create an Availability for that user (date and time of beginning 1/2 hour, assuming timeslot is half hour)
- Runs a thing at 3pm the day before
- People who are available at the same time
- Are in a different division
- Haven't matched before
- Those who are in the same location (last, GHangout)
- If that user is matched, then we'll set the name and email equal to the match

### Testing
```
from tablefor2.models import *
import datetime

t = Profile.objects.create(first_name='tiffany', email='tiffany.qi@mixpanel.com')
a = Profile.objects.create(first_name='andrew', email='andrew.huang@not-mixpanel.com')
dec_30_1pm = datetime.datetime(2016, 12, 30, 13)
dec_31_1pm = datetime.datetime(2016, 12, 31, 13)
tv1 = Availability.objects.create(profile=t, time_available=dec_30_1pm)
tv2 = Availability.objects.create(profile=t, time_available=dec_31_1pm)
av = Availability.objects.create(profile=a, time_available=dec_30_1pm)
Availability.objects.all()

Availability.objects.filter(time_available=dec_30_1pm)

tv1.matched_name = a.first_name
tv1.matched_email = a.email
av.matched_name = t.first_name
av.matched_email = t.email
```


## Signup process
- Connect to Mixpanel google account
- Takes email address from bambooHR and saves each field into app
- Takes availability from google calendar and displays it


## Views
- Home Logged Out
- Signup
    - Input email
    - Confirm bambooHR info
    - Add whether to googleHangout
- Home Logged In
    - See calendar
    - See previous people you've matched with
    - See who you're currently set up to match with
- Settings
    - Edit any info
    - See current info
