from rest_framework import serializers
from properties.models.property import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model=Property
        fields='__all__'