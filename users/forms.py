from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from services.models import Service


class RegisterForm(UserCreationForm):

    # 🔥 FULL NAME
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter full name'
        })
    )

    # 📱 PHONE NUMBER
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )

    # 🔥 EMAIL
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )

    # 🔥 SERVICES (FOR PROVIDER)
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    # 🔥 DOCUMENTS
    aadhar_card = forms.ImageField(required=False)
    passport_photo = forms.ImageField(required=False)
    cv = forms.FileField(required=False)
    driving_license = forms.ImageField(required=False)

    class Meta:
        model = User

        fields = [
            'first_name',
            'username',
            'email',
            'phone',
            'password1',
            'password2',
            'role'
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),

            'role': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    # 🔥 APPLY BOOTSTRAP
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # REMOVE ADMIN ROLE
        self.fields['role'].choices = [
            ('customer', 'Customer'),
            ('provider', 'Provider'),
]

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

        self.fields['aadhar_card'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['passport_photo'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['cv'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['driving_license'].widget.attrs.update({
            'class': 'form-control'
        })

    # 🔥 UNIQUE EMAIL VALIDATION
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

    # 🔥 PHONE VALIDATION
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if len(phone) < 10:
            raise forms.ValidationError(
                "Enter valid phone number."
            )

        return phone

    # 🔥 PROVIDER VALIDATION
    def clean(self):
        cleaned_data = super().clean()

        role = cleaned_data.get('role')

        if role == 'provider':

            if not cleaned_data.get('aadhar_card'):
                raise forms.ValidationError(
                    "Aadhar card is required."
                )

            if not cleaned_data.get('passport_photo'):
                raise forms.ValidationError(
                    "Passport photo is required."
                )

            if not cleaned_data.get('cv'):
                raise forms.ValidationError(
                    "CV is required."
                )

            if not cleaned_data.get('driving_license'):
                raise forms.ValidationError(
                    "Driving license is required."
                )

            if not cleaned_data.get('services'):
                raise forms.ValidationError(
                    "Select at least one service."
                )

        return cleaned_data