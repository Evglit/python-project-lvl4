from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.views import LOGIN_URL_NAME, FORM_HTML, DELETE_HTML
from task_manager.tasks.models import Task
from .models import Label
from .forms import LabelForm


LABELS_URL_NAME = 'labels'


class LabelListPage(LoginRequiredMixin, ListView):
    """Class for creating a label list page."""
    model = Label
    template_name = 'labels.html'
    context_object_name = 'labels'
    login_url = reverse_lazy(LOGIN_URL_NAME)
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Метки'
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class CreateLabel(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Label create class."""
    form_class = LabelForm
    template_name = FORM_HTML
    success_url = reverse_lazy(LABELS_URL_NAME)
    login_url = reverse_lazy(LOGIN_URL_NAME)
    success_message = 'Метка успешно создана'
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать метку'
        context['command'] = 'Создать'
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class UpdateLabel(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Label update class."""
    model = Label
    form_class = LabelForm
    template_name = FORM_HTML
    success_url = reverse_lazy(LABELS_URL_NAME)
    login_url = reverse_lazy(LOGIN_URL_NAME)
    success_message = 'Метка успешно изменена'
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение метки'
        context['command'] = 'Изменить'
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return super().handle_no_permission()


class DeleteLabel(LoginRequiredMixin, DeleteView):
    "Label delete class"
    model = Label
    template_name = DELETE_HTML
    success_url = reverse_lazy(LABELS_URL_NAME)
    login_url = reverse_lazy(LOGIN_URL_NAME)
    success_message = 'Метка успешно удалена'
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление метки'
        context['command'] = 'Да, удалить'
        context['object'] = self.get_object()
        return context

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if Task.objects.filter(labels=obj.pk):
            messages.error(self.request, 'Невозможно удалить статус, потому что он используется')
            return redirect(reverse_lazy(LABELS_URL_NAME))
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)
