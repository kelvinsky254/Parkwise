from django.contrib import admin
from .models import ParkingSession, UserSavedLot


@admin.register(ParkingSession)
class ParkingSessionAdmin(admin.ModelAdmin):
    list_display = ("plate_number", "phone_number", "lot", "vendor", "status", "created_at")
    search_fields = ("plate_number", "phone_number", "user__email")
    list_filter = ("status",)
    list_selected_related = ("lot", "vendor", "user")
    readonly_fields = ("ussd_string", "tel_uri", "plate_number", "phone_number", "created_at", "updated_at")




@admin.register(UserSavedLot)
class UserSavedLotAdmin(admin.ModelAdmin):
    list_display = ("user", "lot", "is_favorite", "visit_count", "last_visited_at")
    search_fields = ("user__email", "lot__name")
    list_filter = ("is_favorite",)
    list_select_related = ("user", "lot")
    readonly_fields = ("visit_count", "last_visited_at", "created_at", "updated_at")

