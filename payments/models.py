from django.db import models
from django.conf import settings

class PaymentSession(models.Model):
    STATUS_INITIATED = "initiated"
    STATUS_DIALED = "dialed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_INITIATED, "Initiated"),
        (STATUS_DIALED, "Dialed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payment_sessions",
    )
    lot = models.ForeignKey(
        "locations.ParkingLot",
        on_delete=models.PROTECT,
        related_name="payment_sessions",
    )
    # Denormalised at session creation time - preserved even if user uses it later
    # changes their plate or phone number
    plate_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    ussd_string = models.CharField(max_length=100)
    tel_uri = models.CharField(max_length=150)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_INITIATED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments_session"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email}" | {self.lot.name} | {self.status}

