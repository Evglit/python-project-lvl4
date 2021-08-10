from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Statuses
from .forms import CreateStatusForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class StatusesPage(LoginRequiredMixin, ListView):
    """Class for creating a status page."""
    model = Statuses
    template_name = 'statuses.html'
    context_object_name = 'statuses'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cтатусы'
        return context


class CreateStatus(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Status registration class."""
    form_class = CreateStatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    login_url = 'login'
    success_message = 'Статус успешно создан'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать статус'
        context['command'] = 'Создать'
        return context


class UpdateStatus(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Status update class."""
    model = Statuses
    form_class = CreateStatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    login_url = 'login'
    success_massage = 'Статус успешно изменён'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение статуса'
        context['command'] = 'Изменить'
        return context


class DeleteStatus(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    "Status delete class"
    model = Statuses
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses')
    login_url = 'login'
    success_message = "Статус успешно удалён"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление статуса'
        context['command'] = 'Да, удалить'
        context['object'] = self.get_object().name
        return context
