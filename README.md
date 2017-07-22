# Table For Two

Table for Two is a web app that allows Mixpanelers the chance to meet with other Mixpanelers from different departments whenever they'd like. It prioritizes new hires, and allows lunch and coffee dates in 30 minute increments.

## Features
- Set your own recurring availability
- Set your own profile settings (location? google hangout?)
- Matches folks automatically and puts the event on the calendar


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

Availability / Recurring Availability
- [x] Create front-end for availabilities
- [x] Save recurring availabilities in the back-end
- [x] Edit availabilities
- [x] Test

Matching
- [x] Match the people by availability and 1x/wk (frequency V2)
- [x] Show your future matches
- [x] Show your previous matches
- [x] Send a google calendar invite
- [x] Change everything to proper timezone
- [x] Option to turn off matching if you want to stop or you're OOO
- [ ] Refactor to add user_request_type
- [ ] Refactor to once a month
- [ ] Run the actual cron job
- [x] Test

Mixpanel
- Goal: acquisition
- [X] Signup flow (index -> signup -> profile -> save)
- [X] identify
- [ ] Save recurring availability --> double, weird
- [X] Match made / invite sent (server-side)
- [X] People prop: email, dept, etc, number of matches, number of availabilities
- [ ] Notifications - onboarding, OOO

Front-end
- PRETTIFY
- [ ] index-logged-out
- [X] index-logged-in
- [X] edit-profile
- [ ] edit-availability
- [ ] Show EMEA/NYC/SF friendly days and fix table
- [ ] tool tips to onboard users about things
- [ ] connect to heroku properly --> calendar still weird


## Matching process
- For every recurring availability, create an Availability for that user (date and time of beginning 1/2 hour, assuming timeslot is half hour)
- Runs a thing at 3pm the day before
- First pick are the newer Mixpanel hires
- Check for:
    - If a user is currently accepting matches
	- Only if fits their frequency of 1x/wk (V2 will be programmatic)
	- People who are available at the same time
	- Are in a different department
	- Haven't matched before
	- Those who are in the same location (last, GHangout)
	- User can choose between veterans or new hires
- If that user is matched, then we'll set the name and email equal to the match


## Mixpanel Implementation

### Events
- Page Viewed
	- Index-logged-out (home page)
	- Index-logged-in (dashboard)
	- Edit-availability (edit availability)
	- Edit-profile (edit profile)
- Profile Created
- Recurring Availability Saved
- Match Created
- Calendar Invite Sent

### Properties
- Page Viewed
	- Page
- Profile Created
- Recurring Availability Saved
- Match Created (2)
	- Current User Department
	- Current User Location
	- Other User Department
	- Other User Location
	- Google Hangout or In Person
- Calendar Invite Sent (2)
	- Time
	- Timezone
- People
	- $first_name
	- $last_name
	- Preferred Name
	- $email
	- Department
	- Accepting Matches
	- Location
	- Timezone
	- Frequency
	- Date Entered Mixpanel
	- Number of Matches
	- Number of Recurring Availabilities
	- Last Match Created
	- Date Joined

### Other Implementation Details
- saving of distinct_id
- identify on db's distinct_id
- clear cookie upon logout


# V2
- BambooHR instead?
- Variable locations?
- See your Mixpanel calendar
- Programmatic frequencies
- [ ] Build in OOOs?
- User request types?

