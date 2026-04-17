"""
API v1 router - aggregates all app-level URL patterns
"""

from django.urls import path, include

urlpatterns = [
    path("auth/", include("accounts.url.auth")),
    path("users/", include("accounts.urls.users")),
    path("locations/", include("locations.urls")),
    path("vendors/", include("vendors.urls")),
    path("payments/", include("payments.url")),
]