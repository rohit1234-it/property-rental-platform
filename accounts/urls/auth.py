from django.urls import path
from accounts.apis.auth import UserLogin,UserProfile


urlpatterns = [
    path(
        'user_login/',
        UserLogin.as_view({'post': 'user_login'}),
        name='user_login'
    ),
    path(
        'me/',
        UserProfile.as_view(),
        name='user_details'
    ),
]