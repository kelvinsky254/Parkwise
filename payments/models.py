from django.db import models
from django.conf import settings
from core.models import TimeStampedModel




class ParkingSession(TimeStampedModel):
    """
    Records each time a user initiates a USSD dial for a parking lot.
    Plate number and phone number are denormalized at session created time
    so the audit trail is preserved even if the user later changes their details.
    """

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
        related_name="parking_sessions",
    )
    lot = models.ForeignKey(
        "locations.ParkingLot",
        on_delete=models.PROTECT,
        related_name="parking_sessions",
    )
    vendor = models.ForeignKey(
        "vendors.Vendor",
        on_delete=models.PROTECT,
        related_name="parking_sessions",
    )
    plate_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    ussd_string = models.CharField(max_length=100)
    tel_uri = models.CharField(max_length=150)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_INITIATED,
    )

    class Meta:
        db_table = "payments_parking_session"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} | {self.lot.name} | {self.status}"

class UserSavedLot(TimeStampedModel):
    """
    A user's personal list of saved/bookmarked parking lots.
    Also tracks visit count for surfacing frequently used lots.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_lots",
    )
    lot = models.ForeignKey(
        "locations.ParkingLot",
        on_delete=models.CASCADE,
        related_name="saved_by",
    )
    is_favorite = models.BooleanField(default=False)
    visit_count = models.PositiveIntegerField(default=0)
    last_visited_at = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "payments_user_saved_lot"
        unique_together = ("user", "lot")
        ordering = ["-visit_count", "-last_visited_at"]


    def __str__(self):
        return f"{self.user.email} -> {self.lot.name}"









