from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """Form for creating and editing products"""

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
