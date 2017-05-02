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
    form = ProfileForm(initial={'department': '', 'location': ''})
    return render(request, 'tablefor2/profile-information.html', {'form': form})
    # return render(request, 'tablefor2/profile-information.html')


@login_required
def register(request, username):
    user = authenticate(username=username, password=None)
    # if user is None and request.method == 'POST':
    #     form = ProfileForm(request.POST)
    #     print form.location.selected

        # if form.is_valid():

# user.first_name
# user.last_name
# user.email
# user.username
# user.is_active
# user.is_superuser
# user.is_staff
# user.date_joined

    return HttpResponseRedirect('/')


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
