from rest_framework import viewsets
from core.models import User, Place, MailNotifications, UserLink, UserLinkTypes
from social.models import Gab, Regab, Notifications
import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class PlaceViewset(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = serializers.PlaceSerializer


class MailNotificationsViewSet(viewsets.ModelViewSet):
    queryset = MailNotifications.objects.all()
    serializer_class = serializers.MailNotificationsSerializer


class UserLinkViewSet(viewsets.ModelViewSet):
    queryset = UserLink.objects.all()
    serializer_class = serializers.UserLinkSerializer


class UserLinkTypesViewSet(viewsets.ModelViewSet):
    queryset = UserLinkTypes.objects.all()
    serializer_class = serializers.UserLinkTypesSerializer


class GabsViewSet(viewsets.ModelViewSet):
    queryset = Gab.objects.all()
    serializer_class = serializers.GabSerializer


class ReGabsViewSet(viewsets.ModelViewSet):
    queryset = Regab.objects.all()
    serializer_class = serializers.ReGabSerializer


class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = serializers.NotificationsSerializer