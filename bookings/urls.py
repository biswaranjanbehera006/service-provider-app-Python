from django.urls import path

from .views import (

    # BOOKING
    create_booking,

    # PAYMENT
    payment_page,
    payment_success,
    payment_failed,

    # STATUS
    update_booking_status,

    # RATING
    rate_booking
)


urlpatterns = [

    # =========================================
    # 📦 CREATE BOOKING
    # =========================================
    path(

        'book/',

        create_booking,

        name='create_booking'
    ),

    # =========================================
    # 💳 PAYMENT PAGE
    # =========================================
    path(

        'payment/<int:booking_id>/',

        payment_page,

        name='payment_page'
    ),

    # =========================================
    # ✅ PAYMENT SUCCESS
    # =========================================
    path(

        'payment-success/',

        payment_success,

        name='payment_success'
    ),

    # =========================================
    # ❌ PAYMENT FAILED
    # =========================================
    path(

        'payment-failed/',

        payment_failed,

        name='payment_failed'
    ),

    # =========================================
    # 🔄 UPDATE BOOKING STATUS
    # =========================================
    path(

        'update/<int:booking_id>/<str:status>/',

        update_booking_status,

        name='update_booking_status'
    ),

    # =========================================
    # ⭐ RATE BOOKING
    # =========================================
    path(

        'rate/<int:id>/',

        rate_booking,

        name='rate_booking'
    ),
]