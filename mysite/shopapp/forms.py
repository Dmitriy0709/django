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
    """Форма для импорта CSV файлов"""
    csv_file = forms.FileField()


class OrderCSVImportForm(forms.Form):
    """Форма для импорта заказов из CSV/JSON/XML файла"""
    csv_file = forms.FileField(
        label='Select file',
        help_text='Upload CSV, JSON, or XML file',
        widget=forms.FileInput(attrs={
            'accept': '.csv,.json,.xml',
            'class': 'form-control'
        })
    )

    def clean_csv_file(self):
        """Валидация формата файла"""
        csv_file = self.cleaned_data['csv_file']

        # Проверка расширения файла
        allowed_extensions = ['csv', 'json', 'xml']
        file_extension = csv_file.name.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            raise forms.ValidationError(
                f'Invalid file format. Allowed formats: {", ".join(allowed_extensions)}'
            )

        # Проверка размера файла (максимум 5 МБ)
        if csv_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File size must not exceed 5 MB')

        return csv_file
