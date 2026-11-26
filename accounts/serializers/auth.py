
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class LoginRequestSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


