import random
import string

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm
from  users.services import send_register_email, send_new_password

def user_register_view(request):
    form = UserRegisterForm(request.POST) # POST
    if request.method == 'POST':
        if form.is_valid(): # Если форма валидна сохраняет введеные данные
            new_user = form.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            send_register_email(new_user.email)
            return HttpResponseRedirect(reverse('users:login_user'))
    context = {
        'form': form
    }
    return render(request, 'users/register_user.html', context)


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('dogs:index'))
                else:
                    return HttpResponse('Аккаунт неактивен!')

    form = UserLoginForm
    context = {
        'form': form
    }
    return render(request, 'users/login_user.html', context)

@login_required
def user_profile_view(request):
    user_object = request.user
    if user_object.first_name:
        user_name = user_object.first_name
    else:
        user_name = "Anonymous"
    context = {
        # 'user_object': user_object,
        'title': f'Ваш профиль {user_name}',
        # 'form': UserForm(instance=user_object),
    }
    return render(request, 'users/user_profile_read_only.html', context)

@login_required
def user_update_view(request):
    user_object = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return HttpResponseRedirect(reverse('user:profile_user'))
        user_name = user_object.first_name
        context = {
            'user_object': user_object,
            'title': f'изменит профиль {user_name}',
            'form': UserUpdateForm(instance=user_object)
        }
        return render(request, 'users/update_user.html', context)

def user_change_password_view(request):
    user_object = request.user
    form = UserPasswordChangeForm(user_object, request.POST)
    if request.method == "POST":
        if form.is_valid():
            user_object = form.save()
            update_session_auth_hash(request, user_object)
            messages.success(request, "Пароль был успешно изменен!")
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            messages.error(request, "Не удалось изменить пароль!")

    context = {
        'form': form
    }
    return render(request, 'users/change_password_user.html', context)

def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')

@login_required()
def user_generate_new_password(request):
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))