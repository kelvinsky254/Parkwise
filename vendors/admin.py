from django.contrib import admin
from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "ussd_shortcode", "sandbox_mode", "is_active")
    search_fields = ("name", "short_name", "ussd_shortcode")
    list_filter = ("sandbox_mode", "is_active")
    readonly_fields = ("id", "created_at", "updated_at")
