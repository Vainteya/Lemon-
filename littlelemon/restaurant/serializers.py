from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Booking, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # Djoser also registers views named "user-detail", so this API's user
    # routes use the "api-user" basename to keep reverse() unambiguous.
    url = serializers.HyperlinkedIdentityField(view_name='api-user-detail')

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
