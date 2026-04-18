from django.db import models


class Vendor(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vendors_vendor"

    def __str__(self):
        return self.name