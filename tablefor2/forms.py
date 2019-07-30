from django import forms

from datetime import *


TEAMS = (
    ('--', 'Select a Team'),
    ('Design', 'Design'),
    ('Engineering', 'Engineering'),
    ('Product', 'Product'),
    ('General & Administrative', 'General & Administrative'),
    ('Marketing', 'Marketing'),
    ('Sales', 'Sales'),
    ('Success', 'Success'),
    ('Support', 'Support')
)

# Ensure in sync with match_users.py
LOCATIONS = (
    ('--', 'Select a Location'),
    ('San Francisco', 'San Francisco'),
    ('New York', 'New York'),
    ('Seattle', 'Seattle'),
    ('Austin', 'Austin'),
    ('London', 'London'),
    ('Paris', 'Paris'),
    ('Barcelona', 'Barcelona'),
    ('Singapore', 'Singapore'),
    ('Other', 'Other')
)

TIMEZONES = (
    ('--', 'Select your timezone'),
    ('EST', 'US/Eastern'),
    ('CST', 'US/Central'),
    ('MST', 'US/Mountain'),
    ('PST', 'US/Pacific'),
    ('BST', 'Europe/London'),
    ('CEST', 'Europe/Paris'),
    ('SGT', 'Singapore'),
)

LOCATION_TO_TIMEZONE = {
    'San Francisco': 'PST',
    'New York': 'EST',
    'Seattle': 'PST',
    'Austin': 'MST',
    'London': 'BST',
    'Paris': 'CEST',
    'Barcelona': 'CEST',
    'Singapore': 'SGT',
}

BOOLEANS = (
    ('--', 'Select a Choice'),
    ('Yes', 'Yes'),
    ('No', 'No')
)

MATCH_TYPES = (
    ('--', 'Select a Choice'),
    ('group', 'Group of four'),
    ('one-on-one', 'One on one'),
)

FREQUENCY = (
    ('--', 'Select a frequency per month'),
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
)


class ProfileForm(forms.Form):
    preferred_first_name = forms.CharField(max_length=50, help_text='First name only! Your last name is already recorded :)')
    department = forms.ChoiceField(label="Team", choices=TEAMS)
    location = forms.ChoiceField(choices=LOCATIONS)
    timezone = forms.ChoiceField(choices=TIMEZONES, help_text='Choose the closest city in your timezone')
    date_entered_mixpanel = forms.DateField(help_text='(When did you join Mixpanel? Format in MM/DD/YYYY or YYYY-MM-DD)')
    frequency = forms.ChoiceField(choices=FREQUENCY, help_text='How often do you want to participate?')
    match_type = forms.ChoiceField(choices=MATCH_TYPES, help_text='Choose your match preference. You can choose to be in a group or a one on one.')
    google_hangout = forms.ChoiceField(label="Video call", choices=BOOLEANS, help_text='If you are not matched with someone in your area, would you be willing to video call?')
    what_is_your_favorite_movie = forms.CharField(label="Favorite movie", max_length=50, required=False, help_text='You have 50 characters!', widget=forms.TextInput(attrs={'maxlength': 50}))
    name_a_fun_fact_about_yourself = forms.CharField(label="Fun fact about yourself", max_length=50, required=False, help_text='You have 50 characters!', widget=forms.TextInput(attrs={'maxlength': 50}))
    distinct_id = forms.CharField(widget=forms.HiddenInput(), label='')

    def clean_department(self):
        department = self.cleaned_data.get('department')
        if department == '--':
            raise forms.ValidationError('Please select your team.')
        return department

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location == '--':
            raise forms.ValidationError('Please select your location.')
        return location

    def clean_timezone(self):
        timezone = self.cleaned_data.get('timezone')
        location = self.cleaned_data.get('location')
        if timezone == '--':
            raise forms.ValidationError('Please select the closest city in your timezone.')
        elif location != '--' and location != 'Other' and LOCATION_TO_TIMEZONE[location] != timezone:
            raise forms.ValidationError('Please change the timezone to match your city.')
        return timezone

    def clean_google_hangout(self):
        google_hangout = self.cleaned_data.get('google_hangout')
        if google_hangout == '--':
            raise forms.ValidationError('Please select your video calling preference.')
        return google_hangout

    def clean_frequency(self):
        frequency = self.cleaned_data.get('frequency')
        if frequency == '--':
            raise forms.ValidationError('Please select your frequency per month to participate.')
        return frequency

    def clean_match_type(self):
        match_type = self.cleaned_data.get('match_type')
        if match_type == '--':
            raise forms.ValidationError('Please select your type of match.')
        return match_type

    def clean_date_entered_mixpanel(self):
        date_entered_mixpanel = self.cleaned_data.get('date_entered_mixpanel')
        if date_entered_mixpanel > date.today():
            raise forms.ValidationError("Please enter a valid Mixpanel start time! (You started in the future?)")
        return date_entered_mixpanel
