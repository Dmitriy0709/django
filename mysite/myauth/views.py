from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'myauth/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Custom logout view with redirect"""
    next_page = reverse_lazy('home')


class RegisterView(CreateView):
    """User registration view"""
    form_class = UserRegistrationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('login')


# Cookie views
def set_cookie_view(request):
    """View to set data in cookies"""
    response = render(request, 'myauth/set_cookie.html')
    response.set_cookie('user_preference', 'light_mode', max_age=3600 * 24 * 365)
    return response


def get_cookie_view(request):
    """View to read data from cookies"""
    user_preference = request.COOKIES.get('user_preference', 'default_mode')
    context = {
        'user_preference': user_preference
    }
    return render(request, 'myauth/get_cookie.html', context)


# Session views
def set_session_view(request):
    """View to set data in session"""
    request.session['user_theme'] = 'dark'
    request.session['language'] = 'en'
    return render(request, 'myauth/set_session.html')


def get_session_view(request):
    """View to read data from session"""
    user_theme = request.session.get('user_theme', 'light')
    language = request.session.get('language', 'en')
    context = {
        'user_theme': user_theme,
        'language': language
    }
    return render(request, 'myauth/get_session.html', context)


def profile_view(request, username):
    """View to display user profile"""
    user = User.objects.get(username=username)
    profile = user.profile
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'myauth/profile.html', context)


def edit_profile_view(request):
    """View to edit user profile"""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'myauth/edit_profile.html', context)
