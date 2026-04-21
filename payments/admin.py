from django.contrib import admin
from .models import PaymentSession


@admin.register(PaymentSession)
class PaymentSessionAdmin(admin.ModelAdmin):
    list_display = ("plate_number", "phone_number", "lot", "vendor", "status", "created_at")
    search_fields = ("plate_number", "phone_number")
    list_filter = ("status",)
    list_select_related = ("lot", "vendor", "user")
    readonly_fields = ("ussd_string", "tel_uri", "plate_number", "phone_number")