from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.views import LOGIN_URL_NAME
from task_manager.tasks.models import Task
from .models import Label
from .forms import LabelForm


LABELS_URL_NAME = reverse_lazy('labels')


class LabelListPage(LoginRequiredMixin, ListView):
    """Class for creating a label list page."""
    model = Label
    template_name = 'labels.html'
    context_object_name = 'labels'
    login_url = LOGIN_URL_NAME
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class CreateLabel(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Label create class."""
    form_class = LabelForm
    template_name = 'form_create_label.html'
    success_url = LABELS_URL_NAME
    login_url = LOGIN_URL_NAME
    success_message = gettext('Метка успешно создана')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class UpdateLabel(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Label update class."""
    model = Label
    form_class = LabelForm
    template_name = 'form_update_label.html'
    success_url = LABELS_URL_NAME
    login_url = LOGIN_URL_NAME
    success_message = gettext('Метка успешно изменена')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return super().handle_no_permission()


class DeleteLabel(LoginRequiredMixin, DeleteView):
    "Label delete class"
    model = Label
    template_name = 'delete_label.html'
    success_url = LABELS_URL_NAME
    login_url = LOGIN_URL_NAME
    success_message = gettext('Метка успешно удалена')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if Task.objects.filter(labels=obj.pk):
            messages.error(
                self.request,
                gettext('Невозможно удалить статус, потому что он используется')
            )
            return redirect(LABELS_URL_NAME)
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)
