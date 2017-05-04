from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from tablefor2.forms import ProfileForm
from tablefor2.models import *


def index(request):
    try:
        # does the profile exist?
        profile = Profile.objects.get(email=request.user.email)

        # force users to add more info
        if not profile.extra_saved_information:
            return HttpResponseRedirect('/edit-profile')
        else:
            return render(request, 'tablefor2/index-logged-in.html', {'profile': profile})

    except:
        return render(request, 'tablefor2/index-logged-out.html')


@login_required
def profile(request):
    profile = Profile.objects.get(email=request.user.email)

    # force users to add more info
    if not profile.extra_saved_information:
        return HttpResponseRedirect('/edit-profile')
    else:
        return render(request, 'tablefor2/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None)
    profile = Profile.objects.get(email=request.user.email)
    return render(request, 'tablefor2/edit-profile.html', {'form': form, 'profile': profile})


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
            profile.date_entered_mixpanel = form.cleaned_data.get('date_entered_mixpanel')
            profile.extra_saved_information = True
            profile.save()

            # add a message here?
            return HttpResponseRedirect('/')

    return render(request, 'tablefor2/edit-profile.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
