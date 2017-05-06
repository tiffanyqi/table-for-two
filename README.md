# Table For Two


## TODOs

Signup
- [x] Create database and model
- [x] Create signup flow
- [x] Create index-logged-out page
- [x] Ask for extra information (edit-profile)
- [x] Create the form and edit-profile page
- [x] Save user in database
- [x] Create profile page
- [x] Show existing profile in form
- [ ] Test

Availability
- [x] Create index-logged-in page
- [x] Set availabilities in back-end
- [x] Show you made these availabilities
- [ ] Test

Matching
- [ ] Match the people by availability (frequency V2)
- [x] Show your future matches
- [x] Show your previous matches
- [ ] Send a google calendar invite
- [ ] Change everything to proper timezone
- [ ] Test

Notifications
- [ ] Set notification based on frequency and current matchings


## Features
- Set your profile settings (location? willing to google hangout if not in the same location?)
- Set your availability on calendar
- Prioritize newer Mixpanel hires
- Set your frequency
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
- Newer Mixpanel hires
- Those who are in the same location (last, GHangout)
- If that user is matched, then we'll set the name and email equal to the match
- Only if fits their frequency

### Testing
```
from tablefor2.models import *
import datetime

d1 = datetime.datetime(2015, 1, 1)
d2 = datetime.datetime(2016, 1, 1)
t = Profile.objects.create(first_name='meh', email='meh.qi@mixpanel.com', date_entered_mixpanel=d1)
a = Profile.objects.create(first_name='andrew', email='andrew.huang@not-mixpanel.com', date_entered_mixpanel=d2)
past = datetime.datetime(2016, 12, 30, 13)
future = datetime.datetime(2017, 12, 31, 13)
tv1 = Availability.objects.create(profile=t, time_available=past)
tv2 = Availability.objects.create(profile=t, time_available=future)
av = Availability.objects.create(profile=a, time_available=future)
Availability.objects.all()

Availability.objects.filter(time_available=past)

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
- Index Logged Out
- Signup
    - Input email
    - Confirm and add info
- Index Logged In
    - See calendar
    - See previous people you've matched with
    - See who you're currently set up to match with
- Settings
    - Edit any info
    - See current info


# V2
- BambooHR instead?
- Variable locations?
- See your Mixpanel calendar
- Change frequencies

