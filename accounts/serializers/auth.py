import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from property_rental_system.accounts.models.user import UserProfile

User = get_user_model()

class LoginRequestSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


