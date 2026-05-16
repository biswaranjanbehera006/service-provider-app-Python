from django.db import models
from django.conf import settings

from services.models import Service
from providers.models import Provider


User = settings.AUTH_USER_MODEL


class Booking(models.Model):

    # =========================================
    # 📌 BOOKING STATUS
    # =========================================

    STATUS_CHOICES = (

        ('pending', 'Pending'),

        ('accepted', 'Accepted'),

        ('rejected', 'Rejected'),

        ('completed', 'Completed'),

        ('cancelled', 'Cancelled'),
    )

    # =========================================
    # 💳 PAYMENT STATUS
    # =========================================

    PAYMENT_STATUS = (

        ('pending', 'Pending'),

        ('success', 'Success'),

        ('failed', 'Failed'),
    )

    # =========================================
    # 👤 CUSTOMER
    # =========================================

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name='user_bookings'
    )

    # =========================================
    # 🛠 SERVICE
    # =========================================

    service = models.ForeignKey(

        Service,

        on_delete=models.CASCADE,

        related_name='service_bookings'
    )

    # =========================================
    # 👨‍🔧 PROVIDER
    # =========================================

    provider = models.ForeignKey(

        Provider,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name='provider_bookings'
    )

    # =========================================
    # 📅 BOOKING DATE & TIME
    # =========================================

    date = models.DateField()

    time = models.TimeField()

    # =========================================
    # 📱 CUSTOMER PHONE
    # =========================================

    phone = models.CharField(
        max_length=15
    )

    # =========================================
    # 📍 CUSTOMER ADDRESS
    # =========================================

    address = models.TextField()

    # =========================================
    # 💰 PAYMENT DETAILS
    # =========================================

    amount = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=500
    )

    is_paid = models.BooleanField(

        default=False
    )

    payment_status = models.CharField(

        max_length=20,

        choices=PAYMENT_STATUS,

        default='pending'
    )

    # =========================================
    # 🔥 RAZORPAY PAYMENT IDS
    # =========================================

    payment_id = models.CharField(

        max_length=255,

        null=True,

        blank=True
    )

    razorpay_order_id = models.CharField(

        max_length=255,

        null=True,

        blank=True
    )

    razorpay_payment_id = models.CharField(

        max_length=255,

        null=True,

        blank=True
    )

    razorpay_signature = models.CharField(

        max_length=500,

        null=True,

        blank=True
    )

    # =========================================
    # ⭐ REVIEW & RATING
    # =========================================

    rating = models.IntegerField(

        null=True,

        blank=True
    )

    review = models.TextField(

        null=True,

        blank=True
    )

    # =========================================
    # 📌 BOOKING STATUS
    # =========================================

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='pending'
    )

    # =========================================
    # ⏱ TIMESTAMPS
    # =========================================

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    updated_at = models.DateTimeField(

        auto_now=True
    )

    # =========================================
    # 📊 MODEL ORDERING
    # =========================================

    class Meta:

        ordering = ['-created_at']

        verbose_name = 'Booking'

        verbose_name_plural = 'Bookings'

    # =========================================
    # 🧠 HELPER METHODS
    # =========================================

    def is_pending(self):

        return self.status == 'pending'

    def is_accepted(self):

        return self.status == 'accepted'

    def is_completed(self):

        return self.status == 'completed'

    def is_cancelled(self):

        return self.status == 'cancelled'

    def is_payment_success(self):

        return self.payment_status == 'success'

    def is_rated(self):

        return self.rating is not None

    # =========================================
    # 🔥 STRING REPRESENTATION
    # =========================================

    def __str__(self):

        return f"{self.user.username} - {self.service.name} ({self.status})"