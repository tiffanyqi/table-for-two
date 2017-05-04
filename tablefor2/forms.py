from django import forms

from django.utils import timezone


DEPARTMENTS = (
    ('---', 'Select a Department'),
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

BOOLEANS = (
    ('-', 'Select a Choice'),
    ('Yes', 'Yes'),
    ('No', 'No')
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
        return department

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location == '--':
            raise forms.ValidationError('Please select your location.')
        return location

    def clean_google_hangout(self):
        google_hangout = self.cleaned_data.get('google_hangout')
        if google_hangout == '-':
            raise forms.ValidationError('Please select your Google Hangout preference.')
        return google_hangout

    def clean_date_entered_mixpanel(self):
        date_entered_mixpanel = self.cleaned_data.get('date_entered_mixpanel')
        if date_entered_mixpanel > timezone.now():
            raise forms.ValidationError("Please enter a valid Mixpanel start time! (You started in the future?)")
        return date_entered_mixpanel
