from rest_framework import serializers
from interactions.models.interactions import Interaction

class IntractionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Interaction
        fields='__all__'