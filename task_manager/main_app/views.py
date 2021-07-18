from django.utils.translation import gettext
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import CreateUserForm
from .models import Users
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render


class HomePage(TemplateView):
    template_name = 'main_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('')
        return context


class UsersPage(TemplateView):
    template_name = 'main_app/users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Пользователи')
        context['users'] = Users.objects.all()
        return context


class LoginPage(TemplateView):
    template_name = 'main_app/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Вход')
        return context


class CreateUser(CreateView):
    form_class = CreateUserForm
    template_name = 'main_app/create.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Регистрация')
        return context


def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                Users.objects.create(**form.cleaned_data)
                return redirect('users')
            except:
                form.add_error(None, 'Ошибка заполнения!')
    else:
        form = CreateUserForm()
    template_name = 'main_app/create.html'
    context = {
        'title': gettext('Регистрация'),
        'command': gettext('Зарегистрировать'),
        'form': form,
    }
    return render(request, template_name, context)


class UbdateUser(UpdateView):
    form_class = CreateUserForm
    template_name = 'main_app/create.html'
    success_url = reverse_lazy('users')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Изменение пользователя')
        return context


def update_user(request, user_id):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                user = Users.objects.get(pk=user_id)
                data_form = form.cleaned_data
                user.id_first_name = data_form['id_first_name']
                user.id_last_name = data_form['id_last_name']
                user.id_username = data_form['id_username']
                user.id_password1 = data_form['id_password1']
                user.id_password2 = data_form['id_password2']
                user.save()
                return redirect('users')
            except:
                form.add_error(None, 'Ошибка заполнения!')
    else:
        user = Users.objects.get(pk=user_id)
        data_form = {
            'id_first_name': user.id_first_name,
            'id_last_name': user.id_last_name,
            'id_username': user.id_username
        }
        form = CreateUserForm(data_form)

    template_name = 'main_app/create.html'
    context = {
        'title': gettext('Изменение пользователя'),
        'command': gettext('Изменить'),
        'form': form,
    }
    return render(request, template_name, context)


class UserDelete(DeleteView):
    """Don't work."""
    model = Users
    success_url = reverse_lazy('users')


def delete_user(request, user_id):
    user = Users.objects.get(pk=user_id)
    user.delete()
    return redirect('users')


def logout_user(request):
    logout(request)
    return redirect('login')
