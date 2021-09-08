from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserForm
from .models import CustomUser
from task_manager.tasks.models import Task


LOGIN_URL_NAME = 'login'
HOME_URL_NAME = 'home'
USERS_URL_NAME = 'users'
FORM_HTML = 'form.html'
DELETE_HTML = 'delete.html'


class HomePage(TemplateView):
    """Class for creating a home page."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserListPage(ListView):
    """Class for creating a user list page."""
    model = CustomUser
    template_name = 'users.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        return context


class CreateUser(SuccessMessageMixin, CreateView):
    """CustomUser registration class."""
    form_class = UserForm
    template_name = FORM_HTML
    success_url = reverse_lazy(LOGIN_URL_NAME)
    success_message = 'Пользователь успешно зарегистрирован'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['command'] = 'Зарегистрировать'
        return context


class LoginUser(SuccessMessageMixin, LoginView):
    """CustomUser login class."""
    form_class = AuthenticationForm
    template_name = FORM_HTML
    success_message = 'Вы залогинены'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        context['command'] = 'Войти'
        return context

    def get_success_url(seld):
        return reverse_lazy(HOME_URL_NAME)


class LogoutUser(SuccessMessageMixin, LogoutView):
    """CustomUser Logout class."""
    next_page = reverse_lazy(HOME_URL_NAME)
    success_message = 'Вы разлогинены'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, self.success_message)
        return response


class UbdateUser(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    """CustomUser update class."""
    model = CustomUser
    form_class = UserForm
    template_name = FORM_HTML
    success_url = reverse_lazy(USERS_URL_NAME)

    login_url = reverse_lazy(LOGIN_URL_NAME)
    success_message = 'Пользователь успешно изменён'
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пользователя'
        context['command'] = 'Изменить'
        return context

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_authenticated and \
                obj.pk != self.request.user.pk:
            self.error_message = (
                'У вас нет прав для изменения другого пользователя.'
            )
            self.login_url = reverse_lazy(USERS_URL_NAME)
            return False
        return True

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class DeleteUser(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    """CustomUser delete class."""
    model = CustomUser
    template_name = 'delete.html'
    success_url = reverse_lazy(USERS_URL_NAME)

    login_url = reverse_lazy(LOGIN_URL_NAME)
    success_message = 'Пользователь успешно удалён'
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление пользователя'
        context['command'] = 'Да, удалить'
        obj = self.get_object()
        context['object'] = f'{obj.first_name} {obj.last_name}'
        return context

    def delete(self, request, *args, **kwargs):
        if Task.objects.filter(author=self.request.user.pk) \
                or Task.objects.filter(executor=self.request.user.pk):
            messages.error(
                self.request,
                'Невозможно удалить пользователя, потому что он используется'
            )
            return redirect(reverse_lazy(USERS_URL_NAME))
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_authenticated and \
                obj.pk != self.request.user.pk:
            self.error_message = (
                'У вас нет прав для изменения другого пользователя.'
            )
            self.login_url = reverse_lazy(USERS_URL_NAME)
            return False
        return True

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)
