from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^connect/', 'core.views.connect', name="connect"),
    url(r'^logout/', 'core.views.logout', name="logout"),
    url(r'^register/', 'core.views.register', name="register"),
    url(r'^admin/', include(admin.site.urls)),
)
