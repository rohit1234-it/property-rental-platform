from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from accounts.serializers.auth import LoginRequestSerializer
from accounts.services.auth import UserAuth


class UserLogin(viewsets.ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = LoginRequestSerializer

    def user_login(self, request):
        return UserAuth(request).login()