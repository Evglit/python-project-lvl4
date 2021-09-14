from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.users.views import LOGIN_URL_NAME
from task_manager.tasks.models import Task
from .models import Status
from .forms import StatusForm


STATUSES_URL_NAME = reverse_lazy('statuses')


class StatuseListPage(LoginRequiredMixin, ListView):
    """Class for creating a status list page."""
    model = Status
    template_name = 'statuses.html'
    context_object_name = 'statuses'
    login_url = LOGIN_URL_NAME
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class CreateStatus(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Status create class."""
    form_class = StatusForm
    template_name = 'form_create_status.html'
    success_url = STATUSES_URL_NAME
    login_url = LOGIN_URL_NAME
    success_message = gettext('Статус успешно создан')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class UpdateStatus(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Status update class."""
    model = Status
    form_class = StatusForm
    template_name = 'form_update_status.html'
    success_url = STATUSES_URL_NAME
    login_url = LOGIN_URL_NAME
    success_message = gettext('Статус успешно изменён')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return super().handle_no_permission()


class DeleteStatus(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    "Status delete class"
    model = Status
    template_name = 'delete_status.html'
    success_url = STATUSES_URL_NAME
    login_url = LOGIN_URL_NAME
    success_message = gettext('Статус успешно удалён')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object().name
        return context

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if Task.objects.filter(status=obj.pk):
            messages.error(
                self.request,
                gettext('Невозможно удалить статус, потому что он используется')
            )
            return redirect(STATUSES_URL_NAME)
        messages.success(self.request, self.success_message)
        return super(DeleteStatus, self).delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)
