from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Profile
from .forms import RegisterForm, ProfileForm, UserUpdateForm


class RegisterView(CreateView):
    """
    View для регистрации нового пользователя.
    При успешной регистрации автоматически создается профиль пользователя.
    """
    form_class = RegisterForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:login')

    def form_valid(self, form):
        """
        Переопределенный метод form_valid.
        После сохранения формы пользователь перенаправляется на страницу входа.
        Профиль создается автоматически в методе save формы.
        """
        response = super().form_valid(form)
        return response


class AboutMeView(LoginRequiredMixin, DetailView):
    """
    View для отображения профиля пользователя (страница "О мне").
    Требует аутентификации пользователя.
    """
    model = Profile
    template_name = 'myauth/about_me.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """
        Получить профиль текущего пользователя.
        """
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """
        Добавить дополнительный контекст для шаблона.
        """
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['profile_form'] = ProfileForm(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
            context['user_form'] = UserUpdateForm(
                self.request.POST,
                instance=self.request.user
            )
        else:
            context['profile_form'] = ProfileForm(instance=self.object)
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        """
        Обработка POST запроса для обновления профиля.
        """
        self.object = self.get_object()
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=self.object
        )
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('myauth:about-me')

        context = self.get_context_data()
        context['profile_form'] = profile_form
        context['user_form'] = user_form
        return self.render_to_response(context)


# Cookie views
def get_cookie_view(request):
    """
    View для получения значения cookie.
    Получает cookie 'item_count' или возвращает значение по умолчанию.
    """
    cookies = request.COOKIES
    items_count = cookies.get('item_count', 'not set')

    return render(
        request,
        'myauth/cookie_view.html',
        context={
            'item_count': items_count,
            'view_name': 'get_cookie_view'
        }
    )


def set_cookie_view(request):
    """
    View для установки cookie.
    Устанавливает cookie 'item_count' с номером товара.
    """
    response = render(
        request,
        'myauth/cookie_view.html',
        context={'view_name': 'set_cookie_view'}
    )

    item_count = request.GET.get('items_count', 1)
    max_age = 60 * 60 * 24 * 7  # 7 дней

    response.set_cookie(
        'item_count',
        value=item_count,
        max_age=max_age,
        httponly=True
    )

    return response


# Session views
def get_session_view(request):
    """
    View для получения значения сессии.
    Получает значение 'item_count' из сессии или возвращает значение по умолчанию.
    """
    items_count = request.session.get('item_count', 'not set')

    return render(
        request,
        'myauth/session_view.html',
        context={
            'item_count': items_count,
            'view_name': 'get_session_view'
        }
    )


def set_session_view(request):
    """
    View для установки значения сессии.
    Устанавливает значение 'item_count' в сессию.
    """
    items_count = request.GET.get('items_count', 1)
    request.session['item_count'] = items_count

    return render(
        request,
        'myauth/session_view.html',
        context={'view_name': 'set_session_view'}
    )
