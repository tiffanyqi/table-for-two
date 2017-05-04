from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from tablefor2 import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^edit-profile/$', views.edit_profile, name='edit-profile'),
    url(r'^save-profile/$', views.save_profile, name='save-profile'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url('', include('social_django.urls', namespace='social')),
]
