from django import forms

from .models import Service


class ServiceForm(forms.ModelForm):

    class Meta:

        model = Service

        fields = [

            'category',

            'name',

            'description',

            'price',

            'image'

        ]

        widgets = {

            # 📂 CATEGORY
            'category': forms.Select(attrs={

                'class': 'form-select'

            }),

            # 🛠 SERVICE NAME
            'name': forms.TextInput(attrs={

                'class': 'form-control',

                'placeholder': 'Enter service name'

            }),

            # 📝 DESCRIPTION
            'description': forms.Textarea(attrs={

                'class': 'form-control',

                'rows': 5,

                'placeholder': 'Enter service description'

            }),

            # 💰 PRICE
            'price': forms.NumberInput(attrs={

                'class': 'form-control',

                'placeholder': 'Enter service price'

            }),

            # 🖼 IMAGE
            'image': forms.ClearableFileInput(attrs={

                'class': 'form-control'

            }),

        }

    # =========================
    # 🛠 NAME VALIDATION
    # =========================
    def clean_name(self):

        name = self.cleaned_data.get('name')

        if len(name) < 3:

            raise forms.ValidationError(

                "Service name is too short."

            )

        return name

    # =========================
    # 💰 PRICE VALIDATION
    # =========================
    def clean_price(self):

        price = self.cleaned_data.get('price')

        if price <= 0:

            raise forms.ValidationError(

                "Price must be greater than 0."

            )

        return price