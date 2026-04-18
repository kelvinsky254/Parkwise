from django.db import models


class ParkingLot(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "locations_parking_lot"

    def __str__(self):
        return self.name


class LotVendorMapping(models.Model):
    lot = models.ForeignKey(
        ParkingLot,
        on_delete=models.CASCADE,
        related_name="vendor_mappings",
    )
    vendor = models.ForeignKey(
        "vendors.Vendor",
        on_delete=models.CASCADE,
        related_name="lot_mappings",
    )
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "locations_lot_vendor_mapping"
        ordering = ["-effective_from"]

    def __str__(self):
        return f"{self.lot.name} → {self.vendor.name} (from {self.effective_from})"