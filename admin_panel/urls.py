from django.urls import path
from . import views

urlpatterns = [

    # ==============================
    # 📊 DASHBOARD
    # ==============================
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # ==============================
    # 📋 PROVIDER REQUESTS (APPROVAL)
    # ==============================
    path('provider-requests/', views.provider_requests, name='provider_requests'),
    path('provider-requests/approve/<int:id>/', views.approve_provider, name='approve_provider'),
    path('provider-requests/reject/<int:id>/', views.reject_provider, name='reject_provider'),

    # ==============================
    # 👤 USER MANAGEMENT
    # ==============================
    path('users/', views.manage_users, name='manage_users'),
    path('users/toggle/<int:id>/', views.toggle_user, name='toggle_user'),
    path('users/delete/<int:id>/', views.delete_user, name='delete_user'),

    # ==============================
    # 👨‍🔧 PROVIDER MANAGEMENT
    # ==============================
path(
    'providers/',
    views.manage_providers,
    name='manage_providers'
),

path(
    'providers/toggle/<int:id>/',
    views.toggle_provider,
    name='toggle_provider'
),

path(
    'providers/delete/<int:id>/',
    views.delete_provider,
    name='delete_provider'
),

path(
    'providers/reviews/<int:id>/',
    views.provider_reviews,
    name='provider_reviews'
),

    # ==============================
    # 🛠 SERVICE MANAGEMENT
    # ==============================
    path('services/', views.manage_services, name='manage_services'),
    path('services/delete/<int:id>/', views.delete_service, name='delete_service'),

    path('services/add/', views.add_service, name='add_service'),
]