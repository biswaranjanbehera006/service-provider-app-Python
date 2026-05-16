from django.urls import path

from .views import (
    cancel_booking,
    logout_view,
    register_view,
    login_view,
    user_dashboard,
    verify_email,
    forgot_password,
    verify_reset_otp,
    reset_password,
    profile_view
)

urlpatterns = [

    path('register/', register_view, name='register'),

    path('login/', login_view, name='login'),

    path('dashboard/', user_dashboard, name='user_dashboard'),

    path('logout/', logout_view, name='logout'),

    path('cancel/<int:id>/', cancel_booking, name='cancel_booking'),

    path(
        'verify-email/<int:user_id>/',
        verify_email,
        name='verify_email'
    ),

    path('profile/', profile_view, name='profile'),

    # =========================
    # FORGOT PASSWORD
    # =========================
    path(
        'forgot-password/',
        forgot_password,
        name='forgot_password'
    ),

    path(
        'verify-reset-otp/',
        verify_reset_otp,
        name='verify_reset_otp'
    ),

    path(
        'reset-password/',
        reset_password,
        name='reset_password'
    ),

]