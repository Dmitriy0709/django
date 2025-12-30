from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продуктов.
    """
    class Meta:
        model = Product
        fields = ('name', 'description', 'price')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()


class OrderCSVImportForm(forms.Form):
    """Форма для импорта заказов из файла"""
    csv_file = forms.FileField(
        label='Select CSV/JSON/XML file',
        help_text='Supported formats: CSV, JSON, XML',
        widget=forms.FileInput(attrs={
            'accept': '.csv,.json,.xml',
            'class': 'form-control'
        })
    )

    def clean_csv_file(self):
        """Проверка расширения файла"""
        file = self.cleaned_data['csv_file']

        # Проверяем расширение
        valid_extensions = ['.csv', '.json', '.xml']
        file_extension = file.name.split('.')[-1].lower()

        if f'.{file_extension}' not in valid_extensions:
            raise forms.ValidationError(
                f'Invalid file type. Allowed types: {", ".join(valid_extensions)}'
            )

        return file
