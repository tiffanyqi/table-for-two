# Table For Two
===============

## TODOs
- [] Create home_logged_out page
- [] Create signup flow
- [] Connect to bambooHR?


## Features
- Connect data from bambooHR
- Set your profile settings (location? willing to google hangout if not in the same location?)
- Set your availability on calendar and see your Mixpanel calendar
- Get the set of people and match people based on diff division (Can't with the same person afterwards)
- With a match, send out a calendar invite
- Weekly email reminder to do a tf2 (Mixpanel? Or set calendar invite for 9am every Monday)


## Matching process

### Matching algorithm (in order)
- Runs a thing at 3pm the day before
- People who are available at the same time
- Are in a different division
- Haven't matched before
- Those who are in the same location (last, GHangout)

### Matching structure
{
	UNIX TIMESTAMP 1 --> [ [A, B], [C, D], [E, F] ],
	UNIX TIMESTAMP 2 --> [ [A, B], [C, D] ]
}

A = Person object with name, location, division, ghangout
UNIX TIMESTAMP = date and time of beginning 1/2 hour, assuming timeslot is half hour


## Database Schema
employee <--> employee
- first_name (string)
- last_name (string)
- name (string)
- email (string)
- division (string)
- location (string)
- current_matches (array of strings)
- previous_matches (array of strings)
- availability (array of timestamps)
- ghangout (boolean)


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
