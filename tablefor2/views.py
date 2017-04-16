from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

# from .models import *


def home(request):
    # if request.user.is_authenticated():
        # return render(request, 'tablefor2/home_logged_in.html')
    # else:
        return render(request, 'tablefor2/home_logged_out.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
