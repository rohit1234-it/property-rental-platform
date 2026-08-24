from properties.apis.property import PropertyViewset
from rest_framework.routers import DefaultRouter

r=DefaultRouter()
r.register('property',PropertyViewset,basename='property')

urlpatterns =r.urls
