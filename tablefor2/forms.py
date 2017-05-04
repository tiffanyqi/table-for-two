from django import forms

from django.utils import timezone


DEPARTMENTS = (
    ('---', 'Select a Department'),
    ('ENG', 'Engineering'),
    ('G&A', 'General & Administrative'),
    ('MAR', 'Marketing'),
    ('SUC', 'Success')
)

# BOAS (6)
# Commercial Sales (18),
# Content Marketing (4),
# Corporate Marketing (1),
# Customer Success Management (25),
# Demand Gen (1),
# Design (9),
# Enterprise Sales (14),
# Finance (15),
# G & A Admin (3),
# Legal (4),
# Machine Learning (7),
# Marketing Admin (3),
# People and Culture (5),
# Product Engineering (27),
# Product Marketing (4),
# Support (28),
# Sales Admin (3),
# Sales Development (14),
# Sales Enablement (5),
# Sales Engineering (10),
# Site Reliability Engineering (3),
# Solutions Architects (7),
# Strategic Sales (5),
# Systems Engineering (14),
# Talent Acquisition (11),
# Workplace (4),


LOCATIONS = (
    ('--', 'Select a Location'),
    ('SF', 'San Francisco'),
    ('NY', 'New York'),
    ('SE', 'Seattle'),
    ('LE', 'Lehi'),
    ('OT', 'Other')
)

BOOLEANS = (
    ('-', 'Select a Choice'),
    ('Y', 'Yes'),
    ('N', 'No')
)


class ProfileForm(forms.Form):
    preferred_name = forms.CharField(max_length=50)
    department = forms.ChoiceField(choices=DEPARTMENTS)
    location = forms.ChoiceField(choices=LOCATIONS)
    google_hangout = forms.ChoiceField(choices=BOOLEANS, help_text='If you are not matched with someone in your area, would you be willing to Google Hangout?')
    date_entered_mixpanel = forms.DateTimeField(help_text='(MM/DD/YYYY)')

    def clean_department(self):
        department = self.cleaned_data.get('department')
        if department == '---':
            raise forms.ValidationError('Please select your department.')

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location == '--':
            raise forms.ValidationError('Please select your location.')

    def clean_google_hangout(self):
        google_hangout = self.cleaned_data.get('google_hangout')
        if google_hangout == '-':
            raise forms.ValidationError('Please select your Google Hangout preference.')

    def clean_date_entered_mixpanel(self):
        date_entered_mixpanel = self.cleaned_data.get('date_entered_mixpanel')
        if date_entered_mixpanel > timezone.now():
            raise forms.ValidationError("Please enter a valid Mixpanel start time! (You started in the future?)")
