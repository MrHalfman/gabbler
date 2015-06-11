from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
import rest_api.views as api_views


router = DefaultRouter()
router.register(r'gabs', api_views.GabsViewSet)
router.register(r'regabs', api_views.ReGabsViewSet)
router.register(r'notifications', api_views.NotificationsViewSet)
router.register(r'users', api_views.UserViewSet)
router.register(r'places', api_views.PlaceViewset)
router.register(r'mailnotifications', api_views.MailNotificationsViewSet)
router.register(r'userlinks', api_views.UserLinkViewSet)
router.register(r'useerlinkstypes', api_views.UserLinkTypesViewSet)

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
    url(r'gabs_list/(?P<page>\d+)', 'social.views.getGabs', name="getGabs"),
    url(r'follow/(?P<user_pk>\d+)', 'social.views.follow', name="follow"),
    url(r'^post_gab/', 'social.views.post_gab', name="post_gab"),
    url(r'^regab/(?P<gab_pk>\d+)/', 'social.views.regab', name="regab"),
    url(r'^like/(?P<gab_pk>\d+)/', 'social.views.like', name="like"),
    url(r'^dislike/(?P<gab_pk>\d+)/', 'social.views.dislike', name="dislike"),
    url(r'^delete_gab/(?P<gab_pk>\d+)/', 'social.views.delete_gab', name="delete_gab"),
    url(r'^report_gab/(?P<gab_pk>\d+)/', 'social.views.report_gab', name="report_gab"),
    url(r'^search/(?P<query>\w+)/', 'social.views.search', name="search"),
    url(r'^notifications_read/', 'social.views.mark_notifications_asread', name="notifications_read"),

    url(r'^admin/$', 'social.views.moderation_reports', name="admin"),
    url(r'^admin/reports/$', 'social.views.moderation_reports', name="moderation_reports"),
    url(r'^admin/reports/markAsProcessed/(?P<report_pk>\d+)/', 'social.views.moderation_reports_processed', name="mark_as_processed"),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

)
