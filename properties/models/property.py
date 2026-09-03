from django.db import models
from accounts.models import User


class Property(models.Model):

    PROPERTY_TYPES = (
        ('flat', 'Flat'),
        ('house', 'House'),
        ('room', 'Room'),
        ('shop', 'Shop'),
        ('office', 'Office'),
    )

    property_name = models.CharField(max_length=100)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES
    )

    address = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    rent = models.PositiveIntegerField()

    deposit = models.PositiveIntegerField(default=0)

    bedrooms = models.PositiveIntegerField(default=1)

    bathrooms = models.PositiveIntegerField(default=1)

    description = models.TextField(blank=True)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.property_name