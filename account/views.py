from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


@login_required  # проверяет авторизован ли пользователь
def dashboard(request):
    """Если авторизован - покажет страницу дашборда, иначе перенаправит на страницу login.html"""
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


# Код ниже показан для примера, тк
# в проекте используются CBV из коробки и шаблоны registration.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # ищем username и password в БД, если есть, кладем в user объект User, т.е аутентифицируем.
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:  # если юзер есть в бд
                if user.is_active:
                    # сохраняем текущего пользователя в сессии, т.е авторизуем (логинимся)
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:  # если юзер неактивен
                    return HttpResponse('Disabled account')
            else:  # если юзера нет в БД
                return HttpResponse('Invalid login')
    else:  # если request.method == 'GET'
        form = LoginForm()
    return render(request, 'account/login_not_actual.html', {'form': form})


#################################################


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный! пароль используя set_password().
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в БД.
            new_user.save()
            # Создание профиля пользователя
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
