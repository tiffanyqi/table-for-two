from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from tablefor2.forms import ProfileForm
from tablefor2.models import *


def index(request):
    try:
        profile = Profile.objects.get(email=request.user.email)
        return render(request, 'tablefor2/index-logged-in.html', {'profile': profile})
    except:
        return render(request, 'tablefor2/index-logged-out.html')


@login_required
def profile_information(request):
    profile = Profile.objects.get(email=request.user.email)
    if not profile.extra_saved_information:
        form = ProfileForm(request.POST or None, request.FILES or None)
        return render(request, 'tablefor2/profile-information.html', {'form': form})

    else:
        return HttpResponseRedirect('/')


@login_required
def register(request):
    form = ProfileForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':

        if form.is_valid():
            profile = Profile.objects.get(email=request.user.email)
            profile.preferred_name = form.cleaned_data.get('preferred_name')
            profile.department = form.cleaned_data.get('department')
            profile.google_hangout = form.cleaned_data.get('google_hangout')
            profile.location = form.cleaned_data.get('location')
            profile.date_entered_mixpanel = form.cleaned_data.get('date_entered_mixpanel')
            profile.extra_saved_information = True
            profile.save()
            # add a message here?
            return HttpResponseRedirect('/')

    return render(request, 'tablefor2/profile-information.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
