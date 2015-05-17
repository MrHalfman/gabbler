from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^connect/', 'core.views.connect', name="connect"),
    url(r'^logout/', 'core.views.logout', name="logout"),
    url(r'^update/', 'core.views.update', name="update"),
    url(r'^register/', 'core.views.register', name="register"),
    url(r'^deleteUser/', 'core.views.delete_user', name="deleteUser"),

    url(r'^postGab/', 'social.views.post_gab', name="post_gab"),
    url(r'delete-gab/(?P<gab_pk>\w+)/', 'social.views.delete_gab', name="delete_gab"),

    url(r'^user/(?P<username>\w+)/', 'core.views.user_profile', name="user_profile"),
    url(r'^admin/', include(admin.site.urls))
)
