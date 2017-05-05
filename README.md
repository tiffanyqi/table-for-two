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

Availability
- [x] Create index-logged-in page
- [x] Set availabilities in back-end
- [x] Show you made these availabilities

Matching
- [ ] Match the people by availability and frequency
- [ ] Show your future matches
- [ ] Show your previous matches
- [ ] Send a google calendar invite

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

