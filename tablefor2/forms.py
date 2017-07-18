from django import forms

from datetime import *


DEPARTMENTS = (  # change these departments
    ('--', 'Select a Department'),
    ('Engineering', 'Engineering'),
    ('General & Administrative', 'General & Administrative'),
    ('Marketing', 'Marketing'),
    ('Success', 'Success')
)

LOCATIONS = (
    ('--', 'Select a Location'),
    ('San Francisco', 'San Francisco'),
    ('New York', 'New York'),
    ('Seattle', 'Seattle'),
    ('Lehi', 'Lehi'),
    ('Other', 'Other')
)

TIMEZONES = (
    ('--', 'Select your timezone by closest city'),
    ('EST (New York)', 'US/Eastern'),
    ('CST (Chicago)', 'US/Central'),
    ('MST (Denver, Lehi)', 'US/Mountain'),
    ('PST (San Francisco, Seattle)', 'US/Pacific'),
    ('BST (London)', 'Europe/London'),
    ('CEST (Barcelona, Madrid, Paris, Amsterdam)', 'Europe/Amsterdam'),
)

BOOLEANS = (
    ('--', 'Select a Choice'),
    ('Yes', 'Yes'),
    ('No', 'No')
)

FREQUENCY = (
    # ('--', 'Select a Frequency'),
    ('Once a week', 'Once a week'),
    # ('Once every other week', 'Once every other week'),
    # ('Once a month', 'Once a month')
)


class ProfileForm(forms.Form):
    preferred_name = forms.CharField(max_length=50)
    department = forms.ChoiceField(choices=DEPARTMENTS)
    location = forms.ChoiceField(choices=LOCATIONS)
    accept_matches = forms.ChoiceField(choices=BOOLEANS, help_text="Choose 'Yes' if you are just starting!")
    timezone = forms.ChoiceField(choices=TIMEZONES, help_text='Choose the closest city in your timezone')
    google_hangout = forms.ChoiceField(choices=BOOLEANS, help_text='If you are not matched with someone in your area, would you be willing to Google Hangout?')
    frequency = forms.ChoiceField(choices=FREQUENCY, help_text='How often do you want to participate?')
    date_entered_mixpanel = forms.DateField(help_text='(MM/DD/YYYY or YYYY-MM-DD)')
    what_is_your_favorite_animal = forms.CharField(max_length=50, help_text='You have 50 characters!')
    name_a_fun_fact_about_yourself = forms.CharField(max_length=50, help_text='You have 50 characters!')
    distinct_id = forms.CharField(widget=forms.HiddenInput(), label='')
    initial_referrer = forms.CharField(widget=forms.HiddenInput(), label='')
    initial_referring_domain = forms.CharField(widget=forms.HiddenInput(), label='')

    def clean_department(self):
        department = self.cleaned_data.get('department')
        if department == '--':
            raise forms.ValidationError('Please select your department.')
        return department

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location == '--':
            raise forms.ValidationError('Please select your location.')
        return location

    def clean_timezone(self):
        timezone = self.cleaned_data.get('timezone')
        if timezone == '--':
            raise forms.ValidationError('Please select the closest city in your timezone.')
        return timezone

    def clean_google_hangout(self):
        google_hangout = self.cleaned_data.get('google_hangout')
        if google_hangout == '--':
            raise forms.ValidationError('Please select your Google Hangout preference.')
        return google_hangout

    def clean_accept_matches(self):
        accept_matches = self.cleaned_data.get('accept_matches')
        if accept_matches == '--':
            raise forms.ValidationError("Please select your matching preference. Select 'Yes' if you're just starting!")
        return accept_matches

    def clean_frequency(self):
        frequency = self.cleaned_data.get('frequency')
        if frequency == '--':
            raise forms.ValidationError('Please select your frequency to participate.')
        return frequency

    def clean_date_entered_mixpanel(self):
        date_entered_mixpanel = self.cleaned_data.get('date_entered_mixpanel')
        if date_entered_mixpanel > date.today():
            raise forms.ValidationError("Please enter a valid Mixpanel start time! (You started in the future?)")
        return date_entered_mixpanel
