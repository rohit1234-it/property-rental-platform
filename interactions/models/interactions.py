from django.db import models
from django.conf import settings


class Interaction(models.Model):

    INTERACTION_TYPES = [
        ('inquiry', 'Inquiry'),
        ('interest', 'Interest'),
        ('visit', 'Visit Request'),
        ('contact', 'Contact'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    # User who performed the interaction
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interactions'
    )

    # Property on which interaction happened
    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.CASCADE,
        related_name='interactions'
    )

    interaction_type = models.CharField(
        max_length=20,
        choices=INTERACTION_TYPES
    )

    message = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.property} - {self.interaction_type}"