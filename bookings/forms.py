from django import forms

from .models import Booking

from datetime import date


class BookingForm(forms.ModelForm):

    class Meta:

        model = Booking

        fields = [

            'service',

            'date',

            'time',

            'phone',

            'address'

        ]

        widgets = {

            # 🔥 SERVICE
            'service': forms.Select(attrs={

                'class': 'form-select'

            }),

            # 📅 DATE
            'date': forms.DateInput(attrs={

                'class': 'form-control',

                'type': 'date'

            }),

            # ⏰ TIME
            'time': forms.TimeInput(attrs={

                'class': 'form-control',

                'type': 'time'

            }),

            # 📱 PHONE
            'phone': forms.TextInput(attrs={

                'class': 'form-control',

                'placeholder': 'Enter phone number'

            }),

            # 📍 ADDRESS
            'address': forms.Textarea(attrs={

                'class': 'form-control',

                'rows': 4,

                'placeholder': 'Enter your full address'

            }),

        }

    # =========================
    # 📅 DATE VALIDATION
    # =========================
    def clean_date(self):

        booking_date = self.cleaned_data.get('date')

        if booking_date < date.today():

            raise forms.ValidationError(

                "Past dates are not allowed."

            )

        return booking_date

    # =========================
    # 📱 PHONE VALIDATION
    # =========================
    def clean_phone(self):

        phone = self.cleaned_data.get('phone')

        if len(phone) < 10:

            raise forms.ValidationError(

                "Enter valid phone number."

            )

        return phone

    # =========================
    # 📍 ADDRESS VALIDATION
    # =========================
    def clean_address(self):

        address = self.cleaned_data.get('address')

        if len(address) < 10:

            raise forms.ValidationError(

                "Enter complete address."

            )

        return address