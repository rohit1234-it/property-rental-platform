from properties.apis.property import PropertyViewSet
from rest_framework.routers import DefaultRouter

r=DefaultRouter()
r.register('property',PropertyViewSet,basename='property')

urlpatterns =r.urls
