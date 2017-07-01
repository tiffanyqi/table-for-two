from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from tablefor2.forms import *
from tablefor2.helpers import calculate_utc, calculate_ampm, determine_ampm
from tablefor2.models import *


def index(request):
    try:
        # does the profile exist?
        profile = Profile.objects.get(email=request.user.email)

        # force users to add more info
        if not profile.extra_saved_information:
            return HttpResponseRedirect('/profile/edit')

        # show profile and availability and matches!
        else:
            recurring = RecurringAvailability.objects.filter(profile=profile)
            today = date.today()
            current_matches = Availability.objects.filter(profile=profile, time_available__gte=today).exclude(matched_name=None) or None
            availabilities = Availability.objects.filter(profile=profile, time_available__gte=today).order_by('time_available') or None
            new_availability_form = AvailabilityForm(request.POST or None, request.FILES or None)

            return render(request, 'tablefor2/index-logged-in.html', {
                'profile': profile,
                'form': new_availability_form,
                'availabilities': availabilities,
                'current_matches': current_matches,
                'recurring': recurring
            })

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/availability/edit')

    except:
        return render(request, 'tablefor2/index-logged-out.html')


# prepares the edit screen for recurring availability
@login_required
def edit_availability(request):
    profile = Profile.objects.get(email=request.user.email)
    times = calculate_ampm()

    try:
        recurring = RecurringAvailability.objects.get(profile=profile) or None

    except:
        return render(request, 'tablefor2/availability/edit.html', {
            'profile': profile,
            'recurring': None,
            'times': times,
        })

    return render(request, 'tablefor2/availability/edit.html', {
        'profile': profile,
        'recurring': recurring,
        'times': times,
    })


# saves the recurring availability
@login_required
def save_availability(request):
    profile = Profile.objects.get(email=request.user.email)
    recurring_availabilities = request.POST.getlist('recurring_availabilities[]')
    for recurring_availability in recurring_availabilities:
        string = recurring_availability.split('-')
        day = string[0]
        time = determine_ampm(string[1])
        rec_av = RecurringAvailability(profile=profile, day=day, time=time)
        print rec_av
        rec_av.save()

    # return render(request, 'tablefor2/index-logged-in.html', {
    #     'profile': profile,
    # })

    return HttpResponseRedirect('/')


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
