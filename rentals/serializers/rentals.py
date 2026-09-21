from rest_framework import serializers
from rentals.models.rental import Rental


class RentalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rental
        fields = "__all__"

        read_only_fields = [
            "owner",
            "created_at",
            "updated_at",
        ]