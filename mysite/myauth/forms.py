from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    """
    Пользовательская форма регистрации
    Расширяет встроенную форму UserCreationForm Django
    """
    # Поле электронной почты (обязательно)
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Адрес электронной почты'
        })
    )

    # Имя (необязательно)
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
        })
    )

    # Фамилия (необязательно)
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия'
        })
    )

    # Имя пользователя (обязательно)
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        })
    )

    # Пароль (обязательно)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )

    # Подтверждение пароля (обязательно)
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        """
        Проверка на уникальность электронной почты
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Эта электронная почта уже зарегистрирована.')
        return email

    def clean_username(self):
        """
        Проверка на уникальность имени пользователя
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Это имя пользователя уже занято.')
        return username

    def save(self, commit=True):
        """
        Сохранение пользователя с дополнительной обработкой
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя
    """
    # Имя пользователя
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    # Фамилия пользователя
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    # Электронная почта
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'website', 'phone', 'birth_date', 'location']
        widgets = {
            # Биография - многострочное поле
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            # Аватар - загрузка файла
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            # Веб-сайт - URL поле
            'website': forms.URLInput(attrs={
                'class': 'form-control'
            }),
            # Телефон - текстовое поле
            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            # Дата рождения - поле даты
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            # Местоположение - текстовое поле
            'location': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с предварительным заполнением данных пользователя
        """
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        """
        Сохранение профиля и обновление связанных данных пользователя
        """
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')

        if commit:
            user.save()
            profile.save()
        return profile
