from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse, HttpRequest
from django.views import View
from django.contrib.auth.models import User

from .forms import UserRegistrationForm, ProfileUpdateForm, AvatarUpdateForm
from .models import Profile


class CustomLoginView(LoginView):
    """
    Стандартное представление для входа пользователя.
    Используется встроенный класс LoginView с параметрами.
    """
    template_name = 'myauth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('myauth:about-me')


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
def about_me_view(request):
    """
    Представление для страницы about-me (профиль текущего пользователя).
    Позволяет пользователю просматривать и обновлять свой профиль и аватарку.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AvatarUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('myauth:about-me')
    else:
        form = AvatarUpdateForm(instance=profile)

    return render(request, 'myauth/about-me.html', {
        'profile': profile,
        'form': form
    })


class UserListView(ListView):
    """
    Представление для отображения списка всех пользователей.
    """
    model = User
    template_name = 'myauth/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        return User.objects.select_related('profile').all()


class UserDetailView(DetailView):
    """
    Представление для отображения детальной информации о пользователе.
    """
    model = User
    template_name = 'myauth/user_detail.html'
    context_object_name = 'user_profile'

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        # Убедимся, что у пользователя есть профиль
        Profile.objects.get_or_create(user=user)
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        # Проверяем, может ли текущий пользователь редактировать этот профиль
        can_edit = (
                self.request.user.is_authenticated and
                (self.request.user.is_staff or self.request.user == user)
        )
        context['can_edit'] = can_edit
        return context


class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """
    Представление для обновления профиля пользователя.
    Доступно только администраторам или владельцу профиля.
    """
    form_class = AvatarUpdateForm
    template_name = 'myauth/user_profile_update.html'
    login_url = 'myauth:login'

    def test_func(self):
        """
        Проверка прав доступа:
        - Администратор (is_staff) может редактировать любой профиль
        - Обычный пользователь может редактировать только свой профиль
        """
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return self.request.user.is_staff or self.request.user == user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        profile, created = Profile.objects.get_or_create(user=user)
        kwargs['instance'] = profile
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('myauth:user-detail', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        context['user_profile'] = user
        return context


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
