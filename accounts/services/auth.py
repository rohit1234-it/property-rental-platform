from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserAuth:

    def __init__(self, request):
        self.request = request

    def login(self):
        username = self.request.data.get("username")
        password = self.request.data.get("password")

        if not username or not password:
            return {
                "success": False,
                "message": "Username and password are required."
            }

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return {
                "success": False,
                "message": "Invalid username or password."
            }

        refresh = RefreshToken.for_user(user)

        return {
            "success": True,
            "message": "Login successful.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        }