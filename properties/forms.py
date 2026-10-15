
from django import forms
from .models import Property, FeaturedOffer


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
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class FeaturedOfferForm(forms.ModelForm):
    class Meta:
        model = FeaturedOffer
        fields = [
            "title",
            "image",
            "description",
            "price",
            "location",
            "duration_hours",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
