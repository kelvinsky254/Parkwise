import uuid
from django.db import models
from core.models import TimeStampedModel



class Vendor(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, unique=True)
    ussd_shortcode = models.CharField(max_length=20)
    ussd_chain_template = models.CharField(
        max_length=100,
        help_text="USSD string template e.g. *483*1*{plate}*{phone}#",
    )
    adapter_class = models.CharField(
        max_length=255,
        help_text="Dotted Python path to the adapter class e.g. vendors.adapters.kaps.KAPSAdapter",
    )
    config = models.JSONField(default=dict, blank=True)
    sandbox_mode = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "vendors_vendor"

    def __str__(self):
        return self.name