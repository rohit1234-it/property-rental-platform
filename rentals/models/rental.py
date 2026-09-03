from django.db import models


class Rental(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACTIVE", "Active"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    id = models.BigAutoField(primary_key=True)

    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.CASCADE,
        related_name="rentals"
    )

    tenant = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name="tenant_rentals"
    )

    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name="owner_rentals"
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    monthly_rent = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    security_deposit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property} - {self.tenant}"