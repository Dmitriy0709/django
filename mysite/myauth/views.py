from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import Http404

from .forms import UserRegistrationForm, ProfileUpdateForm
from .models import Profile


class CustomLoginView(LoginView):
    """
    Стандартное представление для входа пользователя.
    Используется встроенный класс LoginView с параметрами.
    """
    template_name = 'myauth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


class CustomLogoutView(LogoutView):
    """
    Пользовательский класс для выхода пользователя.
    Переопределяем стандартный LogoutView для изменения страницы перенаправления.
    """
    next_page = 'index'


class RegisterView(FormView):
    """
    Представление для регистрации новых пользователей.
    """
    form_class = UserRegistrationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


@login_required(login_url='myauth:login')
def set_cookie_view(request):
    """
    Представление для установки значения в cookies пользователя.
    """
    response = render(request, 'myauth/set_cookie.html')
    response.set_cookie('favorite_food', 'pizza', max_age=3600)
    return response


@login_required(login_url='myauth:login')
def get_cookie_view(request):
    """
    Представление для чтения значений из cookies пользователя.
    Возвращает значение по умолчанию, если оно отсутствует.
    """
    favorite_food = request.COOKIES.get('favorite_food', 'не установлено')
    return render(request, 'myauth/get_cookie.html', {
        'favorite_food': favorite_food
    })


@login_required(login_url='myauth:login')
def set_session_view(request):
    """
    Представление для установки значения в session пользователя.
    """
    request.session['user_data'] = {
        'theme': 'dark',
        'language': 'ru',
        'notifications': True
    }
    return render(request, 'myauth/set_session.html')


@login_required(login_url='myauth:login')
def get_session_view(request):
    """
    Представление для чтения значений из session пользователя.
    Возвращает значение по умолчанию, если оно отсутствует.
    """
    user_data = request.session.get('user_data', {
        'theme': 'light',
        'language': 'en',
        'notifications': False
    })
    return render(request, 'myauth/get_session.html', {
        'user_data': user_data
    })


@login_required(login_url='myauth:login')
def profile_view(request):
    """
    Представление для просмотра и обновления профиля пользователя.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('myauth:profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'myauth/profile.html', {
        'profile': profile,
        'form': form
    })
