from django import forms


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    price = forms.DecimalField(min_value=1, max_value=1000000)
    description = forms.CharField(label="Product description" ,widget=forms.Textarea)
