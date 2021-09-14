from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserForm
from .models import CustomUser
from task_manager.tasks.models import Task


LOGIN_URL_NAME = reverse_lazy('login')
HOME_URL_NAME = reverse_lazy('home')
USERS_URL_NAME = reverse_lazy('users')


class UserListPage(ListView):
    """Class for creating a user list page."""
    model = CustomUser
    template_name = 'users.html'
    context_object_name = 'users'


class CreateUser(SuccessMessageMixin, CreateView):
    """CustomUser registration class."""
    form_class = UserForm
    template_name = 'form_create_user.html'
    success_url = LOGIN_URL_NAME
    success_message = gettext('Пользователь успешно зарегистрирован')


class UbdateUser(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    """CustomUser update class."""
    model = CustomUser
    form_class = UserForm
    template_name = 'form_update_user.html'
    success_url = USERS_URL_NAME

    login_url = LOGIN_URL_NAME
    success_message = gettext('Пользователь успешно изменён')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_authenticated and \
                obj.pk != self.request.user.pk:
            self.error_message = (
                gettext('У вас нет прав для изменения другого пользователя.')
            )
            self.login_url = USERS_URL_NAME
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
    template_name = 'delete_user.html'
    success_url = USERS_URL_NAME

    login_url = LOGIN_URL_NAME
    success_message = gettext('Пользователь успешно удалён')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context

    def delete(self, request, *args, **kwargs):
        if Task.objects.filter(author=self.request.user.pk) \
                or Task.objects.filter(executor=self.request.user.pk):
            messages.error(
                self.request,
                gettext(
                    'Невозможно удалить пользователя, '
                    +
                    'потому что он используется'
                )
            )
            return redirect(reverse_lazy(USERS_URL_NAME))
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_authenticated and \
                obj.pk != self.request.user.pk:
            self.error_message = (
                gettext('У вас нет прав для изменения другого пользователя.')
            )
            self.login_url = USERS_URL_NAME
            return False
        return True

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)
