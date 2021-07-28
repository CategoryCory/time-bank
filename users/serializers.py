from django.contrib.auth import get_user_model
from rest_framework import serializers

CustomUser = get_user_model()


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'profile_pic', ]
