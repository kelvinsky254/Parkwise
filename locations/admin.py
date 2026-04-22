from django.contrib import admin
from .models import ParkingLot, LotVendorMapping

@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "latitude", "longitude", "is_active")
    search_fields = ("name", "address")
    list_filter = ("is_active")
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(LotVendorMapping)
class LotVendorMappingAdmin(admin.ModelAdmin):
    list_display = ("lot", "effective_from", "effective_to", "is_active")
    list_select_related = ("lot", "vendor")
    list_filter = ("is_active")
    readonly_fields = ("created_at", "updated_at")

