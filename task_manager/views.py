from django.shortcuts import render


def index(request):
    return render(request, 'index.html', context={
        'title': '',
    })


def users(request):
    return render(request, 'users.html', context={
        'title': 'Пользователи',
    })


def login(request):
    return render(request, 'login.html', context={
        'title': 'Вход',
    })


def create(request):
    return render(request, 'create.html', context={
        'title': 'Регистрация',
    })
