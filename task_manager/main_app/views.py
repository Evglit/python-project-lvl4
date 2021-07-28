from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

from .forms import CreateUserForm


class HomePage(TemplateView):
    """Class for creating a home page."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UsersPage(ListView):
    """Class for creating a user list page."""
    model = User
    template_name = 'users.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        return context


class CreateUser(SuccessMessageMixin, CreateView):
    """User registration class."""
    form_class = CreateUserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['command'] = 'Зарегистрировать'
        return context


class LoginUser(SuccessMessageMixin, LoginView):
    """User login class."""
    form_class = AuthenticationForm
    template_name = 'form.html'
    success_message = "Вы залогинены"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        context['command'] = 'Войти'
        return context

    def get_success_url(seld):
        return reverse_lazy('home')


class LogoutUser(SuccessMessageMixin, LogoutView):
    """User Logout class."""
    next_page = 'home'
    success_message = "Вы разлогинены"


class UbdateUser(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """User update class."""
    model = User
    form_class = CreateUserForm
    template_name = 'form.html'
    success_url = reverse_lazy('users')

    login_url = 'login'
    success_message = "Пользователь успешно изменён"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пользователя'
        context['command'] = 'Изменить'
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.pk == self.request.user.pk


class DeleteUser(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """User delete class."""
    model = User
    template_name = 'delete_user.html'
    success_url = reverse_lazy('users')

    login_url = 'login'
    success_message = "Пользователь успешно удалён"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление пользователя'
        context['command'] = 'Да, удалить'
        return context
 
    def test_func(self):
        obj = self.get_object()
        return obj.pk == self.request.user.pk
