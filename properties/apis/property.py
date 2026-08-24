from properties.models.property import Property
from rest_framework import viewsets
from properties.serializers.property import PropertySerializer

# Create your views here.
class PropertyViewset(viewsets.ModelViewSet):
    queryset=Property.objects.all()
    serializer_class=PropertySerializer