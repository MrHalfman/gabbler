from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),

    # User
    url(r'^user/(?P<username>\w+)/', 'core.views.user_profile', name="user_profile"),
    url(r'^register/', 'core.views.register', name="register"),
    url(r'^connect/', 'core.views.connect', name="connect"),
    url(r'^logout/', 'core.views.logout', name="logout"),
    url(r'^update/', 'core.views.update', name="update"),
    url(r'^delete_user/', 'core.views.delete_user', name="delete_user"),
    url(r'^lost_password-step-1/', 'core.views.lost_password_step_1', name="lost_password_step_1"),
    url(r'^lost_password-step-2/', 'core.views.lost_password_step_2', name="lost_password_step_2"),

    # Social
    url(r'^post_gab/', 'social.views.post_gab', name="post_gab"),
    url(r'^delete_gab/(?P<gab_pk>\w+)/', 'social.views.delete_gab', name="delete_gab"),
    url(r'^report_gab/(?P<gab_pk>\w+)/', 'social.views.report_gab', name="report_gab"),

    url(r'^admin/$', 'social.views.moderation_reports', name="admin"),
    url(r'^admin/reports/$', 'social.views.moderation_reports', name="moderation_reports"),
    url(r'^admin/reports/markAsProcessed/(?P<report_pk>\w+)/', 'social.views.moderation_reports_processed', name="mark_as_processed"),
)
