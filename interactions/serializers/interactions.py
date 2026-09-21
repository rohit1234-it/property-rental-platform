from rest_framework import serializers
from interactions.models.interactions import Interaction

class IntractionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Interaction
        fields='__all__'

        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]