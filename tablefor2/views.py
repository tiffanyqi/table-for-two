from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from tablefor2.forms import *
from tablefor2.helpers import calculate_ampm, calculate_recurring_values
from tablefor2.models import *

import time


def index(request):
    try:
        # does the profile exist?
        profile = Profile.objects.get(email=request.user.email)
        recurring = RecurringAvailability.objects.filter(profile=profile)
        times = calculate_ampm()

        # force users to add more info
        if not profile.extra_saved_information:
            return HttpResponseRedirect('/profile/edit')
        if not recurring:
            return HttpResponseRedirect('/availability/edit')

        # show profile and availability and matches!
        else:
            today = date.today()
            current_matches = Availability.objects.filter(profile=profile, time_available__gte=today).exclude(matched_name=None) or None
            availabilities = Availability.objects.filter(profile=profile, time_available__gte=today).order_by('time_available') or None
            recurring_values = calculate_recurring_values(recurring)

            return render(request, 'tablefor2/index-logged-in.html', {
                'profile': profile,
                'availabilities': availabilities,
                'current_matches': current_matches,
                'recurring': recurring,
                'recurring_values': recurring_values,
                'times': times,
            })

    except:
        return render(request, 'tablefor2/index-logged-out.html')


# prepares the edit screen for recurring availability
@login_required
def edit_availability(request):
    profile = Profile.objects.get(email=request.user.email)
    times = calculate_ampm()
    recurring = RecurringAvailability.objects.filter(profile=profile)
    recurring_values = calculate_recurring_values(recurring)

    return render(request, 'tablefor2/availability/edit.html', {
        'profile': profile,
        'recurring': recurring,
        'recurring_values': recurring_values,
        'times': times,
    })


# saves the recurring availability
@login_required
def save_availability(request):
    profile = Profile.objects.get(email=request.user.email)
    if request.method == 'POST':
        recurring_availabilities = request.POST.getlist('recurring_availabilities[]')
        for recurring_availability in recurring_availabilities:
            string = recurring_availability.split('-')
            day = string[0]
            time_string = string[1]

            # if deleted, remove
            try:
                rec = RecurringAvailability.objects.get(profile=profile, day=day, time=time_string)
                if string[2]:
                    rec.delete()

            except IndexError:
                pass

            # save the rest since they're new
            except:
                rec_av = RecurringAvailability(profile=profile, day=day, time=time_string)
                rec_av.save()

        time.sleep(1)  # wait until everything's done saving, hacky
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('tablefor2/availability/edit.html')


# deletes an existing availability, delete later
@login_required
def delete_availability(request, availability_id):
    availability = Availability.objects.get(pk=availability_id)
    availability.delete()
    return HttpResponseRedirect('/')


# view profile, remove later
@login_required
def profile(request):
    today = date.today()
    profile = Profile.objects.get(email=request.user.email)
    past_matches = Availability.objects.filter(profile=profile, time_available__lte=today).exclude(matched_name=None) or None

    # force users to add more info
    if not profile.extra_saved_information:
        return HttpResponseRedirect('/profile/edit')
    else:
        return render(request, 'tablefor2/profile/view.html', {
            'profile': profile,
            'past_matches': past_matches
        })


# prepares the editing screen for a profile
@login_required
def edit_profile(request):
    profile = Profile.objects.get(email=request.user.email)

    if not profile.extra_saved_information:
        form = ProfileForm(request.POST or None, request.FILES or None)
    else:
        data = {
            'preferred_name': profile.preferred_name,
            'department': profile.department,
            'location': profile.location,
            'timezone': profile.timezone,
            'google_hangout': profile.google_hangout,
            'frequency': profile.frequency,
            'date_entered_mixpanel': profile.date_entered_mixpanel
        }
        form = ProfileForm(initial=data)

    return render(request, 'tablefor2/profile/edit.html', {'form': form, 'profile': profile})


# saves profile info after edits
@login_required
def save_profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':

        if form.is_valid():
            profile = Profile.objects.get(email=request.user.email)
            # save the form info to this profile
            profile.preferred_name = form.cleaned_data.get('preferred_name')
            profile.department = form.cleaned_data.get('department')
            profile.google_hangout = form.cleaned_data.get('google_hangout')
            profile.location = form.cleaned_data.get('location')
            profile.timezone = form.cleaned_data.get('timezone')
            profile.frequency = form.cleaned_data.get('frequency')
            profile.date_entered_mixpanel = form.cleaned_data.get('date_entered_mixpanel')
            profile.extra_saved_information = True
            profile.save()

            # add a message here?
            return HttpResponseRedirect("/")

    return render(request, 'tablefor2/profile/edit.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
