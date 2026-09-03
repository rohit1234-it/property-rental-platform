from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from accounts.serializers.auth import LoginRequestSerializer
from accounts.services.auth import UserAuth
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class UserLogin(viewsets.ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = LoginRequestSerializer

    def user_login(self, request):
        return UserAuth(request).login()


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "role": request.user.role,
        })