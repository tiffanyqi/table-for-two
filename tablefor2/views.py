from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from tablefor2.forms import *
from tablefor2.helpers import calculate_utc
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
            today = date.today()
            form = AvailabilityForm(request.POST or None, request.FILES or None)
            availabilities = Availability.objects.filter(time_available__gte=today).order_by('time_available') or None
            past_matches = Availability.objects.filter(profile=profile, time_available__lte=today).exclude(matched_name=None) or None
            current_matches = Availability.objects.filter(profile=profile, time_available__gte=today).exclude(matched_name=None) or None
            return render(request, 'tablefor2/index-logged-in.html', {
                'profile': profile,
                'form': form,
                'availabilities': availabilities,
                'past_matches': past_matches,
                'current_matches': current_matches
            })

    except:
        return render(request, 'tablefor2/index-logged-out.html')


@login_required
def save_availability(request):
    profile = Profile.objects.get(email=request.user.email)
    form = AvailabilityForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':

        if form.is_valid():
            availability = Availability(profile=profile)
            availability.time_available = form.cleaned_data.get('time_available')
            availability.time_available_utc = calculate_utc(profile, availability.time_available)
            availability.save()
            return HttpResponseRedirect("/")

    return render(request, 'tablefor2/index-logged-in.html', {'form': form})


@login_required
def edit_availability(request, availability_id):
    profile = Profile.objects.get(email=request.user.email)
    form = AvailabilityForm(request.POST or None, request.FILES or None)
    availability = Availability.objects.get(pk=availability_id)
    if request.method == 'POST':

        if form.is_valid():
            availability.time_available = form.cleaned_data.get('time_available')
            availability.time_available_utc = calculate_utc(profile, availability.time_available)
            availability.save()
            return HttpResponseRedirect('/')

    return render(request, 'tablefor2/index-logged-in.html', {'form': form})


@login_required
def delete_availability(request, availability_id):
    availability = Availability.objects.get(pk=availability_id)
    availability.delete()
    return HttpResponseRedirect('/')


@login_required
def profile(request):
    profile = Profile.objects.get(email=request.user.email)

    # force users to add more info
    if not profile.extra_saved_information:
        return HttpResponseRedirect('/profile/edit')
    else:
        return render(request, 'tablefor2/profile/view.html', {'profile': profile})


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
            return HttpResponseRedirect('/')

    return render(request, 'tablefor2/profile/edit.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
