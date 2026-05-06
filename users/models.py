from django.contrib.auth.models import AbstractUser
from django.db import models
import random


class User(AbstractUser):

    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('provider', 'Provider'),
        ('admin', 'Admin'),
    )

    # 🔥 ROLE
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer'
    )

    # 📱 PHONE NUMBER
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    # 🖼 PROFILE IMAGE
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    # 📧 EMAIL VERIFIED
    is_email_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.username


# =========================
# 🔥 EMAIL OTP MODEL
# =========================
class EmailOTP(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    otp = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def generate_otp(self):

        self.otp = str(
            random.randint(100000, 999999)
        )

        self.save()

    def __str__(self):

        return f"{self.user.email} - {self.otp}"