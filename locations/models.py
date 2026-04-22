from django.db import models
from core.models import TimeStampedModel


class ParkingLot(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_active = models.BooleanField(default=True)


    class Meta:
        db_table = "locations_parking_lot"


    def __str__(self):
        return self.name


class LotVendorMapping(TimeStampedModel):
    lot = models.ForeignKey(
        ParkingLot,
        on_delete=models.CASCADE,
        related_name="vendor_mapping",
    )
    vendor = models.ForeignKey(
        "vendors.vendor",
        on_delete=models.CASCADE,
        related_name="lot_mapping",
    )
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_name = "locations_lot_vendor_mapping"
        ordering = ["-effective_from"]

    def __str__(self):
        return f"{self.lot.name} -> {self.vendor.name} (from {self.effective_from})"


