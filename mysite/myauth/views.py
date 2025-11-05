from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm
from .models import Profile


class RegisterView(CreateView):
    """
    Представление для регистрации новых пользователей
    Создаёт новый аккаунт и автоматически создаёт профиль пользователя
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'myauth/register.html'
    # URL для редиректа после успешной регистрации
    success_url = reverse_lazy('myauth:login')

    def form_valid(self, form):
        """
        Обработка успешной отправки формы
        """
        response = super().form_valid(form)
        user = self.object
        # Добавление сообщения об успешной регистрации
        messages.success(
            self.request,
            f'Аккаунт успешно создан для {user.username}! Пожалуйста, войдите.'
        )
        return response

    def form_invalid(self, form):
        """
        Обработка ошибок формы
        """
        # Добавление сообщений об ошибках
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)


@login_required(login_url='myauth:login')
def profile_view(request):
    """
    Функция для просмотра профиля пользователя
    Требует аутентификации

    GET параметры: нет
    Возвращаемый шаблон: myauth/profile.html
    Контекст: profile, user
    """
    # Получаем профиль текущего пользователя
    profile = request.user.profile

    # Формируем контекст для шаблона
    context = {
        'profile': profile,
        'user': request.user
    }

    return render(request, 'myauth/profile.html', context)


@login_required(login_url='myauth:login')
def profile_edit(request):
    """
    Функция для редактирования профиля пользователя
    Требует аутентификации

    GET: отображает форму редактирования
    POST: сохраняет изменения в профиле

    Возвращаемый шаблон: myauth/profile_edit.html
    Контекст: form, profile
    """
    # Получаем профиль текущего пользователя
    profile = request.user.profile

    if request.method == 'POST':
        # Обработка POST запроса (отправка формы)
        # request.FILES необходимо для загрузки файлов (аватар)
        form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            # Если форма валидна, сохраняем изменения
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('myauth:profile')
        else:
            # Если есть ошибки в форме, добавляем сообщения об ошибках
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # Обработка GET запроса (загрузка формы с текущими данными)
        form = UserProfileForm(instance=profile)

    # Формируем контекст для шаблона
    context = {
        'form': form,
        'profile': profile
    }

    return render(request, 'myauth/profile_edit.html', context)
