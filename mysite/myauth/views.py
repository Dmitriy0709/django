from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.views import LogoutView
from .forms import UserRegistrationForm
from .models import Profile


# ========== РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ ==========

class RegisterView(CreateView):
    """
    Представление для регистрации новых пользователей
    Создаёт новый аккаунт пользователя и автоматически создаёт профиль (через сигнал)
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'myauth/register.html'
    # URL для редиректа после успешной регистрации
    success_url = reverse_lazy('myauth:login')

    def form_valid(self, form):
        """
        Обработка успешной отправки формы регистрации
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


# ========== ПОЛЬЗОВАТЕЛЬСКИЙ LOGOUT VIEW ==========

class CustomLogoutView(LogoutView):
    """
    Пользовательский класс для выхода из системы
    Переопределяет страницу перенаправления после выхода
    """
    # Страница, на которую будет перенаправлен пользователь после выхода
    next_page = reverse_lazy('myauth:login')  # Можно изменить на 'home' или другую страницу


# ========== COOKIES VIEWS ==========

def read_cookies_view(request):
    """
    Представление для чтения значения из cookies
    Учитывает отсутствие значения (добавляет значение по умолчанию)

    GET параметр: нет
    Возвращает: JSON с значением cookies
    """
    # Чтение значения cookie с именем 'theme', по умолчанию 'light'
    theme = request.COOKIES.get('theme', 'light')

    return JsonResponse({
        'status': 'success',
        'theme': theme,
        'message': f'Текущая тема: {theme}'
    })


def set_cookies_view(request):
    """
    Представление для установки значения в cookies
    Устанавливает время жизни cookie (max_age)

    GET параметр: нет
    Действие: устанавливает cookie 'theme' со значением 'dark'
    """
    # Создание ответа
    response = JsonResponse({
        'status': 'success',
        'message': 'Cookie успешно установлена'
    })

    # Установка cookie с временем жизни 1 час (3600 секунд)
    response.set_cookie('theme', 'dark', max_age=3600)

    return response


# ========== SESSION VIEWS ==========

def read_session_view(request):
    """
    Представление для чтения значения из session
    Учитывает отсутствие значения (добавляет значение по умолчанию)

    GET параметр: нет
    Возвращает: JSON с значением session
    """
    # Чтение значения session с ключом 'user_preference', по умолчанию 'default'
    user_preference = request.session.get('user_preference', 'default')

    return JsonResponse({
        'status': 'success',
        'user_preference': user_preference,
        'message': f'Ваша предпочтение: {user_preference}'
    })


def set_session_view(request):
    """
    Представление для установки значения в session
    Session сохраняется на сервере и связана с пользователем/браузером

    GET параметр: нет
    Действие: устанавливает session 'user_preference' со значением 'custom'
    """
    # Установка значения в session
    request.session['user_preference'] = 'custom'

    # Установка времени жизни session (1 час в секундах)
    request.session.set_expiry(3600)

    return JsonResponse({
        'status': 'success',
        'message': 'Session успешно установлена'
    })


# ========== ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ==========

@login_required(login_url='myauth:login')
def profile_view(request):
    """
    Представление для просмотра профиля пользователя
    Требует аутентификации (@login_required декоратор)

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
    Представление для редактирования профиля пользователя
    Требует аутентификации (@login_required декоратор)

    GET: отображает форму редактирования профиля
    POST: сохраняет изменения профиля

    Возвращаемый шаблон: myauth/profile_edit.html
    Контекст: form, profile
    """
    # Получаем профиль текущего пользователя
    profile = request.user.profile

    if request.method == 'POST':
        # Обработка POST запроса (отправка формы с редактированием)
        # request.FILES необходимо для загрузки файлов (аватар)
        from .forms import ProfileUpdateForm
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

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
        from .forms import ProfileUpdateForm
        form = ProfileUpdateForm(instance=profile)

    # Формируем контекст для шаблона
    context = {
        'form': form,
        'profile': profile
    }

    return render(request, 'myauth/profile_edit.html', context)
