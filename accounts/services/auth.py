from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

class UserAuth:

    def __init__(self, request):
        self.request = request

    def login(self):
        username = self.request.data.get("username")
        password = self.request.data.get("password")

        if not username or not password:
            return Response(
            {
                "success": False,
                "message": "Username and password are required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        user = authenticate(
        username=username,
        password=password
    )
        if user is None:
            return Response(
            {
                "success": False,
                "message": "Invalid username or password."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
        refresh = RefreshToken.for_user(user)
        return Response(
        {
            "success": True,
            "message": "Login successful.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        },
        status=status.HTTP_200_OK
    )