from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "title",
            "price",
            "location",
            "description",
            "image",
            "bedrooms",
            "bathrooms",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }