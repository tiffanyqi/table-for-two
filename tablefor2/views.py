from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from oauth2client.client import OAuth2WebServerFlow, AccessTokenCredentials
# from oauth2client.django_orm import Storage

from social.apps.django_app.utils import psa

from tablefor2.forms import ProfileForm


def index(request):
    if request.user.is_authenticated():
        return render(request, 'tablefor2/index-logged-in.html')
    else:
        return render(request, 'tablefor2/index-logged-out.html')


@login_required
def profile_information(request):
    form = ProfileForm(request.POST or None, request.FILES or None)
    return render(request, 'tablefor2/profile-information.html', {'form': form})


@login_required
def register(request, username):
    form = ProfileForm(request.POST or None, request.FILES or None)
    authenticated_user = authenticate(username=username, password=None)
    requested_user = request.user
    if authenticated_user is None and request.method == 'POST':

        print form.is_valid()

        # if form.is_valid():
            # requested_user.first_name
            # requested_user.last_name
            # requested_user.email
            # requested_user.username
            # requested_user.is_active
            # requested_user.is_superuser
            # requested_user.is_staff
            # requested_user.date_joined
            # return HttpResponseRedirect('/')

    return render(request, 'tablefor2/profile-information.html', {'form': form})


@csrf_exempt
@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token POST parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.POST.get('access_token')
    print "Token: {}".format(token)
    user = request.backend.do_auth(token)
    if user:
        login(request, user)

        # The user agent is only used for logs
        # credential = AccessTokenCredentials(token, 'dummy-user-agent/1.0')
        # storage = Storage(GoogleCredentials, 'user', request.user, 'credential')
        # storage.put(credential)

    return HttpResponseRedirect("/")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
