from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model

import logging 
logger1 = logging.getLogger('file')
logger = logging.getLogger('file2')

def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # print(user, user.username, user.password)
            auth_login(request, user)
            # logger1.info(f'singupend {request.user.username} {request.user.sex} {request.user.age}')
            # logger.info('singupend', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age})
            return redirect('posts:recommend')
    else:
        form = CustomUserCreationForm()
        # logger1.info(f'singupstart {request.user.username} {request.user.sex} {request.user.age}')
        # logger.info(f'singupstart', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age})

    context = {
        'form': form,
    }

    return render(request, 'accounts_form.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            # logger1.info(f'loginend {request.user.username} {request.user.sex} {request.user.age}')
            # logger.info(f'loginend', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age})
            return redirect('posts:index')
    else:
        form = CustomAuthenticationForm()
        # logg1er.info(f'loginstart {request.user.username} {request.user.sex} {request.user.age}')
        # logger.info(f'loginstart', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age})
    context = {
        'form': form,
    }
    return render(request, 'accounts_form.html', context)


def logout(request):
    auth_logout(request)
    
    # logg1er.info(f'logout {request.user.username} {request.user.sex} {request.user.age}')
    # logger.info('logout', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age})
    return redirect('accounts:login')

def mypage(request):
    user = request.user
    context = {
        'user': user,
    }
    # logger1.info(f'mypage {request.user.username} {request.user.sex} {request.user.age}') 
    # logger.info('mypage', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age})
    return render(request, 'mypage.html', context)

def mypage_main(request):
    user = request.user
    context = {
        'user': user,
    }
    # logger1.info(f'mypage {request.user.username} {request.user.sex} {request.user.age}') 
    # logger.info('mypage', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age})
    return render(request, 'mypage_main.html', context)

def bookmark_list(request):
    user = request.user
    context = {
        'user': user,
    }
    # logger1.info(f'mypagebookmark {request.user.username} {request.user.sex} {request.user.age}') 
    # logger.info('mypagebookmark', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age})
    return render(request, 'bookmark_list.html', context)

