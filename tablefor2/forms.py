from django import forms


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
    ghangout = forms.ChoiceField(choices=BOOLEANS)
    date_entered_mixpanel = forms.DateTimeField()

    def clean_profile(self):
        department = self.cleaned_date.get('department')
        location = self.cleaned_date.get('location')
        ghangout = self.cleaned_date.get('ghangout')
        date_entered_mixpanel = self.cleaned_date.get('date_entered_mixpanel')

        if department == self.fields['department'].choices[0][0]:
            raise forms.ValidationError('This field is required')
