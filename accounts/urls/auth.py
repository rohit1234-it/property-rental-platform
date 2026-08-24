from accounts.apis.auth import UserLogin
from rest_framework.routers import DefaultRouter

r=DefaultRouter()
r.register('user_login/',UserLogin,basename='user_login')

urlpatterns = r.urls
