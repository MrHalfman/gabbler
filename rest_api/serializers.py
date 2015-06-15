from rest_framework import serializers
from core.models import User, Place, MailNotifications, UserLink, UserLinkTypes
from social.models import Gab, Regab, Notifications


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'banner', 'bio', 'birthdate', 'place', 'mail_notifications')


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'country', 'city')


class MailNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailNotifications
        fields = ('id', 'regab', 'like', 'private_message', 'citation')


class GabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gab
        fields = ('id', 'user', 'date', 'text', 'extras', 'gifId')


class ReGabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regab
        fields = ('id', 'user', 'gab', 'date')


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ('id', 'user', 'text', 'link', 'date', 'read')
