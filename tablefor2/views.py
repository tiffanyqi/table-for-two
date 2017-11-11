from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from mixpanel import Mixpanel

from tablefor2.forms import *
from tablefor2.helpers import calculate_ampm, calculate_recurring_values
from tablefor2.models import *
from tablefor2.settings import MP_TOKEN

import time

mp = Mixpanel(MP_TOKEN)


def index(request):
    try:
        # does the profile exist?
        print(request.user)
        profile = Profile.objects.get(email=request.user.email)
        recurring = RecurringAvailability.objects.filter(profile=profile)
        times = calculate_ampm()

        # force users to add more info
        if not profile.extra_saved_information:
            profile.date_joined = date.today()
            profile.number_of_matches = 0
            profile.save()
            return HttpResponseRedirect('/profile/edit')
        elif not recurring:
            return HttpResponseRedirect('/availability/edit')

        # show profile and availability and matches!
        else:
            today = date.today()
            current_matches = Availability.objects.filter(profile=profile, time_available__gt=today).exclude(matched_name=None) or None
            past_matches = Availability.objects.filter(profile=profile, time_available__lte=today).exclude(matched_name=None).order_by('-time_available_utc') or None
            availabilities = Availability.objects.filter(profile=profile, time_available__gte=today).order_by('time_available') or None
            recurring_values = calculate_recurring_values(recurring)

            return render(request, 'tablefor2/index-logged-in.html', {
                'profile': profile,
                'availabilities': availabilities,
                'current_matches': current_matches,
                'past_matches': past_matches,
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
            except RecurringAvailability.DoesNotExist:
                rec_av = RecurringAvailability(profile=profile, day=day, time=time_string)
                rec_av.save()

        if recurring_availabilities:
            mp.track(profile.distinct_id, 'Recurring Availability Saved')
            mp.people_set(profile.distinct_id, {
                'Number of Recurring Availabilities': len(RecurringAvailability.objects.filter(profile=profile))
            })

        time.sleep(1)  # wait until everything's done saving, hacky
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('tablefor2/availability/edit.html')


# prepares the editing screen for a profile
@login_required
def edit_profile(request):
    profile = Profile.objects.get(email=request.user.email)

    if not profile.extra_saved_information:
        form = ProfileForm(request.POST or None, request.FILES or None)
    else:
        data = {
            'preferred_first_name': profile.preferred_first_name,
            'department': profile.department,
            'accept_matches': profile.accept_matches,
            'location': profile.location,
            'timezone': profile.timezone,
            'google_hangout': profile.google_hangout,
            'frequency': profile.frequency,
            'date_entered_mixpanel': profile.date_entered_mixpanel,
            'what_is_your_favorite_animal': profile.what_is_your_favorite_animal,
            'name_a_fun_fact_about_yourself': profile.name_a_fun_fact_about_yourself
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

            if not profile.extra_saved_information:
                distinct_id = form.cleaned_data.get('distinct_id')
                mp.track(distinct_id, 'Profile Created')
                mp.people_set(distinct_id, {
                    'Number of Matches': 0
                })
                profile.distinct_id = distinct_id
                profile.save()
            else:
                mp.track(profile.distinct_id, 'Profile Saved')

            # save the form info to this profile
            profile.preferred_first_name = form.cleaned_data.get('preferred_first_name')
            profile.department = form.cleaned_data.get('department')
            profile.accept_matches = form.cleaned_data.get('accept_matches')
            profile.google_hangout = form.cleaned_data.get('google_hangout')
            profile.location = form.cleaned_data.get('location')
            profile.timezone = form.cleaned_data.get('timezone')
            profile.frequency = form.cleaned_data.get('frequency')
            profile.date_entered_mixpanel = form.cleaned_data.get('date_entered_mixpanel')
            profile.what_is_your_favorite_animal = form.cleaned_data.get('what_is_your_favorite_animal')
            profile.name_a_fun_fact_about_yourself = form.cleaned_data.get('name_a_fun_fact_about_yourself')
            profile.extra_saved_information = True
            profile.save()

            mp.people_set(profile.distinct_id, {
                '$first_name': profile.first_name,
                '$last_name': profile.last_name,
                'Preferred Name': profile.preferred_first_name,
                '$email': profile.email,
                'Department': profile.department,
                'Accepting Matches': profile.accept_matches,
                'Location': profile.location,
                'Timezone': profile.timezone,
                'Frequency': profile.frequency,
                'Date Entered Mixpanel': str(profile.date_entered_mixpanel),
                'Number of Matches': profile.number_of_matches,
                'Date Joined': str(profile.date_joined)
            })

            # add a message here?
            return HttpResponseRedirect("/")

    return render(request, 'tablefor2/profile/edit.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
