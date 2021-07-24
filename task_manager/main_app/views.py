from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePage(TemplateView):
    """Class for creating a home page."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('')
        return context


class UsersPage(TemplateView):
    """Class for creating a user list page."""
    template_name = 'users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Пользователи')
        context['users'] = User.objects.all()
        return context


class CreateUser(CreateView):
    """User registration class."""
    form_class = CreateUserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Регистрация')
        context['command'] = gettext('Зарегистрировать')
        return context


class LoginUser(LoginView):
    """User login class."""
    form_class = AuthenticationForm
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Вход')
        context['command'] = gettext('Войти')
        return context

    def get_success_url(seld):
        return reverse_lazy('home')


class LogoutUser(LogoutView):
    """User Logout class."""
    next_page = 'home'


class UbdateUser(LoginRequiredMixin, UpdateView):
    """User update class."""
    model = User
    form_class = CreateUserForm
    template_name = 'form.html'
    success_url = reverse_lazy('users')

    login_url = 'login'
    permission_denied_message = gettext(
        'Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Изменение пользователя')
        context['command'] = gettext('Изменить')
        return context


class DeleteUser(LoginRequiredMixin, DeleteView):
    """User delete class."""
    model = User
    template_name = 'delete_user.html'
    success_url = reverse_lazy('users')

    login_url = 'login'
    permission_denied_message = gettext(
        'Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Удаление пользователя')
        context['command'] = gettext('Да, удалить')
        return context
