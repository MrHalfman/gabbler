import django_filters
from rest_framework import viewsets
from core.models import User, Place, MailNotifications
from social.models import Gab, Regab, Notifications
from rest_framework import filters
import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class PlaceViewset(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = serializers.PlaceSerializer


class MailNotificationsViewSet(viewsets.ModelViewSet):
    queryset = MailNotifications.objects.all()
    serializer_class = serializers.MailNotificationsSerializer


class GabsViewSet(viewsets.ModelViewSet):
    queryset = Gab.objects.all()
    serializer_class = serializers.GabSerializer


class ReGabsViewSet(viewsets.ModelViewSet):
    queryset = Regab.objects.all()
    serializer_class = serializers.ReGabSerializer


class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = serializers.NotificationsSerializer