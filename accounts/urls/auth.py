from django.urls import path
from accounts.apis.auth import UserLogin


urlpatterns = [
    path(
        'user_login/',
        UserLogin.as_view({'post': 'user_login'}),
        name='user_login'
    ),
]