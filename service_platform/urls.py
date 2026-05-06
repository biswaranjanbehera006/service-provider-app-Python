"""
URL configuration for service_platform project.
"""

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # =========================
    # DJANGO ADMIN
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # MAIN APP
    # =========================
    path('', include('services.urls')),

    # =========================
    # BOOKINGS
    # =========================
    path('booking/', include('bookings.urls')),

    # =========================
    # USERS
    # =========================
    path('users/', include('users.urls')),

    # =========================
    # PROVIDERS
    # =========================
    path('provider/', include('providers.urls')),

    # =========================
    # ADMIN PANEL
    # =========================
    path('admin-panel/', include('admin_panel.urls')),
]


# =========================
# MEDIA FILES
# =========================
if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )